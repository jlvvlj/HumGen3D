import bpy

from ..core.HG_PCOLL import preview_collections
from ..features.common.HG_COMMON_FUNC import (find_human, get_prefs, hg_log,
                                              show_message)
from ..features.utility_section.HG_UTILITY_FUNC import (
    find_existing_shapekeys, refresh_hair_ul, refresh_outfit_ul,
    refresh_shapekeys_ul)
from ..user_interface.HG_UTILITY_PANEL import Tools_PT_Base


class HG_OT_CANCEL_CONTENT_SAVING_UI(bpy.types.Operator):
    """Takes the user our of the content saving UI, pack into the standard 
    interface
    
    Prereq:
    Currently in content saving UI
    """
    bl_idname      = "hg3d.cancel_content_saving_ui"
    bl_label       = "Cancel saving operation"
    bl_description = 'Cancel saving operation'
    bl_options     = {"UNDO"}

    def invoke(self, context, event):
        #confirmation checkbox
        return context.window_manager.invoke_confirm(self, event)

    def execute(self,context):
        sett = context.scene.HG3D
        sett.content_saving_ui = False
        return {'FINISHED'}
    
class HG_OT_OPEN_CONTENT_SAVING_TAB(bpy.types.Operator):
    """Opens the Content Saving UI, hiding the regular UI.

    Prereq:
    Active object is part of a HumGen human
    
    Arguments:
    content_type (str): String that indicated what content type to show the 
    saving UI for. ('shapekeys', 'clothing', 'hair', 'starting_human', 'pose')

    """
    bl_idname      = "hg3d.open_content_saving_tab"
    bl_label       = "Save custom content"
    bl_description = "Opens the screen to save custom content"

    content_type: bpy.props.StringProperty()

    def execute(self,context):  
        sett = context.scene.HG3D
        
        hg_rig = find_human(context.object)

        sett.content_saving_ui = True
        sett.content_saving_type = self.content_type  
        sett.content_saving_tab_index = 0  
        sett.content_saving_active_human = hg_rig
        
        hg_log(self.content_type)
        if self.content_type   == 'shapekeys':
            refresh_shapekeys_ul(self, context)
        elif self.content_type   == 'hair':
            refresh_hair_ul(self, context)
        elif self.content_type   == 'clothing':
            refresh_outfit_ul(self, context)
            
        if self.content_type == 'starting_human':
            unsaved_sks = self._check_if_human_uses_unsaved_shapekeys(sett)
            if unsaved_sks:
                message = self._build_sk_warning_message(unsaved_sks)
                show_message(self, message)
                
                sett.content_saving_ui = False
                return {'CANCELLED'}

        return {'FINISHED'}

    def _check_if_human_uses_unsaved_shapekeys(self, sett) -> list:
        """Check with the list of already saved shapekeys to see if this human
        uses (value above 0) any shapekeys that are not already saved.

        Args:
            sett (PropertyGroup): Add-on props

        Returns:
            list: list of names of shapekeys that are not saved
        """
        existing_sks = find_existing_shapekeys(sett, get_prefs())
        hg_log('existing sks', existing_sks)
        hg_body = sett.content_saving_active_human.HG.body_obj
        unsaved_sks = []
        for sk in hg_body.data.shape_keys.key_blocks:
            if sk.name not in existing_sks and sk.value > 0:
                unsaved_sks.append(sk.name)

    def _build_sk_warning_message(self, unsaved_sks):
        """Builds a string with newline characters to display which shapekeys
        are not saved yet.

        Args:
            unsaved_sks (list): list of unsaved shapekey names

        Returns:
            str: Message string to display to the user
        """
        message = "This human uses custom shape keys that are not saved yet! \nPlease save these shapekeys using our 'Save custom shapekeys' button:\n"
        for sk_name in unsaved_sks:
            message += f"- {sk_name}\n"
        return message

