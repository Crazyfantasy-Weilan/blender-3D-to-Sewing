import bpy
from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)


class QuickClothsim(Operator):
    """为选中物体添加缝纫纸样布料模拟设置"""
    bl_idname = "object.sewing_pattern_clothsim"
    bl_label = "布料模拟设置"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None:
            return False
        try:
            return obj.type == 'MESH'
        except:
            return False

    use_sewing: BoolProperty(
        name="启用缝合",
        description="启用形状 > 缝合弹簧",
        default=True,
    )
    sewing_force: FloatProperty(
        name="最大缝合力",
        description="最大缝合弹簧力",
        default=5.0,
        min=0.0,
        max=100.0,
    )
    sewing_max_dist: FloatProperty(
        name="最大缝合距离",
        description="缝合弹簧的最大作用距离",
        default=5.0,
        min=0.0,
        max=100.0,
    )
    use_pressure: BoolProperty(
        name="启用压力",
        description="启用压力以充气网格",
        default=True,
    )
    pressure_force: FloatProperty(
        name="压力值",
        description="均匀压力值",
        default=5.0,
        min=0.0,
        max=500.0,
    )
    use_gravity: BoolProperty(
        name="启用重力",
        description="使用世界重力",
        default=False,
    )
    air_damping: FloatProperty(
        name="空气粘度",
        description="空气阻尼。当物体塌陷时增加此值",
        default=10.0,
        min=0.0,
        max=100.0,
    )
    quality: IntProperty(
        name="质量步数",
        description="布料模拟质量步数",
        default=10,
        min=1,
        max=80,
    )
    mass: FloatProperty(
        name="质量",
        description="布料材质质量 (kg)",
        default=0.3,
        min=0.001,
        max=100.0,
    )
    time_scale: FloatProperty(
        name="倍增速率",
        description="布料模拟的时间缩放",
        default=1.0,
        min=0.01,
        max=10.0,
    )
    tension_stiffness: FloatProperty(
        name="张力硬度",
        description="布料的张力硬度",
        default=0.3,
        min=0.0,
        max=1000.0,
    )
    compression_stiffness: FloatProperty(
        name="压缩硬度",
        description="布料的压缩硬度",
        default=0.0,
        min=0.0,
        max=1000.0,
    )
    shear_stiffness: FloatProperty(
        name="切变硬度",
        description="布料的切变硬度",
        default=5.0,
        min=0.0,
        max=1000.0,
    )
    bending_stiffness: FloatProperty(
        name="弯曲硬度",
        description="布料的弯曲硬度",
        default=0.5,
        min=0.0,
        max=1000.0,
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=350)

    def draw(self, context):
        layout = self.layout
        
        # 缝合设置
        box = layout.box()
        box.label(text="缝合设置", icon='MOD_CLOTH')
        box.prop(self, "use_sewing")
        if self.use_sewing:
            box.prop(self, "sewing_force")
            box.prop(self, "sewing_max_dist")
        
        # 压力设置
        box = layout.box()
        box.label(text="压力 / 充气", icon='FORCE_FORCE')
        box.prop(self, "use_pressure")
        if self.use_pressure:
            box.prop(self, "pressure_force")
        
        # 物理设置
        box = layout.box()
        box.label(text="物理设置", icon='PHYSICS')
        box.prop(self, "use_gravity")
        box.prop(self, "air_damping")
        box.prop(self, "quality")
        box.prop(self, "mass")
        box.prop(self, "time_scale")
        
        # 硬度设置
        box = layout.box()
        box.label(text="硬度设置", icon='SNAP_FACE')
        box.prop(self, "tension_stiffness")
        box.prop(self, "compression_stiffness")
        box.prop(self, "shear_stiffness")
        box.prop(self, "bending_stiffness")

    def execute(self, context):
        objects = bpy.context.selected_objects
        if objects is not None:
            for obj in objects:
                # Remove any existing cloth modifiers first
                for mod in list(obj.modifiers):
                    if mod.type == 'CLOTH':
                        obj.modifiers.remove(mod)
                
                # Add fresh cloth modifier
                cloth_mod = obj.modifiers.new(name='Cloth', type='CLOTH')
                
                # Sewing springs
                cloth_mod.settings.use_sewing_springs = self.use_sewing
                cloth_mod.settings.sewing_force_max = self.sewing_force
                if hasattr(cloth_mod.settings, 'max_sewing_distance'):
                    cloth_mod.settings.max_sewing_distance = self.sewing_max_dist
                
                # Pressure settings
                cloth_mod.settings.use_pressure = self.use_pressure
                cloth_mod.settings.uniform_pressure_force = self.pressure_force
                
                # Air damping
                cloth_mod.settings.air_damping = self.air_damping
                
                # Quality
                cloth_mod.settings.quality = self.quality
                
                # Mass
                cloth_mod.settings.mass = self.mass
                
                # Time scale
                cloth_mod.settings.time_scale = self.time_scale
                
                # Stiffness
                cloth_mod.settings.tension_stiffness = self.tension_stiffness
                cloth_mod.settings.compression_stiffness = self.compression_stiffness
                cloth_mod.settings.shear_stiffness = self.shear_stiffness
                cloth_mod.settings.bending_stiffness = self.bending_stiffness
                
                # Set all effector weights to 0
                ew = cloth_mod.settings.effector_weights
                ew.gravity = 0.0
                ew.all = 0.0
                ew.force = 0.0
                ew.vortex = 0.0
                ew.magnetic = 0.0
                ew.harmonic = 0.0
                ew.charge = 0.0
                if hasattr(ew, 'lennard_jones'):
                    ew.lennard_jones = 0.0
                ew.turbulence = 0.0
                ew.drag = 0.0
                ew.boid = 0.0
        
        return {'FINISHED'}
