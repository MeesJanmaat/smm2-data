from mm2_level.level import Level
from enum import Enum

class Category(Enum):
  terrain = 0
  items = 1
  enemies = 2
  gizmos = 3

class ObjectData():
  def __init__(self, _name, _category):
    self.name = _name
    self.category = _category

  def get_color(self):
    match self.category:
      case Category.terrain:
        return "#00C4F4"
      case Category.items:
        return "#E467E5"
      case Category.enemies:
        return "#66E21C"
      case Category.gizmos:
        return "#F9E401"
      case _:
        return "#FFFFFF"
  
  def get_color_lightened(self):
    match self.category:
      case Category.terrain:
        return "#40FFFF"
      case Category.items:
        return "#FFA7FF"
      case Category.enemies:
        return "#A6FF5C"
      case Category.gizmos:
        return "#FFFF41"
      case _:
        return "#FFFFFF"

Objects = {
  Level.Obj.ObjId.ground: ObjectData("ground", Category.terrain),
  Level.Obj.ObjId.block: ObjectData("block", Category.terrain),
  Level.Obj.ObjId.hard_block: ObjectData("hard_block", Category.terrain),
  Level.Obj.ObjId.coin: ObjectData("coin", Category.items),
  Level.Obj.ObjId.spikes: ObjectData("spikes", Category.terrain),
  Level.Obj.ObjId.question_block: ObjectData("question_block", Category.terrain),
  Level.Obj.ObjId.spring: ObjectData("spring", Category.gizmos),
  Level.Obj.ObjId.ice_block: ObjectData("ice_block", Category.terrain),
  Level.Obj.ObjId.door: ObjectData("door", Category.gizmos),
  Level.Obj.ObjId.pipe: ObjectData("pipe", Category.terrain),
  Level.Obj.ObjId.goomba: ObjectData("goomba", Category.enemies),
  Level.Obj.ObjId.koopa: ObjectData("koopa", Category.enemies),
  Level.Obj.ObjId.steep_slope: ObjectData("steep_slope", Category.terrain),
  Level.Obj.ObjId.slight_slope: ObjectData("slight_slope", Category.terrain),
  Level.Obj.ObjId.hidden_block: ObjectData("hidden_block", Category.terrain),
  Level.Obj.ObjId.bob_omb: ObjectData("bob_omb", Category.enemies),
  Level.Obj.ObjId.lava_lift: ObjectData("lava_lift", Category.gizmos),
  Level.Obj.ObjId.conveyor_belt: ObjectData("conveyor_belt", Category.terrain),
  Level.Obj.ObjId.super_hammer: ObjectData("super_hammer", Category.items),
  Level.Obj.ObjId.lakitu: ObjectData("lakitu", Category.enemies),
  Level.Obj.ObjId.porkupuffer: ObjectData("porkupuffer", Category.enemies),
  Level.Obj.ObjId.buzzy_beetle: ObjectData("buzzy_beetle", Category.enemies),
  Level.Obj.ObjId.pow: ObjectData("pow", Category.gizmos),
  Level.Obj.ObjId.super_hammer: ObjectData("super_hammer", Category.items),
  Level.Obj.ObjId.ant_trooper: ObjectData("ant_trooper", Category.enemies),
  Level.Obj.ObjId.koopa_car: ObjectData("koopa_car", Category.enemies),
  Level.Obj.ObjId.tree: ObjectData("tree", Category.gizmos),
  Level.Obj.ObjId.stingby: ObjectData("stingby", Category.enemies),
  Level.Obj.ObjId.boo: ObjectData("boo", Category.enemies),
  Level.Obj.ObjId.charvaargh: ObjectData("charvaargh", Category.enemies),
}