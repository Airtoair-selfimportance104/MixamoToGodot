bl_info = {
    "name": "Mixamo to Godot",
    "author": "bogdanMerkulow",
    "version": (2, 3, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Mixamo",
    "description": "Import Mixamo FBX animations and add Root bone for Godot root motion",
    "category": "Animation",
}

import bpy
import os
import re
from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup, Operator, Panel


def to_pascal_case(name):
    words = re.split(r'[\s_\-\.]+', name)
    return ''.join(w.capitalize() for w in words if w)


def find_armature(context):
    armature = context.active_object
    if armature is None or armature.type != 'ARMATURE':
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                armature = obj
                break
    return armature


def get_fcurves(action):
    if hasattr(action, 'fcurves'):
        try:
            iter(action.fcurves)
            return action.fcurves
        except (TypeError, AttributeError):
            pass
    if hasattr(action, 'layers'):
        for layer in action.layers:
            for strip in layer.strips:
                if hasattr(strip, 'channelbags'):
                    for cb in strip.channelbags:
                        if hasattr(cb, 'fcurves'):
                            return cb.fcurves
    return None


def read_fcurve_data(fc):
    data = []
    for kp in fc.keyframe_points:
        data.append((
            kp.co.x, kp.co.y,
            kp.interpolation,
            kp.handle_left.copy(), kp.handle_right.copy(),
            kp.handle_left_type, kp.handle_right_type,
        ))
    return data


def scale_location_fcurves(fcurves, factor):
    for fc in list(fcurves):
        if '.location' in fc.data_path:
            for kp in fc.keyframe_points:
                kp.co.y *= factor
                kp.handle_left.y *= factor
                kp.handle_right.y *= factor


def create_fcurve(action, armature, data_path, index, group_name=""):
    """Create a new fcurve. Tries multiple APIs for Blender 3.x through 5.x."""

    # Method 1: Blender 5.0+ — action.fcurve_ensure_for_datablock
    # Requires action to be assigned to armature first!
    if hasattr(action, 'fcurve_ensure_for_datablock'):
        try:
            fc = action.fcurve_ensure_for_datablock(
                datablock=armature,
                data_path=data_path,
                index=index,
                group_name=group_name,
            )
            if fc is not None:
                return fc
        except Exception:
            pass

    # Method 2: Blender 3.x/4.x — action.fcurves.new
    if hasattr(action, 'fcurves') and hasattr(action.fcurves, 'new'):
        try:
            fc = action.fcurves.new(data_path, index=index, action_group=group_name)
            if fc is not None:
                return fc
        except Exception:
            pass

    return None


class MixamoProperties(PropertyGroup):
    fbx_folder: StringProperty(
        name="FBX Folder",
        description="Folder containing Mixamo FBX files",
        default="",
        subtype='DIR_PATH',
    )
    hips_bone: StringProperty(
        name="Hips Bone",
        description="Name of the Hips bone in the Mixamo rig",
        default="mixamorig:Hips",
    )


class MIXAMO_OT_import(Operator):
    bl_idname = "mixamo.import_fbx"
    bl_label = "Import All FBX"
    bl_description = "Import all FBX files from the selected folder"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.mixamo_props
        folder = bpy.path.abspath(props.fbx_folder)

        if not folder or not os.path.isdir(folder):
            self.report({'ERROR'}, f"Invalid folder: {folder}")
            return {'CANCELLED'}

        count = 0
        for filename in sorted(os.listdir(folder)):
            if filename.lower().endswith('.fbx'):
                filepath = os.path.join(folder, filename)
                actions_before = set(bpy.data.actions)
                bpy.ops.import_scene.fbx(filepath=filepath)
                anim_name = to_pascal_case(os.path.splitext(filename)[0])
                new_actions = set(bpy.data.actions) - actions_before
                if len(new_actions) == 1:
                    new_actions.pop().name = anim_name
                else:
                    for i, act in enumerate(new_actions):
                        act.name = f"{anim_name}_{i}" if len(new_actions) > 1 else anim_name
                count += 1

        self.report({'INFO'}, f"Imported {count} FBX files, {len(bpy.data.actions)} actions total")
        return {'FINISHED'}


class MIXAMO_OT_fix_root(Operator):
    bl_idname = "mixamo.fix_root"
    bl_label = "Fix Root Motion"
    bl_description = "Add Root bone, apply transforms, scale fcurves, transfer Hips motion to Root"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.mixamo_props
        hips_name = props.hips_bone
        prefix = hips_name.split(":")[0] + ":" if ":" in hips_name else ""
        root_bone_name = prefix + "Root"

        armature = find_armature(context)
        if armature is None:
            self.report({'ERROR'}, "No armature found. Import FBX first.")
            return {'CANCELLED'}

        context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        if armature.data.edit_bones.get(root_bone_name):
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'WARNING'}, f"'{root_bone_name}' already exists, skipping")
            return {'CANCELLED'}

        hips = armature.data.edit_bones.get(hips_name)
        if hips is None:
            available = [b.name for b in armature.data.edit_bones]
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'ERROR'}, f"Bone '{hips_name}' not found. Available: {', '.join(available)}")
            return {'CANCELLED'}

        root = armature.data.edit_bones.new(root_bone_name)
        root.head = (0, 0, 0)
        root.tail = (0, 30, 0)
        hips.parent = root
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(True)
        context.view_layer.objects.active = armature
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        if not armature.animation_data:
            armature.animation_data_create()

        fixed = 0
        for action in bpy.data.actions:
            fcurves = get_fcurves(action)
            if fcurves is None:
                continue

            hips_path = f'pose.bones["{hips_name}"].location'
            hips_loc = [fc for fc in fcurves if fc.data_path == hips_path]
            if not hips_loc:
                continue

            # Assign action to armature (required for fcurve_ensure_for_datablock)
            armature.animation_data.action = action
            if hasattr(armature.animation_data, 'action_suitable_slots'):
                suitable = armature.animation_data.action_suitable_slots
                if len(suitable) > 0:
                    armature.animation_data.action_slot = suitable[0]
                elif hasattr(action, 'slots') and len(action.slots) > 0:
                    armature.animation_data.action_slot = action.slots[0]

            # Scale location fcurves (cm -> m after transform_apply)
            scale_location_fcurves(fcurves, 0.01)

            # Read Hips keyframe data (already scaled)
            hips_data = {}
            for fc in hips_loc:
                hips_data[fc.array_index] = read_fcurve_data(fc)

            # Create Root fcurves and populate with Hips data
            root_path = f'pose.bones["{root_bone_name}"].location'
            root_fcs = {}
            for axis_idx, keyframes in hips_data.items():
                fc = create_fcurve(action, armature, root_path, axis_idx, root_bone_name)
                if fc is None:
                    continue
                fc.keyframe_points.add(len(keyframes))
                for i, (frame, value, interp, hl, hr, hlt, hrt) in enumerate(keyframes):
                    kp = fc.keyframe_points[i]
                    kp.co = (frame, value)
                    kp.interpolation = interp
                    kp.handle_left = hl
                    kp.handle_right = hr
                    kp.handle_left_type = hlt
                    kp.handle_right_type = hrt
                root_fcs[axis_idx] = fc

            # Clamp Root Y >= 0
            if 1 in root_fcs:
                for kp in root_fcs[1].keyframe_points:
                    if kp.co.y < 0:
                        kp.co.y = 0

            # Remove Hips X and Z (keep only Y)
            fcurves = get_fcurves(action)
            hips_loc = [fc for fc in fcurves if fc.data_path == hips_path]
            for fc in [f for f in hips_loc if f.array_index != 1]:
                fcurves.remove(fc)

            # Clamp Hips Y <= 0
            hips_y = [fc for fc in fcurves
                       if fc.data_path == hips_path and fc.array_index == 1]
            for fc in hips_y:
                for kp in fc.keyframe_points:
                    if kp.co.y > 0:
                        kp.co.y = 0

            fixed += 1

        armature.animation_data.action = None

        self.report({'INFO'}, f"Root motion fixed for {fixed}/{len(bpy.data.actions)} actions")
        return {'FINISHED'}


