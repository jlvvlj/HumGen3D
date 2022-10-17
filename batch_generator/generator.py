# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE

import os
import random
from typing import Literal, Optional, Union

from HumGen3D.backend.type_aliases import C  # type:ignore
from HumGen3D.batch_generator.batch_functions import height_from_bell_curve
from HumGen3D.human.base.decorators import injected_context
from HumGen3D.human.human import Human

SettingsDict = dict[str, Union[str, int, float]]


class BatchHumanGenerator:
    """Generator/factory (?) for making completed HG_Humans in the background.

    Also used by the batch panel in the Human Generator GUI
    """

    female_chance: float = 1.0
    male_chance: float = 1.0
    human_preset_category_chances: Optional[dict[str, float]] = None
    add_clothing: bool = True
    clothing_categories: Optional[list[str]] = None
    add_expression: bool = True
    add_hair: bool = True
    hair_quality: Literal["high", "medium", "low", "ultralow"] = "medium"
    average_height_male: int = 177
    average_height_female: int = 172
    height_one_standard_deviation: float = 0.05
    texture_resolution: Literal["high", "optimised", "performance"] = "optimised"

    def __init__(
        self,
        add_clothing: bool = True,
        add_hair: bool = True,
        add_expression: bool = True,
    ) -> None:
        self.add_clothing = add_clothing
        self.add_hair = add_hair
        self.add_expression = add_expression

    @injected_context
    def generate_human(
        self,
        context: C = None,
        pose_type: str = "a_pose",
    ) -> "Human":

        gender = random.choices(
            ("male", "female"), (self.male_chance, self.female_chance)
        )[0]
        if not self.human_preset_category_chances:
            presets = Human.get_preset_options(gender)
        else:
            chosen_category: str = random.choices(
                zip(*self.human_preset_category_chances.items())  # type:ignore
            )[0]
            presets = Human.get_preset_options(gender, chosen_category)

        chosen_preset = random.choice(presets)
        human = Human.from_preset(chosen_preset)

        human.body.randomize()
        human.face.randomize(use_bell_curve=gender == "female")

        human.skin.randomize()
        human.eyes.randomize()

        if self.add_hair:
            human.hair.regular_hair.randomize(context)
            human.hair.regular_hair.randomize_color()
            if human.gender == "male":
                human.hair.face_hair.randomize(context)
                human.hair.face_hair.randomize_color()

        human.hair.set_hair_quality(self.hair_quality)
        human.hair.eyebrows.randomize_color()
        human.hair.children_set_hide(True)

        human.height.set(
            height_from_bell_curve(
                self.average_height_male
                if gender == "male"
                else self.average_height_female,
                self.height_one_standard_deviation,
            )[0]
        )

        if self.add_clothing:
            if self.clothing_categories:
                clothing_category = random.choice(self.clothing_categories)
            else:
                clothing_category = "All"
            clothing_options = human.outfit.get_options(context, clothing_category)

            human.outfit.set(random.choice(clothing_options))
            human.footwear.set_random(context)

            for cloth in human.outfit.objects:
                human.outfit.randomize_colors(cloth)
                human.outfit.set_texture_resolution(cloth, self.texture_resolution)

            for cloth in human.footwear.objects:
                human.footwear.randomize_colors(cloth)
                human.footwear.set_texture_resolution(cloth, self.texture_resolution)

        if pose_type != "a_pose":
            if pose_type == "t_pose":
                human.pose.set(os.path.join("poses", "Base Poses", "HG_T_Pose.blend"))
            else:
                options = human.pose.get_options(context, category=pose_type)
                human.pose.set(random.choice(options))

        if self.add_expression:
            human.expression.set_random(context)
            # FIXME human.expression.shape_keys[0].value = random.choice(
            #    [0.5, 0.7, 0.8, 1, 1, 1]
            # )

        return human