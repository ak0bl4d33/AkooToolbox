bl_info = {
    "name": "AkooToolbox",
    "author": "ak0bl4d3",
    "version": (1, 0),
    "blender": (4, 5, 3),
    "location": "View3D > Tool Shelf",
    "description": "Surface Deform and Shape Keys from Source to active Mesh",
    "category": "Object",
}

import bpy
import json
import os

context = bpy.context
#region def Save/Load Presets and Config
# R-Start - Save/Load Presets ( PRESETS )
def get_presets_path():
    return os.path.join(bpy.utils.user_resource('CONFIG'), "AkooToolbox_presets.json")

def load_presets():
    try:
        with open(get_presets_path(), 'r') as f:
            return json.load(f)
    except:
        return {}

def save_presets(presets):
    try:
        with open(get_presets_path(), 'w') as f:
            json.dump(presets, f, indent=4)
    except Exception as e:
        print(f"[AkooToolbox] Fehler beim Speichern der Presets: {e}")
# R-End - Save/Load Presets
# R-Start - Save Settings across sessions ( CONFIG )
def get_config_path():
    return os.path.join(bpy.utils.user_resource('CONFIG'), "AkooToolbox_config.json")

def save_user_data(data: dict):
    try:
        with open(get_config_path(), 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"[AkooToolbox] Fehler beim Speichern: {e}")

def load_user_data() -> dict:
    try:
        with open(get_config_path(), 'r') as f:
            return json.load(f)
    except:
        return {}
# R-End - Save Settings across sessions
#endregion

#region def get_mesh_objects
# This is for the SOURCE MESH DropDown! (Collects all Objects which are MESH)
def get_mesh_objects(self, context):
    return [(obj.name, obj.name, "") for obj in context.scene.objects if obj.type == 'MESH']
#endregion

#region class save/load/del akopresets
# R-Start - SAVE
class OBJECT_OT_save_akoopreset(bpy.types.Operator):
    bl_idname = "object.save_akoopreset"
    bl_label = "Save Preset"

    def execute(self, context):
        name = context.scene.akoopreset_newname.strip()
        if not name:
            self.report({'ERROR'}, "Please enter a preset name.")
            return {'CANCELLED'}
        presets = load_presets()
        presets[name] = {
            "surface_deform_include_exclude_textfield": context.scene.surface_deform_include_exclude_textfield,
            "surface_deform_falloff": context.scene.surface_deform_falloff,
            "surface_deform_strength": context.scene.surface_deform_strength,
            "vertex_groups_include_exclude_textfield": context.scene.vertex_groups_include_exclude_textfield,
            "vertex_mix_mode": context.scene.vertex_mix_mode,
            "vertex_mix_set": context.scene.vertex_mix_set,
            "vertex_mix_normalize": context.scene.vertex_mix_normalize,
            "vertex_mix_default_a": context.scene.vertex_mix_default_a,
            "vertex_mix_default_b": context.scene.vertex_mix_default_b,
            "vertex_mapping_method": context.scene.vertex_mapping_method,
            "weightpaint_smoothing_amount": context.scene.weightpaint_smoothing_amount,
            "viewportdisplay_settings": context.scene.viewportdisplay_settings
        }
        save_presets(presets)
        self.report({'INFO'}, f"Preset '{name}' saved.")
        return {'FINISHED'}
# R-End - SAVE
# R-Start - LOAD
class OBJECT_OT_load_akoopreset(bpy.types.Operator):
    bl_idname = "object.load_akoopreset"
    bl_label = "Load Preset"

    def execute(self, context):
        name = context.scene.akoopreset_list
        presets = load_presets()
        preset = presets.get(name)
        if not preset:
            self.report({'ERROR'}, f"Preset '{name}' not found.")
            return {'CANCELLED'}
        context.scene.surface_deform_include_exclude_textfield = preset.get("surface_deform_include_exclude_textfield", "")
        context.scene.surface_deform_falloff = preset.get("surface_deform_falloff", 4.0)
        context.scene.surface_deform_strength = preset.get("surface_deform_strength", 1.0)
        context.scene.vertex_groups_include_exclude_textfield = preset.get("vertex_groups_include_exclude_textfield", "")
        context.scene.vertex_mix_mode = preset.get("vertex_mix_mode", "ADD")
        context.scene.vertex_mix_set = preset.get("vertex_mix_set", "ALL")
        context.scene.vertex_mix_normalize = preset.get("vertex_mix_normalize", False)
        context.scene.vertex_mix_default_a = preset.get("vertex_mix_default_a", 0.0)
        context.scene.vertex_mix_default_b = preset.get("vertex_mix_default_b", 0.0)
        context.scene.vertex_mapping_method = preset.get("vertex_mapping_method", "POLYINTERP_NEAREST")
        context.scene.weightpaint_smoothing_amount = preset.get("weightpaint_smoothing_amount", 2)
        context.scene.viewportdisplay_settings = preset.get("viewportdisplay_settings", "")
        self.report({'INFO'}, f"Preset '{name}' loaded.")
        return {'FINISHED'}
# R-End - LOAD
# R-Start - DELETE
class OBJECT_OT_delete_akoopreset(bpy.types.Operator):
    bl_idname = "object.delete_akoopreset"
    bl_label = "Delete Preset"
    def execute(self, context):
        name = context.scene.akoopreset_list
        presets = load_presets()
        if name in presets:
            del presets[name]
            save_presets(presets)
            self.report({'INFO'}, f"Preset '{name}' deleted.")
        else:
            self.report({'WARNING'}, f"Preset '{name}' not found.")
        return {'FINISHED'}
# R-End - DELETE 
#endregion