class MIXAMO_OT_merge_clean(Operator):
    bl_idname = "mixamo.merge_clean"
    bl_label = "Merge & Clean"
    bl_description = "Keep armature with mesh, push actions to NLA, delete extras"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        main_armature = None
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                if any(child.type == 'MESH' for child in obj.children):
                    main_armature = obj
                    break

        if main_armature is None:
            self.report({'ERROR'}, "No armature with mesh found")
            return {'CANCELLED'}

        to_delete = []
        for obj in bpy.data.objects:
            if obj == main_armature:
                continue
            if obj in main_armature.children_recursive:
                continue
            if obj.parent == main_armature:
                continue
            to_delete.append(obj)

        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for obj in to_delete:
            obj.select_set(True)
        bpy.ops.object.delete()

        for mesh in bpy.data.meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)
        for arm in bpy.data.armatures:
            if arm.users == 0:
                bpy.data.armatures.remove(arm)

        context.view_layer.objects.active = main_armature
        main_armature.select_set(True)

        if not main_armature.animation_data:
            main_armature.animation_data_create()
        anim_data = main_armature.animation_data

        pushed = 0
        for action in bpy.data.actions:
            already_pushed = False
            for track in anim_data.nla_tracks:
                for strip in track.strips:
                    if strip.action == action:
                        already_pushed = True
                        break
                if already_pushed:
                    break
            if already_pushed:
                continue

            track = anim_data.nla_tracks.new()
            track.name = action.name
            start_frame = int(action.frame_range[0])
            strip = track.strips.new(action.name, start_frame, action)
            strip.name = action.name
            pushed += 1

        anim_data.action = None

        self.report({'INFO'},
            f"Kept '{main_armature.name}'. Pushed {pushed} actions to NLA. "
            f"Deleted {len(to_delete)} objects")
        return {'FINISHED'}


