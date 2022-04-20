# Core
from .blender_backend.content.HG_CONTENT_PACKS import (
    HG_CONTENT_PACK,
    HG_DELETE_CPACK,
    HG_DELETE_INSTALLPACK,
    HG_INSTALL_CPACK,
    HG_INSTALLPACK,
    HG_REFRESH_CPACKS,
    HG_SELECT_CPACK,
    HG_UL_CONTENTPACKS,
    HG_UL_INSTALLPACKS,
)
from .blender_backend.content.HG_CUSTOM_CONTENT_PACKS import (
    CUSTOM_CONTENT_ITEM,
    HG_OT_CREATE_CPACK,
    HG_OT_EDIT_CPACK,
    HG_OT_EXIT_CPACK_EDIT,
    HG_OT_SAVE_CPACK,
)
from .blender_backend.content.HG_UPDATE import UPDATE_INFO_ITEM
from .blender_backend.HG_CALLBACK import HG_ACTIVATE
from .blender_backend.settings.HG_PREFERENCES import (
    HG_PATHCHANGE,
    HG_PREF,
    HG_PT_ICON_LEGEND,
)
from .blender_backend.settings.HG_PROPS import HG_OBJECT_PROPS, HG_SETTINGS
from .blender_operators.batch_section.HG_BATCH_MODAL_OPERATOR import (
    HG_BATCH_GENERATE,
)
from .blender_operators.batch_section.HG_BATCH_PRIMITIVES import (
    HG_OT_ADD_BATCH_MARKER,
)
from .blender_operators.batch_section.HG_QUICK_GENERATOR import (
    HG_QUICK_GENERATE,
)
from .blender_operators.common.HG_COMMON_OPS import (
    HG_CLEAR_SEARCH,
    HG_DELETE,
    HG_DESELECT,
    HG_NEXT_PREV_HUMAN,
    HG_NEXTPREV_CONTENT_SAVING_TAB,
    HG_OPENPREF,
    HG_SECTION_TOGGLE,
)
from .blender_operators.common.HG_INFO_POPUPS import HG_OT_INFO
from .blender_operators.common.HG_RANDOM import HG_COLOR_RANDOM, HG_RANDOM
from .blender_operators.creation_phase.HG_BACKUP import HG_REVERT_TO_CREATION
from .blender_operators.creation_phase.HG_CREATION import HG_START_CREATION
from .blender_operators.creation_phase.HG_FACE import HG_RESET_FACE
from .blender_operators.creation_phase.HG_FINISH_CREATION_PHASE import (
    HG_FINISH_CREATION,
)
from .blender_operators.creation_phase.HG_HAIR import (
    HG_EYEBROW_SWITCH,
    HG_REMOVE_HAIR,
    HG_TOGGLE_HAIR_CHILDREN,
)
from .blender_operators.creation_phase.HG_HAIRCARDS import HG_CONVERT_HAIRCARDS
from .blender_operators.creation_phase.HG_LENGTH import HG_RANDOM_LENGTH

# Tutorial operator
from .blender_operators.documentation.tutorial_operator import HG_TUTORIAL_OP
from .blender_operators.finalize_phase.HG_CLOTHING import (
    HG_BACK_TO_HUMAN,
    HG_DELETE_CLOTH,
    HG_OT_PATTERN,
)
from .blender_operators.finalize_phase.HG_EXPRESSION import (
    HG_ADD_FRIG,
    HG_REMOVE_FRIG,
    HG_REMOVE_SHAPEKEY,
)
from .blender_operators.finalize_phase.HG_POSE import HG_RIGIFY
from .blender_operators.utility_section.HG_BAKE import HG_BAKE
from .blender_operators.utility_section.HG_CONTENT_SAVING import (
    HG_OT_AUTO_RENDER_THUMB,
    HG_OT_OPEN_FOLDER,
    HG_OT_SAVE_POSE,
    HG_OT_SAVE_SHAPEKEY,
    HG_OT_SAVEHAIR,
    HG_OT_SAVEOUTFIT,
    HG_OT_SAVEPRESET,
)
from .blender_operators.utility_section.HG_DEVTOOLS import (
    HG_CONVERT_HAIR_SHADER,
    HG_DELETE_STRETCH,
    HG_MASK_PROP,
    HG_RESET_BATCH_OPERATOR,
    HG_TESTOP,
)
from .blender_operators.utility_section.HG_MESH_TO_CLOTH import (
    HG_MTC_TO_A_POSE,
    HG_OT_ADDCLOTHMATH,
    HG_OT_ADDCORRECTIVE,
    HG_OT_ADDMASKS,
    HG_OT_AUTOWEIGHT,
)
from .blender_operators.utility_section.HG_UTILITY_OPS import (
    HG_MAKE_EXPERIMENTAL,
    HG_OT_MODAPPLY,
    HG_OT_PREPARE_FOR_ARKIT,
    HG_OT_REFRESH_UL,
    HG_OT_SELECTMODAPPLY,
)
from .tests.HG_CONTENT_TESTS import HG_CONTENT_TESTS

