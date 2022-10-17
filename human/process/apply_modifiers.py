# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE

from typing import TYPE_CHECKING, Any, no_type_check

import bpy  # type: ignore

if TYPE_CHECKING:
    from HumGen3D.backend.properties.scene_main_properties import HG_SETTINGS

from HumGen3D.backend import get_prefs, hg_log
from HumGen3D.human.keys.keys import apply_shapekeys
from HumGen3D.user_interface.content_panel.operators import (
    refresh_hair_ul,
    refresh_outfit_ul,
    refresh_shapekeys_ul,
)


class HG_OT_MODAPPLY(bpy.types.Operator):
    bl_idname = "hg3d.modapply"
    bl_label = "Apply selected modifiers"
    bl_description = "Apply selected modifiers"
    bl_options = {"UNDO"}

    @no_type_check
    def execute(self, context):  # noqa CCR001
        sett = context.scene.HG3D  # type:ignore[attr-defined]
        col = context.scene.modapply_col
        objs = build_object_list(context, sett)

        sk_dict = {}
        driver_dict = {}

        for obj in objs:
            if sett.modapply_keep_shapekeys:
                sk_dict, driver_dict = self.copy_shapekeys(
                    context, col, sk_dict, driver_dict, obj
                )
            apply_shapekeys(obj)

        objs_to_apply = objs.copy()
        for sk_list in sk_dict.values():
            if sk_list:
                objs_to_apply.extend(sk_list)

        self.apply_modifiers(context, sett, col, sk_dict, objs_to_apply)

        for obj in context.selected_objects:
            obj.select_set(False)

        if sett.modapply_keep_shapekeys:
            self.add_shapekeys_again(context, objs, sk_dict, driver_dict)

        refresh_modapply(self, context)
        return {"FINISHED"}

    @no_type_check
    def copy_shapekeys(self, context, col, sk_dict, driver_dict, obj):
        apply = False
        for item in col:
            if (
                item.mod_type == "ARMATURE"
                and (item.count or item.obj == obj)
                and item.enabled
            ):
                apply = True
        pref = get_prefs()
        # TODO this is kind of weird
        keep_sk_pref = pref.keep_all_shapekeys
        pref.keep_all_shapekeys = True
        (
            sk_dict[obj.name],
            driver_dict[obj.name],
        ) = self.human.keys._extract_permanent_keys(
            context, override_obj=obj, apply_armature=apply
        )
        pref.keep_all_shapekeys = keep_sk_pref
        return sk_dict, driver_dict

    @no_type_check
    def apply_modifiers(  # noqa CCR001 # FIXME
        self, context, sett, col, sk_dict, objs_to_apply
    ):
        if sett.modapply_search_modifiers == "summary":
            mod_types = [
                item.mod_type
                for item in col
                if item.enabled and item.mod_name != "HEADER"
            ]
            for obj in objs_to_apply:
                for mod in reversed(obj.modifiers):
                    if mod.type in mod_types:
                        self.apply(context, sett, mod, obj)
        else:
            for item in [item for item in col if item.enabled]:
                try:
                    obj = item.obj
                    mod = obj.modifiers[item.mod_name]
                    self.apply(context, sett, mod, obj)
                    if sett.modapply_keep_shapekeys:
                        for o in sk_dict[obj.name]:
                            self.apply(context, sett, mod, o)
                except Exception as e:
                    hg_log(
                        f"Error while applying modifier {item.mod_name} on ",
                        f"{item.obj}, with error as {e}",
                        level="WARNING",
                    )

    @no_type_check
    def add_shapekeys_again(self, context, objs, sk_dict, driver_dict):
        for obj in objs:
            if not sk_dict[obj.name]:
                continue
            context.view_layer.objects.active = obj
            obj.select_set(True)
            # FIXME reapply_shapekeys(
            #     context, sk_dict[obj.name], obj, driver_dict[obj.name]
            # )
            obj.select_set(False)

    @no_type_check
    def apply(self, context, sett, mod, obj):
        if sett.modapply_apply_hidden and not mod.show_viewport and not mod.show_render:
            apply = False
        else:
            apply = True

        if apply:
            context.view_layer.objects.active = obj
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                hg_log(
                    f"Error while applying modifier {mod.name} on {obj.name}, ",
                    f"with error as {e}",
                    level="WARNING",
                )


