import bpy  # type:ignore
import numpy as np #type:ignore


def length_from_bell_curve(sett, gender, random_seed = True, samples = 1) -> list:
    """Returns one or multiple samples from a bell curve generated from the 
    batch_average_height and batch_standard_deviation properties.

    Args:
        sett (PropertyGroup): HumGen props
        gender (str): 'male' or 'female', determines the gender specific 
            batch_average_height prop
        random_seed (bool, optional): Used by the example list to make sure the 
            list doesn't update all the time. Defaults to True.
        samples (int, optional): Amount of length samples to draw. Defaults to 0.

    Returns:
        list: with the default 0 samples it returns a single length value
            in centimeters, else it returns a list of length values in cm
    """
    
    
    if sett.batch_height_system == 'metric':
        avg_height_cm = getattr(sett, f'batch_average_height_cm_{gender}')  
    else:
        ft = getattr(sett, f'batch_average_height_ft_{gender}')  
        inch = getattr(sett, f'batch_average_height_in_{gender}')  
        avg_height_cm = ft * 30.48 + inch * 2.54
    
    sd = sett.batch_standard_deviation/100
    
    if random_seed:
        np.random.seed()
    else:
        np.random.seed(0)
        
    length_list = np.random.normal(
        loc = avg_height_cm,
        scale = avg_height_cm * sd,
        size = samples
        )
    
    print('returning', length_list)
    return length_list 

def calculate_weight(sett):
    eevee_weight = 14.5
    storage_weight = 59
    
    if sett.batch_hair:
        storage_weight += 10
        p_quality = sett.batch_hair_quality_particle
        if p_quality == 'high':
            eevee_weight += 2.8
        elif p_quality == 'medium':
            eevee_weight += 1
        elif p_quality == 'low':
            eevee_weight += 0.8
        else:
            eevee_weight += 0.2   
        
    if sett.batch_clothing:
        storage_weight += 8
        if sett.batch_apply_clothing_geometry_masks:
            storage_weight -= 1
           
    if sett.batch_delete_backup:
        storage_weight -= 42 
        
    if sett.batch_apply_shapekeys:
        storage_weight -= 6      
        if sett.batch_apply_armature_modifier:
            storage_weight -= 2
            
        if sett.batch_apply_poly_reduction:
            if sett.batch_poly_reduction == 'medium':
                storage_weight -= 5
            elif sett.batch_poly_reduction == 'high':
                storage_weight -= 6
            elif sett.batch_poly_reduction == 'ultra':
                storage_weight -= 7 

    cycles_weight = '10 (Very Fast)'
    eevee_weight = f'{eevee_weight} (Fast)'
    memory_weight = '100 (Heavy)'
    storage_weight = f'~{storage_weight} MB/human*'
    
    return cycles_weight, eevee_weight, memory_weight, storage_weight


def get_batch_marker_list(context) -> list:
    sett = context.scene.HG3D
    
    marker_selection = sett.batch_marker_selection

    all_markers = [obj for obj in bpy.data.objects if 'hg_batch_marker' in obj]
    
    if marker_selection == 'all':
        return all_markers
    
    elif marker_selection == 'selected':
        selected_markers = [
            o for o in all_markers 
            if o in context.selected_objects
            ]
        return selected_markers
    
    else:
        empty_markers = [o for o in all_markers if not has_associated_human(o)]
        return empty_markers

def has_associated_human(marker) -> bool:
    """Check if this marker has an associated human and if that object still 
    exists

    Args:
        marker (Object): marker object to check for associated human

    Returns:
        bool: True if associated human was found, False if not
    """
    
    return (
        'associated_human' in marker #does it have the prop
        and marker['associated_human'] #is the prop not empty
        and bpy.data.objects.get(marker['associated_human'].name) #does the object still exist
        and marker.location == marker['associated_human'].location #is the object at the same spot as the marker
        and bpy.context.scene.objects.get(marker['associated_human'].name) #is the object in the current scene
    )