#region class save settings
class OBJECT_OT_save_settings(bpy.types.Operator):
    bl_idname = "object.save_settings" 
    bl_label = "Save Settings" 
    bl_description = "Saves the settings for the next time you open Blender." 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context): 
        save_user_data({
            "last_surface_deform_falloff_object": context.scene.surface_deform_falloff,
            "last_surface_deform_strength_object": context.scene.surface_deform_strength,
            "last_include_exclude_shapekeys_object": context.scene.surface_deform_include_exclude_textfield,
            "last_include_exclude_vertex_groups_object": context.scene.vertex_groups_include_exclude_textfield,
            "vertex_mix_mode": context.scene.vertex_mix_mode,
            "vertex_mix_set": context.scene.vertex_mix_set,
            "vertex_mix_normalize": context.scene.vertex_mix_normalize,
            "vertex_mix_default_a": context.scene.vertex_mix_default_a,
            "vertex_mix_default_b": context.scene.vertex_mix_default_b,
            "last_mapping_vertex_groups_object": context.scene.vertex_mapping_method,
            "last_viewportdisplay_settings_object": context.scene.viewportdisplay_settings,
            "last_weightpaint_smoothing_amount_object": context.scene.weightpaint_smoothing_amount
        }) 
        self.report({'INFO'}, "Settings saved.") 
        return {'FINISHED'}
#endregion
    
#region class Surface Deform
class OBJECT_OT_surface_deform_with_shapes(bpy.types.Operator): 
    bl_idname = "object.surface_deform_with_shapes" 
    bl_label = "Deform" 
    bl_description = "Transfers all Shapekeys from Source to Target." 
    bl_options = {'REGISTER', 'UNDO'} 

    surface_deform_include_exclude_textfield: bpy.props.StringProperty(
        name="Include/Exclude",
        description="Comma-separated list of ShapeKeys to include/exclude."
    ) # type: ignore
    surface_deform_include_exclude_selector: bpy.props.EnumProperty(
        name="Mode",
        description="Select the mode for including/excluding ShapeKeys.",
        items=[
            ('INCLUDE', "Include", "Include specified ShapeKeys"),
            ('EXCLUDE', "Exclude", "Exclude specified ShapeKeys"),
        ]
    ) # type: ignore
    interpolation_falloff: bpy.props.FloatProperty(
        name="Interpolation Falloff",
        description="How smooth the deformation is",
        default=4.0,
        min=0.0,
        max=100.0
    )  # type: ignore

    strength: bpy.props.FloatProperty(
        name="Strength",
        description="Deformation strength",
        default=1.0,
        min=0.0,
        max=1.0
    )  # type: ignore

    source_object: bpy.props.EnumProperty(
        name="Source Mesh",
        description="Object with Shape Keys",
        items=get_mesh_objects
    ) # type: ignore

    def execute(self, context): 
        source = bpy.data.objects.get(context.scene.surface_deform_source)
        target = context.active_object 
        if not source or not target: 
            self.report({'ERROR'}, "Source or Target-Object unavailable.") 
            return {'CANCELLED'}
        if source == target: 
            self.report({'ERROR'}, "Source or Target-Object shouldn't be the same.") 
            return {'CANCELLED'}
        mod = target.modifiers.new(name="SurfaceDeform", type='SURFACE_DEFORM')
        bpy.data.objects[target.name].modifiers["SurfaceDeform"].target = source
        bpy.data.objects[target.name].modifiers["SurfaceDeform"].falloff = context.scene.surface_deform_falloff
        bpy.data.objects[target.name].modifiers["SurfaceDeform"].strength = context.scene.surface_deform_strength
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=0)
        bpy.ops.object.surfacedeform_bind(modifier=mod.name)
        if not source.data.shape_keys: 
            self.report({'WARNING'}, "Source has no ShapeKeys.")
        else: 
            def resetShapeKeyWeights(obj): 
                if (None != obj.data.shape_keys):
                    shapeKeys = obj.data.shape_keys.key_blocks.keys()
                    for i in shapeKeys:
                        obj.data.shape_keys.key_blocks[i].value = 0
            def saveSurfaceDeformAsShapeKey(obj): 
                override = bpy.context.copy() 
                override["selected_objects"] = context.scene.objects[obj.name] 
                with bpy.context.temp_override(**override): 
                    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="SurfaceDeform")
            if (target.data.shape_keys == None): 
                target.shape_key_add(name = "Basis")          
            resetShapeKeyWeights(target)
            shapeKeys = source.data.shape_keys.key_blocks.keys()
            targetShapeKeys = target.data.shape_keys.key_blocks.keys()
            if context.scene.surface_deform_include_exclude_selector == 'INCLUDE':
                include_list = [name.strip() for name in context.scene.surface_deform_include_exclude_textfield.split(",") if name.strip()]
                exclude_list = []
            else:
                include_list = []
                exclude_list = [name.strip() for name in context.scene.surface_deform_include_exclude_textfield.split(",") if name.strip()]
            for i in shapeKeys:
                if i == "Basis": 
                    continue
                if include_list and i not in include_list: 
                     continue
                if exclude_list and i in exclude_list: 
                     continue
                resetShapeKeyWeights(source)
                if i in targetShapeKeys: 
                    print (f"ShapeKey '{i}' already exists in target. Skipping...")
                else: 
                    source.data.shape_keys.key_blocks[i].value = 1 
                    saveSurfaceDeformAsShapeKey(target) 
                    target.data.shape_keys.key_blocks['SurfaceDeform'].name = i 
            resetShapeKeyWeights(source)
            bpy.ops.object.surfacedeform_bind(modifier=mod.name)
            bpy.ops.object.modifier_remove(modifier=mod.name)
        self.report({'INFO'}, f"{len(source.data.shape_keys.key_blocks)} Transfer ShapeKeys successful.") 
        return {'FINISHED'}     