# User interface
from .user_interface import (
    HG_BATCH_PANEL,
    HG_BATCH_UILIST,
    HG_MAIN_PANEL,
    HG_UTILITY_PANEL,
    HG_UTILITY_UILISTS,
)
from .user_interface.HG_ADD_PRIMITIVE_MENU import VIEW3D_MT_HG_Marker_Add
from .user_interface.HG_CONTENT_SAVING_PANEL import (
    HG_OT_CANCEL_CONTENT_SAVING_UI,
    HG_OT_OPEN_CONTENT_SAVING_TAB,
    HG_PT_CONTENT_SAVING,
)
from .user_interface.HG_TIPS_SUGGESTIONS_UI import (
    HG_OT_HIDE_TIP,
    HG_OT_UNHIDE_TIP,
    TIPS_ITEM,
)

hg_classes = (
    # Add-on backbones
    HG_ACTIVATE,
    HG_PREF,
    # Props
    HG_SETTINGS,
    HG_OBJECT_PROPS,
    # Installation & content packs
    HG_PATHCHANGE,
    HG_CONTENT_PACK,
    HG_UL_CONTENTPACKS,
    HG_REFRESH_CPACKS,
    HG_DELETE_CPACK,
    HG_INSTALL_CPACK,
    HG_INSTALLPACK,
    HG_SELECT_CPACK,
    HG_UL_INSTALLPACKS,
    HG_DELETE_INSTALLPACK,
    # Custom content packs
    HG_OT_SAVE_CPACK,
    HG_OT_EDIT_CPACK,
    HG_OT_EXIT_CPACK_EDIT,
    CUSTOM_CONTENT_ITEM,
    HG_OT_CREATE_CPACK,
    # Panels
    HG_MAIN_PANEL.HG_PT_PANEL,
    HG_MAIN_PANEL.HG_PT_ROT_LOC_SCALE,
    # Utility
    HG_UTILITY_PANEL.HG_PT_UTILITY,
    HG_UTILITY_PANEL.HG_PT_T_BAKE,
    HG_UTILITY_PANEL.HG_PT_T_MODAPPLY,
    HG_UTILITY_PANEL.HG_PT_T_CLOTH,
    HG_UTILITY_PANEL.HG_PT_T_DEV,
    # Uilists for utility
    HG_UTILITY_UILISTS.HG_UL_MODAPPLY,
    HG_UTILITY_UILISTS.MODAPPLY_ITEM,
    HG_UTILITY_UILISTS.HG_UL_SHAPEKEYS,
    HG_UTILITY_UILISTS.SHAPEKEY_ITEM,
    HG_UTILITY_UILISTS.SAVEHAIR_ITEM,
    HG_UTILITY_UILISTS.HG_UL_SAVEHAIR,
    HG_UTILITY_UILISTS.SAVEOUTFIT_ITEM,
    HG_UTILITY_UILISTS.HG_UL_SAVEOUTFIT,
    # Batch
    HG_BATCH_PANEL.HG_PT_BATCH_Panel,
    HG_BATCH_PANEL.HG_PT_B_GENERATION_PROBABILITY,
    HG_BATCH_PANEL.HG_PT_B_HEIGHT_VARIATION,
    HG_BATCH_PANEL.HG_PT_B_HAIR,
    HG_BATCH_PANEL.HG_PT_B_CLOTHING,
    HG_BATCH_PANEL.HG_PT_B_EXPRESSION,
    HG_BATCH_PANEL.HG_PT_B_QUALITY,
    HG_BATCH_PANEL.HG_PT_B_BAKING,
    # Batch uilists
    HG_BATCH_UILIST.HG_UL_BATCH_CLOTHING,
    HG_BATCH_UILIST.HG_UL_BATCH_EXPRESSIONS,
    HG_BATCH_UILIST.BATCH_CLOTHING_ITEM,
    HG_BATCH_UILIST.BATCH_EXPRESSION_ITEM,
    HG_BATCH_UILIST.HG_REFRESH_UILISTS,
    # Pref
    HG_PT_ICON_LEGEND,
    # Custom ui
    HG_TUTORIAL_OP.HG_DRAW_PANEL,
    # Panel ops
    HG_CLEAR_SEARCH,
    HG_FINISH_CREATION,
    HG_NEXT_PREV_HUMAN,
    HG_RANDOM,
    HG_SECTION_TOGGLE,
    HG_OT_INFO,
    HG_OPENPREF,
    # Model ops
    HG_DELETE,
    HG_DESELECT,
    # Eyes
    HG_EYEBROW_SWITCH,
    # Face
    HG_RESET_FACE,
    # Posing
    HG_RIGIFY,
    # Clothing
    HG_BACK_TO_HUMAN,
    HG_OT_PATTERN,
    HG_COLOR_RANDOM,
    HG_DELETE_CLOTH,
    # Creation
    HG_START_CREATION,
    HG_REVERT_TO_CREATION,
    # Length
    HG_RANDOM_LENGTH,
    # Hair
    HG_TOGGLE_HAIR_CHILDREN,
    HG_REMOVE_HAIR,
    HG_CONVERT_HAIRCARDS,
    # Expression
    HG_REMOVE_SHAPEKEY,
    HG_ADD_FRIG,
    HG_REMOVE_FRIG,
    # Extras
    HG_MAKE_EXPERIMENTAL,
    HG_BAKE,
    HG_OT_REFRESH_UL,
    HG_OT_MODAPPLY,
    HG_OT_SELECTMODAPPLY,
    HG_OT_SAVEPRESET,
    HG_OT_OPEN_FOLDER,
    HG_OT_SAVE_SHAPEKEY,
    HG_OT_SAVEHAIR,
    HG_OT_SAVEOUTFIT,
    HG_OT_AUTOWEIGHT,
    HG_OT_ADDCORRECTIVE,
    HG_OT_ADDCLOTHMATH,
    HG_OT_ADDMASKS,
    # Devtools
    HG_DELETE_STRETCH,
    HG_MASK_PROP,
    HG_TESTOP,
    HG_CONVERT_HAIR_SHADER,
    HG_OT_PREPARE_FOR_ARKIT,
    # Update
    UPDATE_INFO_ITEM,
    # Batch
    HG_BATCH_GENERATE,
    HG_QUICK_GENERATE,
    VIEW3D_MT_HG_Marker_Add,
    HG_OT_ADD_BATCH_MARKER,
    HG_RESET_BATCH_OPERATOR,
    # New content saving
    HG_OT_CANCEL_CONTENT_SAVING_UI,
    HG_PT_CONTENT_SAVING,
    HG_OT_AUTO_RENDER_THUMB,
    HG_NEXTPREV_CONTENT_SAVING_TAB,
    HG_OT_OPEN_CONTENT_SAVING_TAB,
    HG_UTILITY_PANEL.HG_PT_CUSTOM_CONTENT,
    HG_OT_SAVE_POSE,
    HG_MTC_TO_A_POSE,
    # TIPS and suggestions
    TIPS_ITEM,
    HG_BATCH_PANEL.HG_PT_BATCH_TIPS,
    HG_UTILITY_PANEL.HG_PT_EXTRAS_TIPS,
    HG_OT_HIDE_TIP,
    HG_OT_UNHIDE_TIP,
    # Tests
    HG_CONTENT_TESTS,
)
