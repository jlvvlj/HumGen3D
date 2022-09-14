import os
import random
from typing import Generator, List, Union

import bpy
import numpy as np
from bpy.props import CollectionProperty
from HumGen3D.backend.preferences.preference_func import get_prefs
from HumGen3D.human.keys.keys import LiveKeyItem, ShapeKeyItem

from ..base.prop_collection import PropCollection


class FaceKeys(PropCollection):
    def __init__(self, human):
        self._human = human

    #     facekeys_dict = self._get_ff_prefix_dict()

    #     for type_name, prefix in facekeys_dict.items():
    #         setattr(
    #             FaceKeys,
    #             type_name,
    #             property(self._set_prop(type_name, prefix)),
    #         )

    # def _set_prop(self, type_name, prefix):
    #     if not hasattr(self, f"_{type_name}"):
    #         filtered_sks = [sk for sk in self if sk.name.startswith(prefix)]
    #         setattr(self, f"_{type_name}", PropCollection(filtered_sks))
    #     return getattr(self, f"_{type_name}")

    @property
    def keys(self) -> List[Union[LiveKeyItem, ShapeKeyItem]]:
        return [key for key in self._human.keys.all_keys if key.category == "face"]

    @property
    def shape_keys(self) -> PropCollection:
        sks = self._human.keys
        ff_keys = [sk for sk in sks if sk.name.startswith("ff_")]
        pr_keys = [sk for sk in sks if sk.name.startswith("pr_")]
        return PropCollection(ff_keys + pr_keys)

    def reset(self):
        for sk in self.shape_keys:
            sk.value = 0

    def randomize(self, ff_subcateg="all", use_bell_curve=False):
        prefix_dict = self._get_ff_prefix_dict()
        face_sk = [
            sk for sk in self.shape_keys if sk.name.startswith(prefix_dict[ff_subcateg])
        ]
        all_v = 0
        for sk in face_sk:
            if use_bell_curve:
                new_value = np.random.normal(loc=0, scale=0.5)
            else:
                new_value = random.uniform(sk.slider_min, sk.slider_max)
            all_v += new_value
            sk.value = new_value

    @staticmethod
    def _get_ff_prefix_dict() -> dict:
        """Returns facial features prefix dict

        Returns:
            dict: key: internal naming of facial feature category
                value: naming prefix of shapekeys that belong to that category
        """
        prefix_dict = {
            "all": "ff",
            "u_skull": ("ff_a", "ff_b"),
            "eyes": "ff_c",
            "l_skull": "ff_d",
            "nose": "ff_e",
            "mouth": "ff_f",
            "chin": "ff_g",
            "cheeks": "ff_h",
            "jaw": "ff_i",
            "ears": "ff_j",
            "custom": "ff_x",
        }

        return prefix_dict