#endregion
#region class Paste Locked ShapeKeys
class OBJECT_OT_shapekeys_paste_locked(bpy.types.Operator):
    bl_idname = "object.shapekeys_paste_locked"
    bl_label = "Paste Locked"
    bl_description = "Collect all locked ShapeKeys on the active object and put them into the Include field (comma-separated)."
    bl_options = {'REGISTER', 'UNDO'}

    from typing import ClassVar, Any
    replace: ClassVar[Any]
    replace = bpy.props.BoolProperty(
        name="Replace Existing",
        description="Replace current Include text. If off, append found ShapeKeys.",
        default=True
    )
    include_basis: ClassVar[Any]
    include_basis = bpy.props.BoolProperty(
        name="Include 'Basis'",
        description="Also include the Basis key (usually you don't want this).",
        default=False
    )    
    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active Object is no Mesh.")
            return {'CANCELLED'}
        locked = [sk.name for sk in obj.data.shape_keys.key_blocks if getattr(sk, "lock_shape", False)]
        if not locked:
            self.report({'INFO'}, "No locked ShapeKeys found.")
            return {'CANCELLED'}
        scene = context.scene
        existing = scene.surface_deform_include_exclude_textfield.strip()
        if self.replace or not existing:
            names = locked
        else:
            current = [n.strip() for n in existing.split(",") if n.strip()]
            names = current + [n for n in locked if n not in current]
        scene.surface_deform_include_exclude_textfield = ", ".join(names)
        self.report({'INFO'}, f"Excluded {len(locked)} locked ShapeKeys.")
        return {'FINISHED'}
    
#endregion
#region class remove empty shapekeys
class OBJECT_OT_remove_empty_shapekeys(bpy.types.Operator): 
    bl_idname = "object.remove_empty_shapekeys" 
    bl_label = "Remove empty ShapeKeys" 
    bl_description = "removes ShapeKeys without any delta from Basis." 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context): 
        obj = context.active_object 
        if not obj or obj.type != 'MESH': 
            self.report({'ERROR'}, "Active Object is no Mesh.") 
            return {'CANCELLED'}         
        if not obj.data.shape_keys: 
            self.report({'WARNING'}, "No ShapeKeys existing.") 
            return {'CANCELLED'}         
        basis = obj.data.shape_keys.key_blocks.get("Basis") 
        keys = obj.data.shape_keys.key_blocks 
        removed = 0 
        for key in list(keys): 
            if key.name == "Basis": 
                continue             
            has_delta = any(
                (v.co - basis.data[i].co).length > 1e-6
                for i, v in enumerate(key.data)
            ) 
            if not has_delta: 
                obj.active_shape_key_index = keys.keys().index(key.name) 
                bpy.context.view_layer.objects.active = obj 
                bpy.ops.object.shape_key_remove() 
                removed += 1        
        self.report({'INFO'}, f"{removed} removed empty ShapeKeys.") 
        return {'FINISHED'} 
#endregion

#region class reset values
class OBJECT_OT_reset_deform_settings(bpy.types.Operator): 
    bl_idname = "object.reset_deform_settings" 
    bl_label = "Reset Settings" 
    bl_description = "Set all Deform values back to default" 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context): 
        context.scene.surface_deform_falloff = 4.0 
        context.scene.surface_deform_strength = 1.0 
        self.report({'INFO'}, "Settings reset to default.") 
        return {'FINISHED'}        
#endregion
#region class VertexGroupMix
class OBJECT_OT_combine_vertexgroups(bpy.types.Operator):
    bl_idname = "object.combine_vertexgroups_mix"
    bl_label = "Combine (mix)"
    bl_options = {'REGISTER', 'UNDO'}

    def _get_weight(self, v, group_index):
        for g in v.groups:
            if g.group == group_index:
                return g.weight
        return None
    def _set_weight(self, obj, group_index, vidx, w):
        obj.vertex_groups[group_index].add([vidx], max(0.0, min(1.0, w)), 'REPLACE')

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active Object is no Mesh.")
            return {'CANCELLED'}
        if context.scene.vertex_groups_include_exclude_selector == 'INCLUDE':
            include_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
            exclude_list = []
        else:
            include_list = []
            exclude_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
        target_name = context.scene.vertex_groups_combined_name.strip() or "Combined"
        mix_mode = context.scene.vertex_mix_mode
        mix_set  = context.scene.vertex_mix_set
        normalize = context.scene.vertex_mix_normalize
        def_a = context.scene.vertex_mix_default_a
        def_b = context.scene.vertex_mix_default_b
        groups_to_use = []
        for vg in obj.vertex_groups:
            if include_list and vg.name not in include_list:
                continue
            if exclude_list and vg.name in exclude_list:
                continue
            groups_to_use.append(vg.name)
        if len(groups_to_use) == 0:
            self.report({'WARNING'}, "No Vertex Groups matched the Include/Exclude filter.")
            return {'CANCELLED'}
        if target_name in [vg.name for vg in obj.vertex_groups]:
            obj.vertex_groups.remove(obj.vertex_groups[target_name])
        first_group = groups_to_use[0]
        obj.vertex_groups.active = obj.vertex_groups[first_group]
        bpy.ops.object.vertex_group_copy()
        obj.vertex_groups.active.name = target_name
        vg_target = obj.vertex_groups[target_name]
        idx_target = vg_target.index
        name_to_index = {vg.name: vg.index for vg in obj.vertex_groups}
        def combine(a, b, mode):
            if mode == 'ADD': return a + b
            if mode == 'SUB': return a - b
            if mode == 'MUL': return a * b
            if mode == 'DIV': return a / b if b != 0 else a
            if mode == 'DIF': return abs(a - b)
            if mode == 'AVG': return 0.5 * (a + b)
            if mode == 'MIN': return min(a, b)
            if mode == 'MAX': return max(a, b)
            if mode == 'SET': return b
            return a
        for gname in groups_to_use[1:]:
            if gname not in name_to_index:
                continue
            idx_b = name_to_index[gname]
            for v in obj.data.vertices:
                wA_raw = self._get_weight(v, idx_target)
                wB_raw = self._get_weight(v, idx_b)
                hasA = (wA_raw is not None)
                hasB = (wB_raw is not None)
                affect = (
                    (mix_set == 'ALL') or
                    (mix_set == 'A'   and hasA) or
                    (mix_set == 'B'   and hasB) or
                    (mix_set == 'OR'  and (hasA or hasB)) or
                    (mix_set == 'AND' and (hasA and hasB))
                )
                if not affect:
                    continue
                wA = wA_raw if hasA else def_a
                wB = wB_raw if hasB else def_b
                wC = combine(wA, wB, mix_mode)
                if normalize:
                    wC = max(0.0, min(1.0, wC))
                self._set_weight(obj, idx_target, v.index, wC)
        context.scene.vertex_groups_mask = target_name
        self.report({'INFO'}, f"Combined {len(groups_to_use)} groups into '{target_name}' with mode={mix_mode}, set={mix_set}, normalize={normalize}.")
        return {'FINISHED'}
