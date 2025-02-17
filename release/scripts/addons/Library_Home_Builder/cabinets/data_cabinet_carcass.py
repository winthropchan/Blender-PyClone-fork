import bpy
import math
from ..pc_lib import pc_types, pc_unit, pc_utils
from . import data_cabinet_parts
from . import data_cabinet_exteriors
from . import data_cabinet_interiors
from .. import home_builder_utils
from .. import home_builder_pointers
from . import common_prompts

from os import path

class Carcass(pc_types.Assembly):

    use_design_carcass = True
    left_side = None
    right_side = None
    back = None
    bottom = None
    top = None
    design_carcass = None
    design_base_assembly = None
    interior = None
    exterior = None

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  
        if obj_bp:
            for child in obj_bp.children:   
                if "IS_LEFT_SIDE_BP" in child:
                    self.left_side = pc_types.Assembly(child)
                if "IS_RIGHT_SIDE_BP" in child:
                    self.right_side = pc_types.Assembly(child)    
                if "IS_BACK_BP" in child:
                    self.back = pc_types.Assembly(child)   
                if "IS_BOTTOM_BP" in child:
                    self.bottom = pc_types.Assembly(child)
                if "IS_TOP_BP" in child:
                    self.top = pc_types.Assembly(child)      
                if "IS_DESIGN_CARCASS_BP" in child:
                    self.design_carcass = pc_types.Assembly(child)         
                if "IS_DESIGN_BASE_ASSEMBLY_BP" in child:
                    self.design_base_assembly = pc_types.Assembly(child)                                          
                if "IS_INTERIOR_BP" in child:
                    self.interior = data_cabinet_interiors.Cabinet_Interior(child)    
                if "IS_EXTERIOR_BP" in child:
                    self.exterior = data_cabinet_exteriors.Cabinet_Exterior(child)                                                    

    def add_design_carcass(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        finished_back = self.get_prompt("Finished Back")
        finished_top = self.get_prompt("Finished Top")
        toe_kick_height = self.get_prompt("Toe Kick Height")
        toe_kick_setback = self.get_prompt("Toe Kick Setback")

        carcass = data_cabinet_parts.add_design_carcass(self)
        carcass.set_name('Design Carcass')
        carcass.loc_x(value=0)
        carcass.loc_y(value=0)
        carcass.dim_x('width',[width])
        carcass.dim_y('depth',[depth])
        if toe_kick_height:
            toe_kick_height_var = toe_kick_height.get_var('toe_kick_height_var')
            toe_kick_setback_var = toe_kick_setback.get_var('toe_kick_setback_var')
            carcass.loc_z('toe_kick_height_var',[toe_kick_height_var])
            carcass.dim_z('height-toe_kick_height_var',[height,toe_kick_height_var])

            base_assembly = data_cabinet_parts.add_design_base_assembly(self)
            base_assembly.set_name('Design Base Assembly')
            base_assembly.loc_x(value=0)
            base_assembly.loc_y(value=0)
            base_assembly.loc_z(value=0)
            base_assembly.dim_x('width',[width])
            base_assembly.dim_y('depth+toe_kick_setback_var',[depth,toe_kick_setback_var])
            base_assembly.dim_z('toe_kick_height_var',[toe_kick_height_var])
            home_builder_pointers.update_design_base_assembly_pointers(base_assembly,True,True,True)

        else:
            carcass.loc_z(value=0)
            carcass.dim_z('height',[height])
        home_builder_pointers.update_design_carcass_pointers(carcass,True,True,True,True,True)
        return carcass

    def add_cabinet_top(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        finished_back = self.get_prompt("Finished Back")
        finished_top = self.get_prompt("Finished Top")

        top = data_cabinet_parts.add_carcass_part(self)
        top.obj_bp["IS_TOP_BP"] = True
        top.set_name('Top')
        top.loc_x('material_thickness',[material_thickness])
        top.loc_y(value=0)
        top.loc_z('height',[height])
        top.dim_x('width-(material_thickness*2)',[width,material_thickness])
        top.dim_y('depth',[depth])
        top.dim_z('-material_thickness',[material_thickness])
        home_builder_pointers.update_top_material(top,finished_back.get_value(),finished_top.get_value())
        return top

    def add_cabinet_bottom(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        finished_back = self.get_prompt("Finished Back")
        finished_bottom = self.get_prompt("Finished Bottom")

        bottom = data_cabinet_parts.add_carcass_part(self)
        bottom.obj_bp["IS_BOTTOM_BP"] = True
        bottom.set_name('Bottom')
        bottom.loc_x('material_thickness',[material_thickness])
        bottom.loc_y(value=0)
        bottom.loc_z('toe_kick_height',[toe_kick_height])
        bottom.dim_x('width-(material_thickness*2)',[width,material_thickness])
        bottom.dim_y('depth',[depth])
        bottom.dim_z('material_thickness',[material_thickness])
        home_builder_pointers.update_bottom_material(bottom,finished_back.get_value(),finished_bottom.get_value())
        home_builder_utils.flip_normals(bottom)
        return bottom

    def add_upper_cabinet_bottom(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        finished_back = self.get_prompt("Finished Back")
        finished_bottom = self.get_prompt("Finished Bottom")

        bottom = data_cabinet_parts.add_carcass_bottom(self)
        bottom.obj_bp["IS_BOTTOM_BP"] = True
        bottom.set_name('Bottom')
        bottom.loc_x('material_thickness',[material_thickness])
        bottom.loc_y(value=0)
        bottom.loc_z(value=0)
        bottom.dim_x('width-(material_thickness*2)',[width,material_thickness])
        bottom.dim_y('depth',[depth])
        bottom.dim_z('material_thickness',[material_thickness])
        home_builder_pointers.update_bottom_material(bottom,finished_back.get_value(),finished_bottom.get_value())
        home_builder_utils.flip_normals(bottom)
        return bottom

    def add_cabinet_back(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")
        finished_back = self.get_prompt("Finished Back")

        back = data_cabinet_parts.add_carcass_part(self)
        back.obj_bp["IS_BACK_BP"] = True
        back.set_name('Back')
        back.loc_x('width-material_thickness',[width,material_thickness])
        back.loc_y(value=0)
        back.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
        back.rot_y(value=math.radians(-90))
        back.rot_z(value=math.radians(90))
        back.dim_x('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        back.dim_y('width-(material_thickness*2)',[width,material_thickness])
        back.dim_z('material_thickness',[material_thickness])
        home_builder_pointers.update_cabinet_back_material(back,finished_back.get_value())
        return back

    def add_upper_cabinet_back(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        finished_back = self.get_prompt("Finished Back")

        back = data_cabinet_parts.add_carcass_part(self)
        back.obj_bp["IS_BACK_BP"] = True
        back.set_name('Back')
        back.loc_x('width-material_thickness',[width,material_thickness])
        back.loc_y(value=0)
        back.loc_z('material_thickness',[material_thickness])
        back.rot_y(value=math.radians(-90))
        back.rot_z(value=math.radians(90))
        back.dim_x('height-(material_thickness*2)',[height,material_thickness])
        back.dim_y('width-(material_thickness*2)',[width,material_thickness])
        back.dim_z('material_thickness',[material_thickness])
        home_builder_pointers.update_cabinet_back_material(back,finished_back.get_value())
        return back

    def add_toe_kick(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")
        toe_kick_setback = self.get_prompt("Toe Kick Setback").get_var("toe_kick_setback")

        toe_kick = data_cabinet_parts.add_double_sided_part(self)
        toe_kick.set_name('Toe Kick')
        toe_kick.loc_x('material_thickness',[material_thickness])
        toe_kick.loc_y('depth+toe_kick_setback+material_thickness',[depth,toe_kick_setback,material_thickness])
        toe_kick.loc_z(value=0)
        toe_kick.rot_x(value=math.radians(90))
        toe_kick.dim_x('width-(material_thickness*2)',[width,material_thickness])
        toe_kick.dim_y('toe_kick_height',[toe_kick_height])
        toe_kick.dim_z('material_thickness',[material_thickness])
        return toe_kick

    def add_blind_panel(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        height = self.obj_z.pyclone.get_var('location.z','height')
        
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        blind_panel_location = self.get_prompt("Blind Panel Location").get_var("blind_panel_location")
        blind_panel_width = self.get_prompt("Blind Panel Width").get_var("blind_panel_width")
        blind_panel_reveal = self.get_prompt("Blind Panel Reveal").get_var("blind_panel_reveal")
        carcass_type = self.get_prompt("Carcass Type")

        blind_panel = data_cabinet_parts.add_double_sided_part(self)
        blind_panel.obj_bp["IS_BLIND_PANEL_BP"] = True
        blind_panel.set_name('Blind Panel')
        blind_panel.loc_x('IF(blind_panel_location==0,material_thickness,width-material_thickness-blind_panel_width-blind_panel_reveal)',
                          [blind_panel_location,material_thickness,width,blind_panel_width,blind_panel_reveal])
        blind_panel.loc_y('depth',[depth])
        blind_panel.rot_y(value=math.radians(-90))
        blind_panel.rot_z(value=math.radians(90))
        blind_panel.dim_y('-blind_panel_width-blind_panel_reveal',[depth,blind_panel_width,blind_panel_reveal])
        blind_panel.dim_z('-material_thickness',[material_thickness])
        if carcass_type.get_value() == "Upper":
            blind_panel.loc_z('material_thickness',[material_thickness])
            blind_panel.dim_x('height-(material_thickness*2)',[height,material_thickness])
        else:
            toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")
            blind_panel.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])      
            blind_panel.dim_x('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])  
        return blind_panel

    def add_cabinet_sides(self,add_toe_kick_notch):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        left_finished_end = self.get_prompt("Left Finished End")
        right_finished_end = self.get_prompt("Right Finished End")
        finished_back = self.get_prompt("Finished Back")
        finished_top = self.get_prompt("Finished Top")
        finished_bottom = self.get_prompt("Finished Bottom")

        left_side = data_cabinet_parts.add_carcass_part(self)
        left_side.obj_bp["IS_LEFT_SIDE_BP"] = True
        left_side.set_name('Left Side')
        left_side.loc_x(value=0)
        left_side.loc_y(value=0)
        left_side.loc_z(value=0)
        left_side.rot_y(value=math.radians(-90))
        left_side.dim_x('height',[height])
        left_side.dim_y('depth',[depth])
        left_side.dim_z('-material_thickness',[material_thickness])

        right_side = data_cabinet_parts.add_carcass_part(self)
        right_side.obj_bp["IS_RIGHT_SIDE_BP"] = True
        right_side.set_name('Right Side')
        right_side.loc_x('width',[width])
        right_side.loc_y(value=0)
        right_side.loc_z(value=0)
        right_side.rot_y(value=math.radians(-90))
        right_side.dim_x('height',[height])
        right_side.dim_y('depth',[depth])
        right_side.dim_z('material_thickness',[material_thickness])
        home_builder_utils.flip_normals(right_side)
        home_builder_pointers.update_side_material(left_side,left_finished_end.get_value(),finished_back.get_value(),finished_top.get_value(),finished_bottom.get_value())
        home_builder_pointers.update_side_material(right_side,right_finished_end.get_value(),finished_back.get_value(),finished_top.get_value(),finished_bottom.get_value())

        if add_toe_kick_notch:
            toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")
            toe_kick_setback = self.get_prompt("Toe Kick Setback").get_var("toe_kick_setback")
            boolean_overhang = self.get_prompt("Boolean Overhang").get_var("boolean_overhang")

            left_notch = data_cabinet_parts.Square_Cutout()
            self.add_assembly(left_notch)
            left_notch.assign_boolean(left_side)
            left_notch.set_name('Left Square Cutout')
            left_notch.loc_x('-boolean_overhang/2',[boolean_overhang])
            left_notch.loc_y('depth-boolean_overhang/2',[depth,boolean_overhang])
            left_notch.loc_z('-boolean_overhang',[boolean_overhang])
            left_notch.rot_y(value=math.radians(-90))
            left_notch.dim_x('toe_kick_height+boolean_overhang',[toe_kick_height,boolean_overhang])
            left_notch.dim_y('toe_kick_setback+boolean_overhang/2',[toe_kick_setback,boolean_overhang])
            left_notch.dim_z('-material_thickness-boolean_overhang',[material_thickness,boolean_overhang])   
            home_builder_utils.flip_normals(left_notch)    

            right_notch = data_cabinet_parts.Square_Cutout()
            self.add_assembly(right_notch)
            right_notch.assign_boolean(right_side)
            right_notch.set_name('Right Square Cutout')
            right_notch.loc_x('width+boolean_overhang/2',[width,boolean_overhang])
            right_notch.loc_y('depth-boolean_overhang/2',[depth,boolean_overhang])
            right_notch.loc_z('-boolean_overhang',[boolean_overhang])
            right_notch.rot_y(value=math.radians(-90))
            right_notch.dim_x('toe_kick_height+boolean_overhang',[toe_kick_height,boolean_overhang])
            right_notch.dim_y('toe_kick_setback+boolean_overhang/2',[toe_kick_setback,boolean_overhang])
            right_notch.dim_z('material_thickness+boolean_overhang',[material_thickness,boolean_overhang])  

        return left_side, right_side

    def add_kick_lighting(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        add_bottom_light = self.get_prompt("Add Bottom Light").get_var("add_bottom_light")
        lighting_width = self.get_prompt("Lighting Width").get_var("lighting_width")
        lighting_dim_from_front = self.get_prompt("Lighting Dim From Front").get_var("lighting_dim_from_front")
        lighting_inset_from_sides = self.get_prompt("Lighting Inset From Sides").get_var("lighting_inset_from_sides")
        toe_kick_height = self.get_prompt("Toe Kick Height").get_var("toe_kick_height")

        light = data_cabinet_parts.add_lighting_strip_part(self)
        light.set_name('Kick Lighting')
        light.loc_x('lighting_inset_from_sides',[lighting_inset_from_sides])
        light.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light.loc_z('toe_kick_height',[toe_kick_height])
        light.rot_y(value=0)
        light.dim_x('width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light.dim_y('lighting_width',[lighting_width])
        light.dim_z(value=-.001)
        home_builder_utils.flip_normals(light)    
        hide = light.get_prompt("Hide")
        hide.set_formula('IF(add_bottom_light==True,False,True)',[add_bottom_light])   

        light_obj = self.add_light('Kick Light','AREA')
        light_obj.data.shape = 'RECTANGLE'
        light_obj.data.energy = .5
        light_obj.pyclone.loc_x('width/2',[width])
        light_obj.pyclone.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light_obj.pyclone.loc_z('toe_kick_height',[toe_kick_height])
        light_obj.pyclone.add_data_driver('size',-1,'width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light_obj.pyclone.add_data_driver('size_y',-1,'lighting_width',[lighting_width])
        light_obj.pyclone.hide('IF(add_bottom_light==True,False,True)',[add_bottom_light])   
    
    def add_under_cabinet_lighting(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        add_bottom_light = self.get_prompt("Add Bottom Light").get_var("add_bottom_light")
        lighting_width = self.get_prompt("Lighting Width").get_var("lighting_width")
        lighting_dim_from_front = self.get_prompt("Lighting Dim From Front").get_var("lighting_dim_from_front")
        lighting_inset_from_sides = self.get_prompt("Lighting Inset From Sides").get_var("lighting_inset_from_sides")

        light = data_cabinet_parts.add_lighting_strip_part(self)
        light.set_name('Under Cabinet Light')
        light.loc_x('lighting_inset_from_sides',[lighting_inset_from_sides])
        light.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light.loc_z(value=0)
        light.rot_y(value=0)
        light.dim_x('width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light.dim_y('lighting_width',[lighting_width])
        light.dim_z(value=-.001)
        home_builder_utils.flip_normals(light)    
        hide = light.get_prompt("Hide")
        hide.set_formula('IF(add_bottom_light==True,False,True)',[add_bottom_light])   

        light_obj = self.add_light('Under Cabinet Light','AREA')
        light_obj.data.shape = 'RECTANGLE'
        light_obj.data.energy = .5
        light_obj.pyclone.loc_x('width/2',[width])
        light_obj.pyclone.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light_obj.pyclone.loc_z(value=0)
        light_obj.pyclone.add_data_driver('size',-1,'width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light_obj.pyclone.add_data_driver('size_y',-1,'lighting_width',[lighting_width])
        light_obj.pyclone.hide('IF(add_bottom_light==True,False,True)',[add_bottom_light])

    def add_side_lighting(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        add_side_light = self.get_prompt("Add Side Light").get_var("add_side_light")
        lighting_width = self.get_prompt("Lighting Width").get_var("lighting_width")
        lighting_dim_from_front = self.get_prompt("Lighting Dim From Front").get_var("lighting_dim_from_front")
        lighting_inset_from_sides = self.get_prompt("Lighting Inset From Sides").get_var("lighting_inset_from_sides")
        toe_kick_height = self.get_prompt("Toe Kick Height")

        l_light = data_cabinet_parts.add_lighting_strip_part(self)
        l_light.set_name('Top Cabinet Light')
        l_light.loc_x('material_thickness',[material_thickness])
        l_light.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        l_light.rot_y(value=math.radians(-90))
        if toe_kick_height:
            kick_height = toe_kick_height.get_var('kick_height')    
            l_light.loc_z('kick_height+material_thickness',[kick_height,material_thickness])
            l_light.dim_x('height-(lighting_inset_from_sides*2)-kick_height',[height,lighting_inset_from_sides,kick_height])
        else:
            l_light.dim_x('height-(lighting_inset_from_sides*2)',[height,lighting_inset_from_sides])
            l_light.loc_z('material_thickness',[material_thickness])
        l_light.dim_y('lighting_width',[lighting_width])
        l_light.dim_z(value=-.001)
        home_builder_utils.flip_normals(l_light)    
        hide = l_light.get_prompt("Hide")
        hide.set_formula('IF(add_side_light==True,False,True)',[add_side_light])   

        l_light_obj = self.add_light('Under Cabinet Light','AREA')
        l_light_obj.data.shape = 'RECTANGLE'
        l_light_obj.data.energy = .5
        l_light_obj.pyclone.loc_x('material_thickness+.001',[material_thickness])
        l_light_obj.pyclone.loc_y('depth+lighting_dim_from_front+(lighting_width)/2',[depth,lighting_dim_from_front,lighting_width])
        if toe_kick_height:
            kick_height = toe_kick_height.get_var('kick_height')
            l_light_obj.pyclone.loc_z('(height+kick_height)/2',[height,kick_height])
            l_light_obj.pyclone.add_data_driver('size',-1,'height-(lighting_inset_from_sides*2)-kick_height',
            [height,lighting_inset_from_sides,kick_height])
        else:
            l_light_obj.pyclone.loc_z('height/2',[height,material_thickness])
            l_light_obj.pyclone.add_data_driver('size',-1,'height-(lighting_inset_from_sides*2)',
            [height,lighting_inset_from_sides])
        l_light_obj.pyclone.rot_y(value=math.radians(-90))
        l_light_obj.pyclone.add_data_driver('size_y',-1,'lighting_width',[lighting_width])
        l_light_obj.pyclone.hide('IF(add_side_light==True,False,True)',[add_side_light])

        r_light = data_cabinet_parts.add_lighting_strip_part(self)
        r_light.set_name('Top Cabinet Light')
        r_light.loc_x('width-material_thickness-.001',[width,material_thickness])
        r_light.loc_y('depth+lighting_dim_from_front+(lighting_width)/2',[depth,lighting_dim_from_front,lighting_width])
        r_light.loc_z('height-material_thickness',[height,material_thickness])
        r_light.rot_y(value=math.radians(90))
        if toe_kick_height:
            kick_height = toe_kick_height.get_var('kick_height')
            r_light.dim_x('height-(lighting_inset_from_sides*2)-kick_height',[height,lighting_inset_from_sides,kick_height])
        else:
            r_light.dim_x('height-(lighting_inset_from_sides*2)',[height,lighting_inset_from_sides])
        r_light.dim_y('lighting_width',[lighting_width])
        r_light.dim_z(value=-.001)
        home_builder_utils.flip_normals(r_light)    
        hide = r_light.get_prompt("Hide")
        hide.set_formula('IF(add_side_light==True,False,True)',[add_side_light])   

        r_light_obj = self.add_light('Under Cabinet Light','AREA')
        r_light_obj.data.shape = 'RECTANGLE'
        r_light_obj.data.energy = .5
        r_light_obj.pyclone.loc_x('width-material_thickness',[width,material_thickness])
        r_light_obj.pyclone.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        if toe_kick_height:
            kick_height = toe_kick_height.get_var('kick_height')
            r_light_obj.pyclone.loc_z('(height+kick_height)/2',[height,kick_height])
            r_light_obj.pyclone.add_data_driver('size',-1,'height-(lighting_inset_from_sides*2)-kick_height',[height,lighting_inset_from_sides,kick_height])
        else:
            r_light_obj.pyclone.loc_z('height/2',[height,material_thickness])
            r_light_obj.pyclone.add_data_driver('size',-1,'height-(lighting_inset_from_sides*2)',[height,lighting_inset_from_sides])
        r_light_obj.pyclone.rot_y(value=math.radians(90))
        r_light_obj.pyclone.add_data_driver('size_y',-1,'lighting_width',[lighting_width])
        r_light_obj.pyclone.hide('IF(add_side_light==True,False,True)',[add_side_light])

    def add_top_lighting(self):
        width = self.obj_x.pyclone.get_var('location.x','width')
        height = self.obj_z.pyclone.get_var('location.z','height')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        material_thickness = self.get_prompt("Material Thickness").get_var("material_thickness")
        add_top_light = self.get_prompt("Add Top Light").get_var("add_top_light")
        lighting_width = self.get_prompt("Lighting Width").get_var("lighting_width")
        lighting_dim_from_front = self.get_prompt("Lighting Dim From Front").get_var("lighting_dim_from_front")
        lighting_inset_from_sides = self.get_prompt("Lighting Inset From Sides").get_var("lighting_inset_from_sides")

        light = data_cabinet_parts.add_lighting_strip_part(self)
        light.set_name('Top Cabinet Light')
        light.loc_x('lighting_inset_from_sides',[lighting_inset_from_sides])
        light.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light.loc_z('height-material_thickness',[height,material_thickness])
        light.rot_y(value=0)
        light.dim_x('width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light.dim_y('lighting_width',[lighting_width])
        light.dim_z(value=-.001)
        home_builder_utils.flip_normals(light)    
        hide = light.get_prompt("Hide")
        hide.set_formula('IF(add_top_light==True,False,True)',[add_top_light])   

        light_obj = self.add_light('Under Cabinet Light','AREA')
        light_obj.data.shape = 'RECTANGLE'
        light_obj.data.energy = .5
        light_obj.pyclone.loc_x('width/2',[width])
        light_obj.pyclone.loc_y('depth+lighting_dim_from_front',[depth,lighting_dim_from_front])
        light_obj.pyclone.loc_z('height-material_thickness',[height,material_thickness])
        light_obj.pyclone.add_data_driver('size',-1,'width-(lighting_inset_from_sides*2)',[width,lighting_inset_from_sides])
        light_obj.pyclone.add_data_driver('size_y',-1,'lighting_width',[lighting_width])
        light_obj.pyclone.hide('IF(add_top_light==True,False,True)',[add_top_light])

    def add_insert(self,insert):
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt('Material Thickness').get_var('material_thickness')
        carcass_type = self.get_prompt("Carcass Type")

        if insert.carcass_type == "":
            insert.carcass_type = carcass_type.get_value()

        insert = self.add_assembly(insert)
        insert.loc_x('material_thickness',[material_thickness])
        insert.loc_y('depth',[depth])
        if carcass_type.get_value() == "Upper": #UPPER CABINET
            insert.loc_z('material_thickness',[material_thickness])
            insert.dim_z('height-(material_thickness*2)',[height,material_thickness])
        else:
            toe_kick_height = self.get_prompt('Toe Kick Height').get_var('toe_kick_height')
            insert.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
            insert.dim_z('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        
        insert.dim_x('width-(material_thickness*2)',[width,material_thickness])
        insert.dim_y('fabs(depth)-material_thickness',[depth,material_thickness])
        insert.obj_x.empty_display_size = .001
        insert.obj_y.empty_display_size = .001
        insert.obj_z.empty_display_size = .001
        insert.obj_bp.empty_display_size = .001
        insert.obj_prompts.empty_display_size = .001

        bpy.context.view_layer.update()

        # calculator = insert.get_calculator('Front Height Calculator')
        # if calculator:
        #     calculator.calculate()
        
        return insert

    def add_blind_exterior(self,insert):
        # x_loc_carcass = self.obj_bp.pyclone.get_var('location.x','x_loc_carcass')
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt('Material Thickness').get_var('material_thickness')
        carcass_type = self.get_prompt("Carcass Type")
        blind_panel_location = self.get_prompt("Blind Panel Location").get_var("blind_panel_location")
        blind_panel_width = self.get_prompt("Blind Panel Width").get_var("blind_panel_width")
        blind_panel_reveal = self.get_prompt("Blind Panel Reveal").get_var("blind_panel_reveal")
        
        #ADD NAME OF EXTERIOR TO 
        #PASS PROMPTS IN CORRECT
        insert.carcass_type = carcass_type.get_value()

        insert = self.add_assembly(insert)
        insert.loc_x('IF(blind_panel_location==0,material_thickness+blind_panel_width+blind_panel_reveal,material_thickness)',
                     [blind_panel_location,width,blind_panel_width,blind_panel_reveal,material_thickness])
        insert.loc_y('depth',[depth])
        if carcass_type.get_value() == "Upper": #UPPER CABINET
            insert.loc_z('material_thickness',[material_thickness])
            insert.dim_z('height-(material_thickness*2)',[height,material_thickness])
        else:
            toe_kick_height = self.get_prompt('Toe Kick Height').get_var('toe_kick_height')
            insert.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
            insert.dim_z('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        
        insert.dim_x('width-(material_thickness*2)-blind_panel_width-blind_panel_reveal',[width,material_thickness,blind_panel_width,blind_panel_reveal])
        insert.dim_y('fabs(depth)-material_thickness',[depth,material_thickness])
        insert.obj_x.empty_display_size = .001
        insert.obj_y.empty_display_size = .001
        insert.obj_z.empty_display_size = .001
        insert.obj_bp.empty_display_size = .001
        insert.obj_prompts.empty_display_size = .001

        bpy.context.view_layer.update()

        # calculator = insert.get_calculator('Front Height Calculator')
        # if calculator:
        #     calculator.calculate()
        
        return insert

    def add_blind_interior(self,insert):
        # x_loc_carcass = self.obj_bp.pyclone.get_var('location.x','x_loc_carcass')
        width = self.obj_x.pyclone.get_var('location.x','width')
        depth = self.obj_y.pyclone.get_var('location.y','depth')
        height = self.obj_z.pyclone.get_var('location.z','height')
        material_thickness = self.get_prompt('Material Thickness').get_var('material_thickness')
        carcass_type = self.get_prompt("Carcass Type")

        #ADD NAME OF EXTERIOR TO 
        #PASS PROMPTS IN CORRECT
        insert.carcass_type = carcass_type.get_value()

        insert = self.add_assembly(insert)
        insert.loc_x('material_thickness',[material_thickness])
        insert.loc_y('depth+material_thickness',[depth,material_thickness])
        if carcass_type.get_value() == "Upper": #UPPER CABINET
            insert.loc_z('material_thickness',[material_thickness])
            insert.dim_z('height-(material_thickness*2)',[height,material_thickness])
        else:
            toe_kick_height = self.get_prompt('Toe Kick Height').get_var('toe_kick_height')
            insert.loc_z('toe_kick_height+material_thickness',[toe_kick_height,material_thickness])
            insert.dim_z('height-toe_kick_height-(material_thickness*2)',[height,toe_kick_height,material_thickness])
        
        insert.dim_x('width-(material_thickness*2)',[width,material_thickness])
        insert.dim_y('fabs(depth)-(material_thickness*2)',[depth,material_thickness])
        insert.obj_x.empty_display_size = .001
        insert.obj_y.empty_display_size = .001
        insert.obj_z.empty_display_size = .001
        insert.obj_bp.empty_display_size = .001
        insert.obj_prompts.empty_display_size = .001

        bpy.context.view_layer.update()

        # calculator = insert.get_calculator('Front Height Calculator')
        # if calculator:
        #     calculator.calculate()
        
        return insert

class Base_Advanced(Carcass):

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  

    def draw(self):
        props = home_builder_utils.get_scene_props(bpy.context.scene)
        self.use_design_carcass = props.use_design_carcass

        self.create_assembly("Carcass")
        self.obj_bp["IS_CARCASS_BP"] = True

        # common_prompts.add_cabinet_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_carcass_prompts(self)
        common_prompts.add_base_assembly_prompts(self)
        # common_prompts.add_cabinet_lighting_prompts(self)
        
        carcass_type = self.get_prompt("Carcass Type")
        carcass_type.set_value("Base")

        self.obj_x.location.x = pc_unit.inch(18) 
        self.obj_y.location.y = -props.base_cabinet_depth
        self.obj_z.location.z = props.base_cabinet_height

        if self.use_design_carcass:
            self.add_design_carcass()
        else:
            self.add_cabinet_bottom()
            self.add_cabinet_top()
            self.left_side, self.right_side = self.add_cabinet_sides(add_toe_kick_notch=True)
            self.back = self.add_cabinet_back()
            self.add_toe_kick()
            # add_top_lighting(self)
            # add_kick_lighting(self)
            # add_side_lighting(self)


class Tall_Advanced(Carcass):

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  

    def draw(self):
        props = home_builder_utils.get_scene_props(bpy.context.scene)
        self.use_design_carcass = props.use_design_carcass

        self.create_assembly("Carcass")
        self.obj_bp["IS_CARCASS_BP"] = True

        # common_prompts.add_cabinet_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_carcass_prompts(self)
        common_prompts.add_base_assembly_prompts(self)
        # common_prompts.add_cabinet_lighting_prompts(self)

        carcass_type = self.get_prompt("Carcass Type")
        carcass_type.set_value("Tall")

        self.obj_x.location.x = pc_unit.inch(18) 
        self.obj_y.location.y = -props.tall_cabinet_depth
        self.obj_z.location.z = props.tall_cabinet_height

        if self.use_design_carcass:
            self.add_design_carcass()
        else:
            self.add_cabinet_bottom()
            self.add_cabinet_top()
            self.add_cabinet_sides(add_toe_kick_notch=True)
            self.add_cabinet_back()
            self.add_toe_kick()
            # add_top_lighting(self)
            # add_kick_lighting(self)
            # add_side_lighting(self)

class Upper_Advanced(Carcass):

    def __init__(self,obj_bp=None):
        super().__init__(obj_bp=obj_bp)  

    def draw(self):
        props = home_builder_utils.get_scene_props(bpy.context.scene)
        self.use_design_carcass = props.use_design_carcass
        
        self.create_assembly("Carcass")
        self.obj_bp["IS_CARCASS_BP"] = True

        common_prompts.add_cabinet_prompts(self)
        common_prompts.add_thickness_prompts(self)
        common_prompts.add_carcass_prompts(self)
        # common_prompts.add_cabinet_lighting_prompts(self)

        carcass_type = self.get_prompt("Carcass Type")
        carcass_type.set_value("Upper")
        print('CTYPE',carcass_type.get_value())
        self.obj_x.location.x = pc_unit.inch(18) 
        self.obj_y.location.y = -props.upper_cabinet_depth
        self.obj_z.location.z = props.upper_cabinet_height

        if self.use_design_carcass:
            self.add_design_carcass()
        else:
            self.add_upper_cabinet_bottom()
            self.add_cabinet_top()
            self.add_cabinet_sides(add_toe_kick_notch=False)
            self.add_upper_cabinet_back()
            # add_top_lighting(self)
            # add_under_cabinet_lighting(self)
            # add_side_lighting(self)


class Refrigerator(pc_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Transition(pc_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Blind_Corner(pc_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Inside_Corner(pc_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"

class Outside_Corner(pc_types.Assembly):
    category_name = "Carcass"
    prompt_id = "room.part_prompts"
    placement_id = "room.draw_multiple_walls"