class MIXAMO_OT_do_all(Operator):
    bl_idname = "mixamo.do_all"
    bl_label = "Import + Fix + Merge"
    bl_description = "Import all FBX, merge into skinned character, fix root motion, push to NLA"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        result = bpy.ops.mixamo.import_fbx()
        if result != {'FINISHED'}:
            return result

        result = bpy.ops.mixamo.merge_clean()
        if result != {'FINISHED'}:
            return result

        result = bpy.ops.mixamo.fix_root()
        if result != {'FINISHED'}:
            return result

        self.report({'INFO'}, "Import + Fix + Merge complete!")
        return {'FINISHED'}


class MIXAMO_PT_panel(Panel):
    bl_label = "Mixamo to Godot"
    bl_idname = "MIXAMO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Mixamo"

    def draw(self, context):
        layout = self.layout
        props = context.scene.mixamo_props

        layout.prop(props, "fbx_folder")
        layout.prop(props, "hips_bone")

        layout.separator()
        layout.operator("mixamo.import_fbx", icon='IMPORT')
        layout.operator("mixamo.merge_clean", icon='TRASH')
        layout.operator("mixamo.fix_root", icon='BONE_DATA')

        layout.separator()
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mixamo.do_all", icon='PLAY')


classes = (
    MixamoProperties,
    MIXAMO_OT_import,
    MIXAMO_OT_merge_clean,
    MIXAMO_OT_fix_root,
    MIXAMO_OT_do_all,
    MIXAMO_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mixamo_props = PointerProperty(type=MixamoProperties)


def unregister():
    del bpy.types.Scene.mixamo_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