#endregion
#region Vertex Groups Paste Locked
class OBJECT_OT_vertexgroups_paste_locked(bpy.types.Operator):
    bl_idname = "object.vertexgroups_paste_locked"
    bl_label = "Paste Locked"
    bl_description = "Collect all locked vertex groups on the active mesh and put them into the Exclude field (comma-separated)."
    bl_options = {'REGISTER', 'UNDO'}

    replace: bpy.props.BoolProperty(
        name="Replace Existing",
        description="Replace current Exclude text. If off, append locked names.",
        default=True
    ) # type: ignore

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Active Object is no Mesh.")
            return {'CANCELLED'}
        locked = [vg.name for vg in obj.vertex_groups if getattr(vg, "lock_weight", False)]
        if not locked:
            self.report({'INFO'}, "No locked vertex groups found.")
            return {'CANCELLED'}
        scene = context.scene
        existing = scene.vertex_groups_include_exclude_textfield.strip()
        if self.replace or not existing:
            names = locked
        else:
            current = [n.strip() for n in existing.split(",") if n.strip()]
            names = current + [n for n in locked if n not in current]
        scene.vertex_groups_include_exclude_textfield = ", ".join(names)
        self.report({'INFO'}, f"Excluded {len(locked)} locked groups.")
        return {'FINISHED'}
#endregion

#region class Vertex Groups
class OBJECT_OT_transfer_vertexgroups(bpy.types.Operator):
    bl_idname = "object.transfer_vertexgroups"
    bl_label = "Transfer Vertex Groups"
    bl_description = "Transfers selected Vertex Groups from Source to Active Object using DataTransfer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        source = bpy.data.objects.get(context.scene.surface_deform_source)
        target = context.active_object    
        if not source or not target:
            self.report({'ERROR'}, "Source or Target-Object unavailable.")
            return {'CANCELLED'}    
        if source == target:
            self.report({'ERROR'}, "Source and Target must be different.")
            return {'CANCELLED'}
        if context.scene.vertex_groups_include_exclude_selector == 'INCLUDE':
            include_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
            exclude_list = []
        else:
            include_list = []
            exclude_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
        transferred_count = 0
        for vg in source.vertex_groups:
            if include_list and vg.name not in include_list:
                continue
            if exclude_list and vg.name in exclude_list:
                continue
            mod = target.modifiers.new(name=f"Transfer_{vg.name}", type='DATA_TRANSFER')
            bpy.ops.object.modifier_move_to_index(modifier=mod.name, index=0)
            mod.object = source
            mod.use_vert_data = True
            mod.data_types_verts = {'VGROUP_WEIGHTS'}
            mod.vert_mapping = context.scene.vertex_mapping_method
            mod.layers_vgroup_select_src = vg.name
            mod.layers_vgroup_select_dst = 'NAME'
            mod.mix_mode = 'REPLACE'
            mod.mix_factor = 1.0
            mask_name = context.scene.vertex_groups_mask.strip()
            if mask_name:
                mod.vertex_group = mask_name
                mod.invert_vertex_group = context.scene.vertex_groups_mask_invert
            else:
                mod.vertex_group = ""
                mod.invert_vertex_group = False
            bpy.context.view_layer.objects.active = target
            bpy.ops.object.datalayout_transfer(modifier=mod.name)
            bpy.ops.object.modifier_apply(modifier=mod.name)
            transferred_count += 1
        removed_count = 0
        vgroup_used = {i: False for i, k in enumerate(target.vertex_groups)}
        for v in target.data.vertices:
            for g in v.groups:
                if g.weight > 0.0:
                    vgroup_used[g.group] = True
    
        for i, used in sorted(vgroup_used.items(), reverse=True):
            if not used:
                target.vertex_groups.remove(target.vertex_groups[i])
                removed_count += 1
        self.report({'INFO'}, f"{transferred_count} Vertex Groups transferred. {removed_count} empty groups removed.")
        return {'FINISHED'}
#endregion
#region class Weight Paint Smoothing
class OBJECT_OT_weightpaint_smoothing(bpy.types.Operator):
    bl_idname = "object.weightpaint_smoothing"
    bl_label = "Weight Paint Smoothing"
    bl_description = "Smooths all VertexGroups or based on Include/Exclude."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target = context.active_object
        if context.scene.vertex_groups_include_exclude_selector == 'INCLUDE':
            include_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
            exclude_list = []
        else:
            include_list = []
            exclude_list = [name.strip() for name in context.scene.vertex_groups_include_exclude_textfield.split(",") if name.strip()]
        smoothing_amount = context.scene.weightpaint_smoothing_amount
    
        if not target or target.type != 'MESH':
            self.report({'ERROR'}, "Active Object is no Mesh.")
            return {'CANCELLED'}
    
        original_mode = target.mode
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    
        for i, vg in enumerate(target.vertex_groups):
            if include_list and vg.name not in include_list:
                continue
            if exclude_list and vg.name in exclude_list:
                continue
            target.vertex_groups.active_index = i
            bpy.ops.object.vertex_group_smooth(repeat=smoothing_amount)
    
        bpy.ops.object.mode_set(mode=original_mode)
        self.report({'INFO'}, "Weight Paint smoothed.")
        return {'FINISHED'}