class HG_OT_REFRESH_UL(bpy.types.Operator):
    bl_idname = "hg3d.ulrefresh"
    bl_label = "Refresh list"
    bl_description = "Refresh list"

    uilist_type: bpy.props.StringProperty()

    @no_type_check
    def execute(self, context):
        if self.uilist_type == "modapply":
            refresh_modapply(self, context)
        elif self.uilist_type == "shapekeys":
            refresh_shapekeys_ul(self, context)
        elif self.uilist_type == "hair":
            refresh_hair_ul(self, context)
        elif self.uilist_type == "outfit":
            refresh_outfit_ul(self, context)
        return {"FINISHED"}


class HG_OT_SELECTMODAPPLY(bpy.types.Operator):
    bl_idname = "hg3d.selectmodapply"
    bl_label = "Select all/none modifiers"
    bl_description = "Select all/none modifiers"
    bl_options = {"UNDO"}

    select_all: bpy.props.BoolProperty()

    @no_type_check
    def execute(self, context):
        col = context.scene.modapply_col

        refresh_modapply(self, context)

        for item in col:
            item.enabled = self.select_all

        return {"FINISHED"}


def refresh_modapply(self: Any, context: bpy.types.Context) -> None:  # noqa CCR001
    sett = context.scene.HG3D  # type:ignore[attr-defined]
    col = context.scene.modapply_col
    col.clear()

    header = col.add()
    header.mod_name = "HEADER"
    header.count = 1 if sett.modapply_search_modifiers == "summary" else 0
    objs = build_object_list(context, sett)

    for obj in objs:
        for mod in obj.modifiers:
            if mod.type == "PARTICLE_SYSTEM":
                continue
            if sett.modapply_search_modifiers == "individual":
                build_full_list(col, mod, obj)  # type:ignore[arg-type]
            else:
                build_summary_list(col, mod)  # type:ignore[arg-type]


def build_object_list(
    context: bpy.types.Context, sett: "HG_SETTINGS"
) -> list[bpy.types.Object]:
    from HumGen3D.human.human import Human

    objs = [obj for obj in context.selected_objects if not obj.HG.ishuman]
    if sett.modapply_search_objects == "selected":
        return objs
    elif sett.modapply_search_objects == "full":
        human = Human.from_existing(context.object, strict_check=False)
        humans = list(human)
    else:
        humans = [obj for obj in bpy.data.objects if obj.HG.ishuman]

    for human in humans:
        if not human:
            continue
        objs.extend(list(human.children))

    return list(set(objs))


def build_full_list(
    col: bpy.types.CollectionProperty, mod: bpy.types.Modifier, obj: bpy.types.Object
) -> None:
    item = col.add()
    item.mod_name = mod.name
    item.mod_type = mod.type

    item.viewport_visible = mod.show_viewport
    item.render_visible = mod.show_render
    item.count = 0
    item.obj = obj

    if mod.type in ["ARMATURE", "SUBSURF"]:
        item.enabled = False
    else:
        item.enabled = True


def build_summary_list(
    col: bpy.types.CollectionProperty, mod: bpy.types.Modifier
) -> None:
    existing = [item for item in col if item.mod_type == mod.type]
    if existing:
        item = existing[0]
        item.count += 1
    else:
        item = col.add()
        item.mod_name = mod.type.title().replace("_", " ")
        item.mod_type = mod.type
        item.count = 1
        if mod.type in ["ARMATURE", "SUBSURF"]:
            item.enabled = False
        else:
            item.enabled = True