# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE


""" # noqa D400
context.scene.HG3D

Main propertygroup of Human Generator, others are subclasses of this one.
Contains top level properties.
"""

import bpy  # type: ignore
from bpy.props import (  # type: ignore
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from HumGen3D.backend import preview_collections
from HumGen3D.human.human import Human

from .batch_props import BatchProps
from .custom_content_properties import CustomContentProps
from .preview_collection_props import PreviewCollectionProps
from .process_props import ProcessProps
from .ui_properties import UserInterfaceProps


class HG_SETTINGS(bpy.types.PropertyGroup):
    """Main property group of Human Generator.

    Contains top level properties and pointers to lower level property groups.
    """

    _register_priority = 5

    pcoll: PointerProperty(type=PreviewCollectionProps)
    ui: PointerProperty(type=UserInterfaceProps)
    custom_content: PointerProperty(type=CustomContentProps)
    batch: PointerProperty(type=BatchProps)

    process: PointerProperty(type=ProcessProps)

    # back end
    load_exception: BoolProperty(name="load_exception", default=False)
    subscribed: BoolProperty(name="subscribed", default=False)
    update_exception: BoolProperty(default=False)

    # creation
    gender: EnumProperty(
        name="Gender",
        description="Choose a gender",
        items=[
            ("male", "Male", "", 0),
            ("female", "Female", "", 1),
        ],
        default="male",
        update=lambda self, context: preview_collections["humans"].refresh(
            context, self.gender
        ),
    )

    human_height: FloatProperty(
        default=183,
        soft_min=150,
        soft_max=200,
        min=120,
        max=250,
        precision=0,
        set=lambda s, value: Human.from_existing(bpy.context.object).height.set(
            value, realtime=True, context=bpy.context
        ),
        get=lambda s: Human.from_existing(bpy.context.object).height.centimeters,
    )

    age: IntProperty(
        default=30,
        min=20,
        max=70,
        step=10,
        set=lambda s, value: Human.from_existing(bpy.context.object).age.set(
            value, realtime=True
        ),
        get=lambda s: Human.from_existing(bpy.context.object).age._current,
    )

    # skin props
    skin_sss: EnumProperty(
        description="Turns on/off subsurface scattering on the skin shader",
        items=[
            ("on", "On ", "", 0),
            ("off", "Off", "", 1),
        ],
        default="off",
        update=lambda s, c: Human.from_existing(
            c.object
        ).skin.set_subsurface_scattering(s.skin_sss == "on", c),
    )

    underwear_switch: EnumProperty(
        description="Turns on/off underwear layer",
        items=[
            ("on", "On ", "", 0),
            ("off", "Off", "", 1),
        ],
        default="on",
        update=lambda s, c: Human.from_existing(c.object).skin.set_underwear(
            s.underwear_switch == "on", c
        ),
    )

    # Dev tools
    shapekey_calc_type: EnumProperty(
        name="calc type",
        items=[
            ("pants", "Bottom", "", 0),
            ("top", "Top", "", 1),
            ("shoe", "Footwear", "", 2),
            ("full", "Full Body", "", 3),
        ],
        default="top",
    )
    dev_delete_unselected: BoolProperty(name="Delete unselected objs", default=True)
    dev_tools_ui: BoolProperty(name="Developer tools", default=True)
    calc_gender: BoolProperty(name="Calculate both genders", default=False)
    dev_mask_name: EnumProperty(
        name="mask_name",
        items=[
            ("lower_short", "Lower Short", "", 0),
            ("lower_long", "Lower Long", "", 1),
            ("torso", "Torso", "", 2),
            ("arms_short", "Arms Short", "", 3),
            ("arms_long", "Arms Long", "", 4),
            ("foot", "Foot", "", 5),
        ],
        default="lower_short",
    )

    hair_json_path: StringProperty(subtype="FILE_PATH")
    hair_json_name: StringProperty()

    hair_mat_male: EnumProperty(
        name="posing",
        items=[
            ("eye", "Eyebrows & Eyelashes", "", 0),
            ("face", "Facial Hair", "", 1),
            ("head", "Hair", "", 2),
        ],
        default="head",
    )

    hair_mat_female: EnumProperty(
        name="posing",
        items=[
            ("eye", "Eyebrows & Eyelashes", "", 0),
            ("head", "Hair", "", 1),
        ],
        default="head",
    )

    hair_shader_type: EnumProperty(
        name="Hair shader type",
        items=[
            ("fast", "Fast", "", 0),
            ("accurate", "Accurate (Cycles only)", "", 1),
        ],
        default="fast",
        update=lambda s, c: Human.from_existing(c.object).hair.update_hair_shader_type(
            s.hair_shader_type
        ),
    )

    show_hidden_tips: BoolProperty(default=False)