#endregion
#region class FixViewport Display
class OBJECT_OT_FixViewportDisplay(bpy.types.Operator): 
    bl_idname = "object.fix_viewport_display" 
    bl_label = "Fix Viewport Display" 
    bl_description = "Fixes the Viewport Display to have the Bones always be in front and display as wired." 
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context): 
        obj = context.object
        armature = None
        settings = [s.strip() for s in context.scene.viewportdisplay_settings.split(",")]
        show_flags = {
            "show_in_front": "show_in_front",
            "show_axis": "show_axis",
            "show_name": "show_name"
        }
        used_display_type = {
            "wire": 'WIRE',
            "solid": 'SOLID',
            "textured": 'TEXTURED',
            "bounds": 'BOUNDS',
            "bounds_sphere": 'BOUNDS'
        }
        used_display_bounds = {
            "box": 'BOX',
            "sphere": 'SPHERE',
            "cylinder": 'CYLINDER',
            "cone": 'CONE',
            "capsule": 'CAPSULE'
        }
        if obj and obj.type == 'ARMATURE':
            armature = obj
        elif obj and obj.type == 'MESH':
            if obj.parent and obj.parent.type == 'ARMATURE':
                armature = obj.parent
            else:
                for mod in obj.modifiers:
                    if mod.type == 'ARMATURE' and mod.object:
                        armature = mod.object
                        break
        elif context.pose_object and context.pose_object.type == 'ARMATURE':
            armature = context.pose_object
        if armature:
            for key, attr in show_flags.items():
                setattr(armature, attr, key in settings)
            for key in reversed(settings):
                if key in used_display_type:
                    armature.display_type = used_display_type[key]
                    break
            else: 
                armature.display_type = "TEXTURED"
            for key in reversed(settings):
                if key in used_display_bounds:
                    armature.display_bounds_type = used_display_bounds[key]
                    armature.show_bounds = True
                    break
            else:
                armature.show_bounds = False
            self.report({'INFO'}, f"Viewport Display fixed for: {armature.name}")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Keine Armature gefunden.")
            return {'CANCELLED'}
#endregion
#region class surface deform PANEL (Draw)
class OBJECT_PT_surface_deform_panel(bpy.types.Panel): 
    bl_label = "AkooToolbox" 
    bl_idname = "OBJECT_PT_surface_deform_panel" 
    bl_space_type = 'VIEW_3D' 
    bl_region_type = 'UI' 
    bl_category = 'AkooToolbox' 

    # Start - def draw
    def draw(self, context): 
        layout = self.layout 
        scene = context.scene
        # R-Start - Show/Hide source Region
        layout.prop(scene, "show_source_region", icon="TRIA_DOWN" if scene.show_source_region else "TRIA_RIGHT", emboss=False)
        if scene.show_source_region:
            box = layout.box()
            box.label(text="Select SOURCE MESH to copy from", icon="INFO")
            box.prop(context.scene, "surface_deform_source", text="", icon="MESH_CUBE") 
            box.separator()
        # R-End - Show/Hide Source Region
        # R-Start - Show/Hide Shapekey Region (Surface Deform)
        layout.prop(scene, "show_shapekey_region", icon="TRIA_DOWN" if scene.show_shapekey_region else "TRIA_RIGHT", emboss=False)
        if scene.show_shapekey_region:
            box = layout.box()
            box.label(text="Use Comma to separate! (Butt+, Hip+, Breast-, etc.)", icon="INFO")
            col = box.column(align=True)
            col.prop(context.scene, "surface_deform_include_exclude_selector", text="", icon="FORCE_CHARGE")
            col.prop(context.scene, "surface_deform_include_exclude_textfield", text="")
            col.operator("object.shapekeys_paste_locked", text="Paste Locked", icon="PASTEDOWN")
            box.separator() 
            Shapekey_Setting = box.row(align=True)
            Shapekey_Setting.prop(context.scene, "surface_deform_falloff", text="Falloff") 
            Shapekey_Setting.prop(context.scene, "surface_deform_strength", text="Strength") 
            Shapekey_Setting.operator("object.reset_deform_settings", icon="LOOP_BACK") 
            scene = context.scene 
            box.separator() 
            box.label(text="Select TARGET MESH before deforming", icon="INFO") 
            Shapekey_Btn = box.row(align=True)
            Shapekey_Btn.operator("object.surface_deform_with_shapes", icon="SHAPEKEY_DATA") 
            Shapekey_Btn.operator("object.remove_empty_shapekeys", icon="BRUSH_DATA")
            box.separator() 
        # R-Start - Show/Hide VertexGroups Region
        layout.prop(scene, "show_vertexgroups_region", icon="TRIA_DOWN" if scene.show_vertexgroups_region else "TRIA_RIGHT", emboss=False)
        if scene.show_vertexgroups_region:
            box = layout.box()
            box.label(text="Use Comma to separate! (Hips, Spine, Chest, etc.)", icon="INFO")
            col = box.column(align=True)
            col.prop(context.scene, "vertex_groups_include_exclude_selector", text="", icon="FORCE_CHARGE")
            col.prop(context.scene, "vertex_groups_include_exclude_textfield", text="")
            col.operator("object.vertexgroups_paste_locked", text="Paste Locked", icon="PASTEDOWN")
            box.separator()
            box.label(text="Combine groups using VertexWeightMix", icon="INFO")
            set_box = box.box()
            set_box.label(text="Mix Settings")
            r1 = set_box.row(align=True)
            r1.prop(context.scene, "vertex_mix_mode", text="Mode")
            r1.prop(context.scene, "vertex_mix_set", text="Affect")
            r2 = set_box.row(align=True)
            r2.prop(context.scene, "vertex_mix_normalize", text="Normalize")
            r3 = set_box.row(align=True)
            r3.prop(context.scene, "vertex_mix_default_a")
            r3.prop(context.scene, "vertex_mix_default_b")
            row = box.row(align=True)
            row.prop(context.scene, "vertex_groups_combined_name", text="Target Group")
            row.operator("object.combine_vertexgroups_mix", text="Combine (mix)", icon="GROUP_VERTEX")
            mask_row = box.row(align=True)
            mask_row.prop(context.scene, "vertex_groups_mask", text="Mask")
            mask_row.prop(context.scene, "vertex_groups_mask_invert", text="Invert")
            box.separator()
            box.label(text="Select Mapping Method:", icon="INFO")
            box.prop(context.scene, "vertex_mapping_method", icon="MOD_DATA_TRANSFER", text="")
            box.separator()
            box.label(text="Make sure to have the target selected!", icon="INFO") 
            box.operator("object.transfer_vertexgroups", icon="GROUP_VERTEX")
            box.separator() 
            box.label(text="Make sure to use Include/Exclude to not smooth all VertexGroups!", icon="INFO")
            Smooth = box.row(align=True)
            Smooth.prop(context.scene, "weightpaint_smoothing_amount", text="Iterations")
            Smooth.operator("object.weightpaint_smoothing", text="Smooth", icon="MOD_SMOOTH")
        # R-End - Show/Hide VertexGroups Region
        # R-Start - Show/Hide Viewport Display Region
        layout.prop(scene, "show_viewportdisplay_region", icon="TRIA_DOWN" if scene.show_viewportdisplay_region else "TRIA_RIGHT", emboss=False)
        if scene.show_viewportdisplay_region:
            box = layout.box()
            box.label(text="Use Comma to separate! (show_name, show_in_front, solid, box, etc.) more info hover over field", icon="INFO")
            box.prop(context.scene, "viewportdisplay_settings", text="")
            box.operator("object.fix_viewport_display", icon="VIEW3D")
            box.separator() 
        # R-End - Show/Hide Viewport Display Region
        # R-Start - Show/Hide Save Region
        layout.prop(scene, "show_save_region", icon="TRIA_DOWN" if scene.show_save_region else "TRIA_RIGHT", emboss=False)
        if scene.show_save_region:
            box = layout.box()
            box.label(text="Saves and restores settings across Blender sessions", icon="INFO")
            box.operator("object.save_settings", icon="FILE_TICK")
            box.separator()
            box.label(text="Lets you create Presets of your current settings", icon="INFO")
            box.prop(scene, "akoopreset_list", text="", icon="TAG")
            row = box.row(align=True)
            row.operator("object.load_akoopreset", text="Load", icon="FILE_FOLDER")
            row.operator("object.save_akoopreset", text="Save/Create", icon="FILE_TICK")
            row.operator("object.delete_akoopreset", text="Delete", icon="X")
            box.prop(scene, "akoopreset_newname", text="New Preset Name")
            box.separator()
        # R-End - Show/Hide Save Region
    # End - def draw