class HG_PT_CONTENT_SAVING(bpy.types.Panel): 
    """Panel that shows step by step options for saving various kinds of custom
    content. Which custom content it displays options for is determined by 
    sett.content_saving_type. Which tab it shows is determined by 
    content_saving_tab_index
    """
    bl_idname = "HG_PT_CONTENT_SAVING"
    bl_label  = " Content Saving"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI"
    bl_category    = "HumGen"
    
    @classmethod
    def poll(cls, context):
        return context.scene.HG3D.content_saving_ui

    def draw_header(self, context):
        row = self.layout.row()
        row.alert = True
        row.operator(
            'hg3d.cancel_content_saving_ui',
            text='Cancel',
            icon='X'
        )

    def draw(self, context):
        layout = self.layout
        sett = context.scene.HG3D
        self.sett = sett
        
        content_type = sett.content_saving_type

        tab_idx = sett.content_saving_tab_index

        self._draw_warning_if_different_active_human(context, layout)
        
        if content_type == 'hair':
            if tab_idx == 0:
                self._draw_particle_system_selection_ui(context, layout)
            elif tab_idx == 1:
                self._draw_thumbnail_selection_ui(context, layout, content_type)
            elif tab_idx == 2:
                self._draw_hairtype_ui(context, layout)  
            elif tab_idx == 3:
                self._draw_hair_gender_ui(context, layout)
            else:
                self._draw_name_ui(context, layout, content_type)
        elif content_type == 'starting_human':        
            if tab_idx == 0:
                self._draw_thumbnail_selection_ui(context, layout, content_type)
            elif tab_idx == 1:
                self._draw_name_ui(context, layout, content_type)
        elif content_type == 'shapekeys':
            if tab_idx == 0:
                self._draw_shapekey_selection_ui(context, layout)
            elif tab_idx == 1:
                self._draw_name_ui(context, layout, content_type)
        elif content_type == 'clothing':
            if tab_idx == 0:
                self._draw_outfit_type_selector(context, layout)
            elif tab_idx == 1:
                self._draw_clothing_uilist_ui(context, layout)
            elif tab_idx == 2:
                self._draw_thumbnail_selection_ui(context, layout, content_type)
            elif tab_idx == 3:
                self._draw_clothing_gender_ui(context, layout)
            elif tab_idx == 4:
                self._draw_name_ui(context, layout, content_type)
        elif content_type == 'pose':
            if tab_idx == 0:
                self._draw_thumbnail_selection_ui(context, layout, content_type)
            elif tab_idx == 1:
                self._draw_pose_category_ui(context, layout)
            elif tab_idx == 2:
                self._draw_name_ui(context, layout, content_type)            

    ### Blocks for all content types:
    
    def _draw_name_ui(self, context, layout, content_type):
        """Draws the tab to give the content a name

        Args:
            context (context): Blender context
            layout (UILayout): layout to draw in
            content_type (str): String about what content type this is
        """
        sett = self.sett
        
        tag_dict = {
            'hair': 'hairstyle',
            'starting_human': 'preset',
            'shapekeys': 'sk_collection',
            'clothing': 'clothing',
            'pose': 'pose'
        }
        tag = tag_dict[content_type]
        self._draw_header_box(
            layout,
            f"Give your {tag.replace('sk_', '')} a name",
            'OUTLINER_OB_FONT'
        )
        
        col = layout.column()
        col.scale_y = 1.5
        col.prop(sett, f'{tag}_name',
                 text = 'Name'
                 )
        
        self._draw_save_button(
            layout,
            content_type,
            poll=bool(getattr(sett, f'{tag}_name'))
        )

    def _draw_thumbnail_selection_ui(self, context, layout, content_type):
        """Tab to select/generate a thumbnail for this content

        Args:
            context (context): Blender context
            layout (UILayout): layout to draw in
            content_type (str): What type of content to get thumbnail for
        """
        sett = self.sett
        
        self._draw_header_box(layout, 'Select a thumbnail', icon = 'IMAGE')
        
        col = layout.column(align = True)
        col.scale_y = 1.5
        col.prop(sett, 'thumbnail_saving_enum', text = '')
        
        if sett.thumbnail_saving_enum == 'none':
            row = layout.row()
            row.alignment = 'CENTER'
            row.scale_y = 3
            row.alert = True
            row.label(text = 'No thumbnail will be exported')
            self._draw_next_button(layout)
            return
        
        img = sett.preset_thumbnail
               
        layout.template_icon_view(
            sett, "preset_thumbnail_enum",
            show_labels=True,
            scale=8,
            scale_popup=10
            )   
        if sett.thumbnail_saving_enum == 'custom':
            layout.template_ID(
                sett, "preset_thumbnail",
                open="image.open"
                )
            layout.label(text = '256*256px recommended', icon = 'INFO')
        elif sett.thumbnail_saving_enum == 'auto':
            self.__draw_auto_thumbnail_ui(layout, content_type)
            
        elif sett.thumbnail_saving_enum == 'last_render':
            self.__draw_render_result_thumbnail_ui(layout)
               
        self._draw_next_button(layout, poll = sett.preset_thumbnail)

    def __draw_render_result_thumbnail_ui(self, layout):
        """Draw UI inside thumbnail tab for picking the last render result

        Args:
            layout (UILayout): layout to draw in
        """
        layout.label(text = '256*256px recommended', icon = 'INFO')
        layout.separator()
        layout.label(text = 'If you render does not show,', icon = 'INFO')
        layout.label(text = 'reload thumbnail category above.')

    def __draw_auto_thumbnail_ui(self, layout, content_type):
        """Draw UI inside thumbnail tab for automatically rendering a thumbnail

        Args:
            layout (UILayout): layout to draw in  
            content_type (str): what type of content to make thumbnail for
        """
        row = layout.row()
        row.scale_y = 1.5
        thumbnail_type_dict = {
                'head': ('hair', 'starting_human'),
                'full_body_front': ('clothing',),
                'full_body_side': ('pose',)
            }
            
        thumbnail_type = next(t_type for t_type, c_type_set 
                                  in thumbnail_type_dict.items() 
                                  if content_type in c_type_set)
            
        row.operator(
                'hg3d.auto_render_thumbnail',
                text='Render [Automatic]',
                icon='RENDER_STILL'
            ).thumbnail_type = thumbnail_type

    def _draw_header_box(self, layout, text, icon):
        """Draws a box with an icon to show the name/description of this tab. If
        the text consists of multiple lines the icon will center in the height
        axis

        Args:
            layout (UILayout): layout to draw header box in 
            text (str): text to display in the header box, can be multiline
            icon (str): name of icon to display in the box
        """
        box = layout.box()
        
        lines = text.splitlines()
        
        split = box.split(factor = 0.1)
        icon_col = split.column()
        text_col = split.column() 
        
        icon_col.scale_y = len(lines)*0.7 if len(lines) > 1 else 1
        if len(lines) > 1:
            text_col.scale_y = 0.7

        icon_col.label(text = '', icon = icon)
        
        for line in lines:
            text_col.label(text = line)

    def _draw_next_button(self, layout, poll = True):
        """Draws a button to go to the next tab. Also draws previous button if
        the index is higher than 0. Next button is disabled if poll == False

        Args:
            layout (UILayout): layout to draw buttons in
            poll (bool, optional): poll to enable/disable next button.
                Defaults to True.
        """
        row = layout.row(align=True)
        row.scale_y = 1.5
        row.alert = True
        
        #Show previous button if the current index is higher than 0
        if self.sett.content_saving_tab_index > 0:
            row.operator(
                'hg3d.nextprev_content_saving_tab',
                text='Previous',
                icon='TRIA_LEFT',
                depress=True
            ).next = False
        
        #Hide next button if poll is False
        if not poll:
            row = row.row(align = True)
            row.enabled = False
            
        row.operator(
            'hg3d.nextprev_content_saving_tab',
            text='Next',
            icon='TRIA_RIGHT',
            depress=True
        ).next = True

    def _draw_save_button(self, layout, content_type, poll = True):
        """Draws a saving button on the last tab of the content saving ui. Also
        shows small previous button next to it. Button is disabled if poll == 
        False

        Args:
            layout (UILayout): layout to draw button in
            content_type (str): type of content to save
            poll (bool, optional): Decides if button is enabled.
                Defaults to True.
        """
        split = layout.split(factor = 0.1, align = True)
        row = split.row(align = True)
        row.scale_y = 1.5
        row.alert = True
        row.operator(
            'hg3d.nextprev_content_saving_tab',
            text='',
            icon='TRIA_LEFT',
            depress=True
        ).next = False
        
        row = split.row(align=True)
        row.enabled = poll
        row.scale_y = 1.5
        row.operator(
            f'hg3d.save_{content_type}',
            text='Save',
            icon='FILEBROWSER',
            depress=True
        )

    def _draw_warning_if_different_active_human(self, context, layout):
        """Draw a warning at the top of the content saving tab if the user has
        selected a different human than the one the content saving was 
        initialised for.

        Args:
            context (context): BL context
            layout (UILayout): layout to draw warning button in
        """
        sett = self.sett
        
        active_human = find_human(context.object)
        try:            
            if active_human and active_human != sett.content_saving_active_human:
                row = layout.row()
                row.alert = True
                row.label(
                    text=f'Selected human is not {sett.content_saving_active_human.name}'
                )
        except Exception as e:
            row = layout.row()
            row.alert = True
            row.label(text='Human seems to be deleted')            
  
  
  
    ### Hair tabs    
         
    def _draw_hair_gender_ui(self, context, layout):
        """Draws the tab for the user to select for which gender this hairstyle
        is meant.

        Args:
            context (context): bl context
            layout (UIlayout): layout to draw tab in
        """
        sett = self.sett
        
        self._draw_header_box(
            layout,
            "Is this style for men, women \nor all genders?",
            'COMMUNITY'
        )
        
        col = layout.column()
        col.scale_y = 1.5
        col.prop(sett, 'savehair_male',
                 text = 'Male',
                 toggle= True
                 )    
        subrow = col.row(align = True)
        subrow.enabled = False if sett.save_hairtype == 'facial_hair' else True  
        subrow.prop(sett, 'savehair_female',
                    text = 'Female',
                    toggle= True
                    )      
        
        poll = any((sett.savehair_male, sett.savehair_female))
        self._draw_next_button(layout, poll = poll)    
          
    def _draw_hairtype_ui(self, context, layout):
        """Draws layout for the user to select if this is facial hair or regular
        hair.

        Args:
            context (context):  bl context
            layout (UILayout): layout to draw tab in
        """
        sett = self.sett
        
        self._draw_header_box(layout, "Is this style facial hair?", 'COMMUNITY')
        
        col = layout.column()
        col.scale_y = 1.5
        col.prop(sett, 'save_hairtype', expand = True)
        
        self._draw_next_button(layout)

    def _draw_particle_system_selection_ui(self, context, layout):
        """Draws a UIList for the user to select which particle systems to save
        for this hairstyle

        Args:
            context (context): bl context
            layout (UILayout): layout to draw tab in
        """
        
        self._draw_header_box(
            layout,
            'Select particle systems \nto be included in this style.',
            'OUTLINER_OB_HAIR'
        )
        
        
        col = layout.column(align = True)
        row = col.row(align = True)
        hg_icons = preview_collections['hg_icons']
        
        row.operator('hg3d.ulrefresh',
                     text = 'Refresh hairsystems'
                     ).type = 'hair'
        row.prop(self.sett, 'show_eyesystems',
                 text = '',
                 icon_value = hg_icons['eyes'].icon_id,
                 toggle = True
                 )

        col.template_list(
            "HG_UL_SAVEHAIR",
            "",
            context.scene,
            "savehair_col",
            context.scene,
            "savehair_col_index"
            )
        
        poll = [i for i in context.scene.savehair_col if i.enabled]
        self._draw_next_button(layout, poll)
        
        
        
    
    ### Pose tabs    
        
    def _draw_pose_category_ui(self, context, layout):
        """Draws the tab for selecting in which category this pose should be
        saved.

        Args:
            context (context): bl context
            layout (UILayout): layout to draw tab in
        """
        self._draw_header_box(
            layout,
            "What category should this \npose be saved to?",
            'ARMATURE_DATA'
        )

        col = layout.column()
        col.scale_y = 1.5
        
        row = col.row()
        row.prop(self.sett, 'pose_category_to_save_to', expand = True)
        
        col.separator()
        
        if self.sett.pose_category_to_save_to == 'existing':
            col.prop(self.sett, 'pose_chosen_existing_category', text = '')
            poll = self.sett.pose_chosen_existing_category != 'All'
        else:
            col.prop(self.sett, 'pose_new_category_name', text = 'Name')
            poll = self.sett.pose_new_category_name
        
        col.separator()  
                
        self._draw_next_button(layout, poll = poll)




    ### Clothing tabs

    def _draw_clothing_gender_ui(self, context, layout):
        """Draws a tab for the user to select for which gender(s) this clothing
        item is meant.

        Args:
            context (context): bl context
            layout (UILayout): layout to draw this tab in
        """
        self._draw_header_box(layout, "Is this clothing for men \nwomen or all genders?", 'MOD_CLOTH')
        
        col = layout.column(align = True)
        col.scale_y = 1.5
        sett = self.sett
        
        col.prop(sett, 'saveoutfit_male', text = 'Male', toggle= True)    
        col.prop(sett, 'saveoutfit_female', text = 'Female', toggle= True)      
        
        poll = any((sett.saveoutfit_male, sett.saveoutfit_female))  
        self._draw_next_button(layout, poll = poll)      
    
    def _draw_clothing_uilist_ui(self, context, layout):
        """Draws a UIList tab for selecting which clothing items should be saved
        for this outfit/footwear

        Args:
            context (context): bl context
            layout (UIlayout): layout to draw tab in
        """
        self._draw_header_box(layout, "Select which objects are \npart of this outfit.", 'MOD_CLOTH')
        
        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator('hg3d.ulrefresh',
                     text = 'Refresh objects'
                     ).type = 'outfit'
        col.template_list("HG_UL_SAVEOUTFIT",
                          "",
                          context.scene,
                          "saveoutfit_col",
                          context.scene,
                          "saveoutfit_col_index"
                          )       
        
        poll = [i for i in context.scene.saveoutfit_col if i.enabled]
        self._draw_next_button(layout, poll = poll)   

    def _draw_outfit_type_selector(self, context, layout):
        """Draws a tab for the user to select if this is an outfit or footwear

        Args:
            context (context): bl context
            layout (UILayout): layout to draw tab in
        """
        self._draw_header_box(layout, "Are you saving an outfit \nor footwear?", 'MOD_CLOTH')
        
        col = layout.column()
        col.scale_y = 1.5
        col.prop(self.sett, 'saveoutfit_categ', expand = True)
        
        self._draw_next_button(layout)        




    ### Shapekey tabs

    def _draw_shapekey_selection_ui(self, context, layout):
        """Draws a tab with an UIList for the user to select which shapekeys to
        save in this collection

        Args:
            context (context): bl context
            layout (UILayout): layout to draw tab in
        """
        sett = self.sett
        self._draw_header_box(layout, "Select shapekeys to save", 'SHAPEKEY_DATA')
        
        col = layout.column(align = True)
        
        col.operator(
            'hg3d.ulrefresh',
            text = 'Refresh shapekeys'
            ).type = 'shapekeys'
        col.template_list(
            "HG_UL_SHAPEKEYS",
            "",
            context.scene,
            "shapekeys_col",
            context.scene,
            "shapekeys_col_index"
            )
        
        col.separator()
        
        col.prop(sett, 'show_saved_sks',
                 text = 'Show already saved shapekeys',
                 icon = ('CHECKBOX_HLT' 
                         if sett.show_saved_sks 
                         else 'CHECKBOX_DEHLT'))     
        
        poll = [i for i in context.scene.shapekeys_col if i.enabled]
        self._draw_next_button(layout, poll = poll)   

