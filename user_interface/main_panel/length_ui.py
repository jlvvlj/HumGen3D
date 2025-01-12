# Copyright (c) 2022 Oliver J. Post & Alexander Lashko - GNU GPL V3.0, see LICENSE

import bpy

from ..panel_functions import draw_paragraph

from ..ui_baseclasses import MainPanelPart, subpanel_draw


class HG_PT_HEIGHT(MainPanelPart, bpy.types.Panel):
    bl_idname = "HG_PT_HEIGHT"
    phase_name = "height"

    @subpanel_draw
    def draw(self, context):
        col = self.layout.column(align=True)

        if self.human.process.is_lod:
            col.alert = True
            draw_paragraph(col, "LOD models can't be edited.")
            return
        elif self.human.process.rig_renamed:
            col.alert = True
            draw_paragraph(col, "Bones were renamed. Height can't be changed.")
            return

        height_m = self.human.height.meters
        height_feet = height_m / 0.3048
        height_inches = int(height_feet * 12.0 - int(height_feet) * 12.0)
        height_label = (
            str(round(height_m, 2))
            + " m   |   "
            + str(int(height_feet))
            + "'"
            + str(height_inches)
            + '"'
        )  # example: 1.83m   |   5'11"

        row = col.row()
        row.scale_y = 2
        row.alignment = "CENTER"
        row.label(text=height_label, icon="EMPTY_SINGLE_ARROW")

        row = col.row(align=True)
        row.scale_y = 2
        row.scale_x = 1.2
        row.prop(self.sett, "human_height", text="Height [cm]")
        row.operator(
            "hg3d.random_value", text="", icon="FILE_REFRESH"
        ).random_type = "height"