#endregion

#region def register
def register(): 
    # R-Start - Save Region
    bpy.types.Scene.show_save_region = bpy.props.BoolProperty(
        name="Show Save Region",
        description="Expand to show save options",
        default=True
    )
    saved_data = load_user_data()
    bpy.types.Scene.akoopreset_list = bpy.props.EnumProperty(
        name="Presets",
        description="Select preset",
        items=lambda self, context: [(k, k, "") for k in load_presets().keys()]
    )
    bpy.types.Scene.akoopreset_newname = bpy.props.StringProperty(
        name="Preset Name",
        description="Name of new preset to save"
    )
    bpy.utils.register_class(OBJECT_OT_save_akoopreset)
    bpy.utils.register_class(OBJECT_OT_load_akoopreset)
    bpy.utils.register_class(OBJECT_OT_delete_akoopreset)
    # R-End - Save Region
    # R-Start - Source Region
    bpy.types.Scene.show_source_region = bpy.props.BoolProperty(
        name="Show Source Region",
        description="Expand to show deform options",
        default=True
    )
    #saved_sourcemesh = saved_data.get("last_source_object")
    bpy.types.Scene.surface_deform_source = bpy.props.EnumProperty(
        name="Source Mesh",
        description="Object with ShapeKeys",
        items=get_mesh_objects,
        default=None
    )
    bpy.utils.register_class(OBJECT_OT_save_settings)
    # R-End - Main Region
    # R-Start - Shapekey Region
    bpy.types.Scene.show_shapekey_region = bpy.props.BoolProperty(
        name="Show Shapekey Region",
        description="Expand to show shapekey options",
        default=False
    )
    bpy.utils.register_class(OBJECT_OT_surface_deform_with_shapes) 
    bpy.utils.register_class(OBJECT_OT_remove_empty_shapekeys) 
    bpy.utils.register_class(OBJECT_PT_surface_deform_panel) 
    saved_include_exclude_textfield_shapekey = saved_data.get("last_include_exclude_textfield_shapekeys_object")
    #saved_include_shapekey = saved_data.get("last_include_shapekeys_object")
    #saved_exclude_shapekey = saved_data.get("last_exclude_shapekeys_object")
    bpy.types.Scene.surface_deform_include_exclude_selector = bpy.props.EnumProperty(
        name="Include/Exclude Mode",
        description="Choose whether to use Include or Exclude list (Include has priority).",
        items=[
            ('INCLUDE', "Include", "Use the Include list (if not empty)"),
            ('EXCLUDE', "Exclude", "Use the Exclude list (if Include is empty)"),
        ]
    )
    bpy.types.Scene.surface_deform_include_exclude_textfield = bpy.props.StringProperty(
        name="Include/Exclude TextField",
        description="Comma-separated list of ShapeKeys to include (leave blank to include all).",
        default=saved_include_exclude_textfield_shapekey if saved_include_exclude_textfield_shapekey else "",
    ) 
    #bpy.types.Scene.surface_deform_include = bpy.props.StringProperty(
    #    name="Include ShapeKeys",
    #    description="Comma-separated list of ShapeKeys to include (leave blank to include all).",
    #    default=saved_include_shapekey if saved_include_shapekey else ""
    #) 
    #bpy.types.Scene.surface_deform_exclude = bpy.props.StringProperty(
    #    name="Exclude ShapeKeys",
    #    description="Comma-separated list of ShapeKeys to exclude.",
    #    default=saved_exclude_shapekey if saved_exclude_shapekey else ""
    #) 
    saved_falloff_shapekey = saved_data.get("last_surface_deform_falloff_object")
    saved_strength_shapekey = saved_data.get("last_surface_deform_strength_object")
    bpy.types.Scene.surface_deform_falloff = bpy.props.FloatProperty(
        name="Interpolation Falloff",
        default=saved_falloff_shapekey if saved_falloff_shapekey else 4.0,
        min=0.0,
        max=100.0
    )
    bpy.types.Scene.surface_deform_strength = bpy.props.FloatProperty(
        name="Strength",
        default=saved_strength_shapekey if saved_strength_shapekey else 1.0,
        min=0.0,
        max=1.0
    ) 
    bpy.utils.register_class(OBJECT_OT_reset_deform_settings) 
    # R-Start - Paste Locked Shapekeys
    bpy.utils.register_class(OBJECT_OT_shapekeys_paste_locked)
    # R-End - Paste Locked Shapekeys
    # R-End - Shapekey Region
    # R-Start - VertexGroups Region
    bpy.types.Scene.show_vertexgroups_region = bpy.props.BoolProperty(
        name="VertexGroups Region",
        description="Expand to show vertexgroups options",
        default=False
    )
    # Load saved include/exclude for VertexGroups from AkooToolbox_config.json
    saved_include_exclude_textfield_vertexgroups = saved_data.get("last_include_vertex_groups_object")
    bpy.types.Scene.vertex_groups_include_exclude_selector = bpy.props.EnumProperty(
    name="Include/Exclude Mode",
    description="Choose whether to use Include or Exclude list (Include has priority).",
    items=[
        ('INCLUDE', "Include", "Use the Include list (if not empty)"),
        ('EXCLUDE', "Exclude", "Use the Exclude list (if Include is empty)"),
    ]
    )
    bpy.types.Scene.vertex_groups_include_exclude_textfield = bpy.props.StringProperty(
        name="Include/Exclude TextField",
        description="Comma-separated list of ShapeKeys to include (leave blank to include all).",
        default=saved_include_exclude_textfield_vertexgroups if saved_include_exclude_textfield_vertexgroups else "",
    ) 
    #bpy.types.Scene.vertex_groups_include = bpy.props.StringProperty(
    #    name="Include VertexGroups",
    #    description="Comma-separated list of VertexGroups to include (leave blank to include all).",
    #    default=saved_include_vertex_groups if saved_include_vertex_groups else ""
    #) 
    #bpy.types.Scene.vertex_groups_exclude = bpy.props.StringProperty(
    #    name="Exclude VertexGroups",
    #    description="Comma-separated list of VertexGroups to exclude.",
    #    default=saved_exclude_vertex_groups if saved_exclude_vertex_groups else ""
    #) 
    # Load saved mapping for VertexGroups from AkooToolbox_config.json
    saved_mapping_vertex_groups = saved_data.get("last_mapping_vertex_groups_object")
    bpy.types.Scene.vertex_mapping_method = bpy.props.EnumProperty(
    name="Mapping",
    description="Choose the mapping method for Data Transfer",
    items=[
        ('TOPOLOGY', "Topology", ""),
        ('NEAREST', "Nearest Vertex", ""),
        ('EDGE_NEAREST', "Nearest Edge Vertex", ""),
        ('EDGEINTERP_NEAREST', "Nearest Edge Interpolated", ""),
        ('POLY_NEAREST', "Nearest Face Vertex", ""),
        ('POLYINTERP_NEAREST', "Nearest Face Interpolated", ""),
        ('POLYINTERP_VNORPROJ', "Projected Face Interpolated", ""),
    ],
    default=saved_mapping_vertex_groups if saved_mapping_vertex_groups else 'POLYINTERP_NEAREST'
)
    bpy.utils.register_class(OBJECT_OT_transfer_vertexgroups)
    saved_weightpaint_smoothing_amount = saved_data.get("last_weightpaint_smoothing_amount_object")
    bpy.types.Scene.weightpaint_smoothing_amount = bpy.props.IntProperty(
        name="Smoothing Iterations",
        description="Number of smoothing iterations for Weight Paint",
        default=saved_weightpaint_smoothing_amount if saved_weightpaint_smoothing_amount else 2,
        min=1,
        max=10
    )
    bpy.utils.register_class(OBJECT_OT_weightpaint_smoothing)
    # R-End - VertexGroups Region
    # R-Start - Viewport Display Region
    bpy.types.Scene.show_viewportdisplay_region = bpy.props.BoolProperty(
        name="ViewportDisplay Region",
        description="Expand to show viewportdisplay options",
        default=True
    )
    # Load saved data for ViewportDisplay from AkooToolbox_config.json
    saved_viewportdisplay_settings = saved_data.get("last_viewportdisplay_settings_object")
    bpy.types.Scene.viewportdisplay_settings = bpy.props.StringProperty(
        name="ViewportDisplay Settings",
        description="ALL OPTIONS: show_name, show_axis, show_in_front, bounds or wire or solid or textured, box or sphere or cylinder or cone or capsule",
        default=saved_viewportdisplay_settings if saved_viewportdisplay_settings else ""
    ) 
    bpy.utils.register_class(OBJECT_OT_FixViewportDisplay)
    # R-End - Viewport Display Region
    # R-Start - VertexGroupMix
    bpy.types.Scene.vertex_groups_combined_name = bpy.props.StringProperty(
        name="Target Group",
        description="Name of the combined vertex group that will receive the mixed weights.",
        default="Combined"
    )
    bpy.utils.register_class(OBJECT_OT_combine_vertexgroups)
    bpy.types.Scene.vertex_mix_mode = bpy.props.EnumProperty(
        name="Mode",
        description="VertexWeightMix mode (how A and B are combined)",
        items=[
            ('ADD', 'Add', 'A + B'),
            ('SUB', 'Subtract', 'A - B'),
            ('MUL', 'Multiply', 'A * B'),
            ('DIV', 'Divide', 'A / B'),
            ('DIF', 'Difference', '|A - B|'),
            ('AVG', 'Average', '(A + B) / 2'),
            ('MIN', 'Minimum', 'min(A, B)'),
            ('MAX', 'Maximum', 'max(A, B)'),
            ('SET', 'Replace', 'Set A to B'),
        ],
        default='ADD'
    )
    bpy.types.Scene.vertex_mix_set = bpy.props.EnumProperty(
        name="Affect",
        description="Which vertices to affect when mixing",
        items=[
            ('A',   'Only A',    'Only vertices existing in group A'),
            ('B',   'Only B',    'Only vertices existing in group B'),
            ('OR',  'A or B',    'Vertices in A or B'),
            ('AND', 'A and B',   'Vertices in both A and B'),
            ('ALL', 'All',       'All vertices'),
        ],
        default='ALL'
    )
    bpy.types.Scene.vertex_mix_normalize = bpy.props.BoolProperty(
        name="Normalize",
        description="Normalize weights to 0..1 after mixing",
        default=False
    )
    bpy.types.Scene.vertex_mix_default_a = bpy.props.FloatProperty(
        name="Default A",
        description="Default weight for vertices missing in group A",
        min=0.0, max=1.0, default=0.0
    )
    bpy.types.Scene.vertex_mix_default_b = bpy.props.FloatProperty(
        name="Default B",
        description="Default weight for vertices missing in group B",
        min=0.0, max=1.0, default=0.0
    )
    # R-End - VertexGroupMix
    # R-Start - Vertex Groups Paste Locked
    bpy.utils.register_class(OBJECT_OT_vertexgroups_paste_locked)
    # R-End - Vertex Groups Paste Locked
    bpy.types.Scene.vertex_groups_mask = bpy.props.StringProperty(
    # R-Start - Vertex Group Mask
    name="Vertex Group Mask",
    description="Optional vertex group name to limit affected areas during Vertex Group transfer.",
    default=""
    )
    bpy.types.Scene.vertex_groups_mask_invert = bpy.props.BoolProperty(
        name="Invert",
        description="Invert the vertex group mask.",
        default=True
    )
    # R-End - Vertex Group Mask
