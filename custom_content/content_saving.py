# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE

import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path
from shutil import copyfile

import bpy
from HumGen3D.backend import get_addon_root, get_prefs, hg_delete, hg_log
from HumGen3D.human.base.shapekey_calculator import (
    build_distance_dict,
    deform_obj_from_difference,
)
from HumGen3D.human.height.height import apply_armature
from HumGen3D.human.keys.keys import apply_shapekeys
from HumGen3D.user_interface.documentation.feedback_func import (
    ShowMessageBox,
    show_message,
)
from mathutils import Vector

refresh_pcoll = None  # FIXME


class Content_Saving_Operator:
    def overwrite_warning(self):
        """Show a warning popup if the file already exists"""
        layout = self.layout
        col = layout.column(align=True)
        col.label(text=f'"{self.name}" already exists in:')
        col.label(text=self.folder)
        col.separator()
        col.label(text="Overwrite?")

    @staticmethod
    def save_thumb(folder, img_name, save_name):
        """Save the thumbnail with this content

        Args:
            folder (Path): folder where to save it
            current_name (str): current name of the image
            save_name (str): name to save the image as
        """
        img = bpy.data.images[img_name]
        thumbnail_type = bpy.context.scene.HG3D.custom_content.thumbnail_saving_enum

        destination_path = os.path.join(folder, f"{save_name}.jpg")
        if thumbnail_type in ("last_render", "auto"):
            image_name = (
                "temp_render_thumbnail"
                if thumbnail_type == "last_render"
                else "temp_thumbnail"
            )
            source_image = os.path.join(
                get_prefs().filepath, "temp_data", f"{image_name}.jpg"
            )
            hg_log("Copying", source_image, "to", destination_path)
            copyfile(source_image, destination_path)

        else:
            try:
                img.filepath_raw = os.path.join(folder, f"{save_name}.jpg")
                img.file_format = "JPEG"
                img.save()
            except RuntimeError as e:
                # show_message(self, "Thumbnail image doesn't have any image data")
                print(e)

    @staticmethod
    def save_objects_optimized(
        context,
        objs,
        folder,
        filename,
        clear_sk=True,
        clear_materials=True,
        clear_vg=True,
        clear_ps=True,
        run_in_background=True,
        clear_drivers=True,
    ):
        """Saves the passed objects as a new blend file, opening the file in the
        background to make it as small as possible

        Args:
            objs              (list)          : List of objects to save
            folder            (Path)          : Folder to save the file in
            filename          (str)           : Name to save the file as
            clear_sk          (bool, optional): Remove all shapekeys from objs.
                                                Defaults to True.
            clear_materials   (bool, optional): Remove all materials from objs.
                                                Defaults to True.
            clear_vg          (bool, optional): Remove all vertex groups from
                                                objs. Defaults to True.
            clear_ps          (bool, optional): Remove all particle systems from
                                                objs. Defaults to True.
            run_in_background (bool, optional): Open the new subprocess in the
                                                background. Defaults to True.
        """
        for obj in objs:
            if obj.type != "MESH":
                continue
            if clear_materials:
                obj.data.materials.clear()
            if clear_vg:
                obj.vertex_groups.clear()
            if clear_sk:
                Content_Saving_Operator._remove_shapekeys(obj)
            if clear_ps:
                Content_Saving_Operator._remove_particle_systems(context, obj)
            if clear_drivers:
                Content_Saving_Operator._remove_obj_drivers(obj)

        if clear_drivers:
            Content_Saving_Operator._clear_sk_drivers()

        new_scene = bpy.data.scenes.new(name="test_scene")
        new_col = bpy.data.collections.new(name="HG")
        new_scene.collection.children.link(new_col)
        for obj in objs:
            new_col.objects.link(obj)

        if not os.path.exists(folder):
            os.makedirs(folder)

        blend_filepath = os.path.join(folder, f"{filename}.blend")
        bpy.data.libraries.write(blend_filepath, {new_scene})

        # python_file = os.path.join(get_addon_root(), "scripts", "hg_purge.py")
        # if run_in_background:
        #     hg_log("STARTING HumGen background process", level="BACKGROUND")
        #     background_blender = subprocess.Popen(
        #         [
        #             bpy.app.binary_path,
        #             blend_filepath,
        #             "--background",
        #             "--python",
        #             python_file,
        #         ],
        #         stdout=subprocess.DEVNULL,
        #     )
        # else:
        #     subprocess.Popen(
        #         [bpy.app.binary_path, blend_filepath, "--python", python_file]
        #     )

        bpy.data.scenes.remove(new_scene)

    @staticmethod
    def _clear_sk_drivers():
        for key in bpy.data.shape_keys:
            try:
                fcurves = key.animation_data.drivers
                for _ in fcurves:
                    fcurves.remove(fcurves[0])
            except AttributeError:
                pass

    @staticmethod
    def _remove_obj_drivers(obj):
        try:
            drivers_data = obj.animation_data.drivers

            for dr in drivers_data[:]:
                obj.driver_remove(dr.data_path, -1)
        except AttributeError:
            return

    @staticmethod
    def _remove_particle_systems(context, obj):
        """Remove particle systems from the passed object

        Args:
            obj (Object): obj to remove particle systems from
        """
        context.view_layer.objects.active = obj
        for i, ps in enumerate(obj.particle_systems):
            obj.particle_systems.active_index = i
            bpy.ops.object.particle_system_remove()

    @staticmethod
    def _remove_shapekeys(obj):
        """Remove shapekeys from the passed object

        Args:
            obj (Object): obj to remove shapekeys from
        """
        for sk in [sk for sk in obj.data.shape_keys.key_blocks if sk.name != "Basis"]:
            obj.shape_key_remove(sk)
        if obj.data.shape_keys:
            obj.shape_key_remove(obj.data.shape_keys.key_blocks["Basis"])

    @staticmethod
    def remove_number_suffix(name) -> str:
        """Remove the number suffix from the passed name
        (i.e. Box.004 becomes Box)

        Args:
            name (str): name to remove suffix from

        Returns:
            str: name without suffix
        """
        re_suffix = re.search(r".\d\d\d", name)
        if not re_suffix or not name.endswith(re_suffix.group(0)):
            return name
        else:
            return name.replace(re_suffix.group(0), "")