#endregion

#region def unregister
def unregister(): 
    
    bpy.types.Scene.akoopreset_list = bpy.props.EnumProperty(
        name="Presets",
        description="Select preset",
        items=lambda self, context: [(k, k, "") for k in load_presets().keys()]
    )
    bpy.types.Scene.akoopreset_newname = bpy.props.StringProperty(
        name="Preset Name",
        description="Name of new preset to save"
    )
    bpy.utils.register_class(OBJECT_OT_save_akoopreset)
    bpy.utils.register_class(OBJECT_OT_load_akoopreset)
    bpy.utils.register_class(OBJECT_OT_delete_akoopreset)
    # R-Start - Source Region
    del bpy.types.Scene.show_source_region
    del bpy.types.Scene.show_save_region
    del bpy.types.Scene.surface_deform_source 
    bpy.utils.unregister_class(OBJECT_OT_save_settings) 
    # R-End - Source Region
    # R-Start - Shapekey Region
    del bpy.types.Scene.show_shapekey_region
    bpy.utils.unregister_class(OBJECT_OT_surface_deform_with_shapes) 
    bpy.utils.unregister_class(OBJECT_OT_remove_empty_shapekeys) 
    bpy.utils.unregister_class(OBJECT_PT_surface_deform_panel)  
    del bpy.types.Scene.surface_deform_include_exclude_selector
    del bpy.types.Scene.surface_deform_include_exclude_textfield
    #del bpy.types.Scene.surface_deform_include 
    #del bpy.types.Scene.surface_deform_exclude
    del bpy.types.Scene.surface_deform_falloff
    del bpy.types.Scene.surface_deform_strength
    bpy.utils.unregister_class(OBJECT_OT_reset_deform_settings) 
    # R-Start - Paste locked Shapekeys
    bpy.utils.unregister_class(OBJECT_OT_shapekeys_paste_locked)
    # R-End - Paste locked Shapekeys
    # R-End - Shapekey Region
    # R-Start - VertexGroups Region
    del bpy.types.Scene.show_vertexgroups_region
    del bpy.types.Scene.vertex_groups_include
    del bpy.types.Scene.vertex_groups_exclude
    del bpy.types.Scene.vertex_mapping_method
    bpy.utils.unregister_class(OBJECT_OT_transfer_vertexgroups)
    del bpy.types.Scene.weightpaint_smoothing_amount
    bpy.utils.unregister_class(OBJECT_OT_weightpaint_smoothing)
    # R-End - VertexGroups Region
    # R-Start - Viewport Display Region 
    del bpy.types.Scene.show_viewportdisplay_region
    del bpy.types.Scene.viewportdisplay_settings
    bpy.utils.unregister_class(OBJECT_OT_FixViewportDisplay)
    # R-End - Viewport Display Region
    # R-Start - VertexGroupMix
    del bpy.types.Scene.vertex_groups_combined_name
    bpy.utils.unregister_class(OBJECT_OT_combine_vertexgroups)
    del bpy.types.Scene.vertex_mix_mode
    del bpy.types.Scene.vertex_mix_set
    del bpy.types.Scene.vertex_mix_normalize
    del bpy.types.Scene.vertex_mix_default_a
    del bpy.types.Scene.vertex_mix_default_b
    # R-End - VertexGroupMix
    # R-Start - Vertex Groups Paste Locked
    bpy.utils.unregister_class(OBJECT_OT_vertexgroups_paste_locked)
    # R-End - Vertex Groups Paste Locked
    # R-Start - Vertex Group Mask
    del bpy.types.Scene.vertex_groups_mask
    del bpy.types.Scene.vertex_groups_mask_invert
    # R-End - Vertex Group Mask
#endregion

if __name__ == "__main__": 
    register() 

