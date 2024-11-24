import pandas as pd
import numpy as np
from kaitaistruct import KaitaiStream
from mm2_level.level import Level
from io import BytesIO
import zlib
import multiprocessing as mp
import time
import pickle

# to-do: objects containing other objects

obj_counts = {}
obj_likes = {}
obj_boos = {}
obj_plays = {}
obj_attempts = {}
obj_clears = {}

def append_dicts(id, likes, boos, plays, attempts, clears):
  obj_counts[id] = obj_counts.get(id, 0) + 1
  obj_likes[id] = obj_likes.get(id, 0) + likes
  obj_boos[id] = obj_boos.get(id, 0) + boos
  obj_plays[id] = obj_plays.get(id, 0) + plays
  obj_attempts[id] = obj_attempts.get(id, 0) + attempts
  obj_clears[id] = obj_clears.get(id, 0) + clears

# Level objects analysis
def analyze_level(level_data, likes, boos, plays, attempts, clears):
  encountered_objects = set()
  level = Level(KaitaiStream(BytesIO(zlib.decompress(level_data))))
  # Overworld
  for i in range(level.overworld.object_count):
    obj = level.overworld.objects[i]
    if (obj.id not in encountered_objects):
      append_dicts(obj.id, likes, boos, plays, attempts, clears)
      encountered_objects.add(obj.id)
  # Subworld
  for i in range(level.subworld.object_count):
    obj = level.subworld.objects[i]
    if (obj.id not in encountered_objects):
      append_dicts(obj.id, likes, boos, plays, attempts, clears)
      encountered_objects.add(obj.id)
  
  # Miscellaneous objects that already have their own counter
  if (level.overworld.ice_count > 0 or level.subworld.ice_count > 0):
    append_dicts(Level.Obj.ObjId.ice_block, likes, boos, plays, attempts, clears)
  if (level.overworld.track_count > 0 or level.subworld.track_count > 0):
    append_dicts(Level.Obj.ObjId.track, likes, boos, plays, attempts, clears)
  if (level.overworld.ground_count > 0 or level.subworld.ground_count > 0):
    append_dicts(Level.Obj.ObjId.ground, likes, boos, plays, attempts, clears)
  if (level.overworld.clear_pipe_count > 0 or level.subworld.clear_pipe_count > 0):
    append_dicts(Level.Obj.ObjId.clear_pipe, likes, boos, plays, attempts, clears)
  if (level.overworld.snake_block_count > 0 or level.subworld.snake_block_count > 0):
    append_dicts(Level.Obj.ObjId.snake_block, likes, boos, plays, attempts, clears)
  if (level.overworld.track_block_count > 0 or level.subworld.track_block_count > 0):
    append_dicts(Level.Obj.ObjId.track_block, likes, boos, plays, attempts, clears)
  if (level.overworld.piranha_creeper_count > 0 or level.subworld.piranha_creeper_count > 0):
    append_dicts(Level.Obj.ObjId.piranha_creeper, likes, boos, plays, attempts, clears)
  if (level.overworld.exclamation_mark_block_count > 0 or level.subworld.exclamation_mark_block_count > 0):
    append_dicts(Level.Obj.ObjId.exclamation_block, likes, boos, plays, attempts, clears)
  

def worker(data):
  data.apply(lambda d: analyze_level(d["level_data"], d["likes"], d["boos"], d["plays"], d["attempts"], d["clears"]), axis=1)
  return obj_counts, obj_likes, obj_boos, obj_plays, obj_attempts, obj_clears

if __name__ == '__main__':
  df = pd.read_parquet("mm2_level/data/train-00000-of-00196-7a2d43e1e8287c30.parquet", engine="fastparquet")
  n_proc = 16
  chunk_size = 5120
  offset = 16 * 5120
  subframes = [df.iloc[i + offset:i + offset + chunk_size] for i in range(0, n_proc * chunk_size, chunk_size)]

  with mp.Pool(n_proc) as pool:
    start = time.time()
    res = pool.map(worker, subframes)
    end = time.time()
    pool.close()
    pool.join()

  print(f"Analysis done on {n_proc * chunk_size} levels in {round(end - start, 4)} seconds. Starting final summation...")

  for result in res:
    for key in result[0]: obj_counts[key] = obj_counts.get(key, 0) + result[0][key]
    for key in result[1]: obj_likes[key] = obj_likes.get(key, 0) + result[1][key]
    for key in result[2]: obj_boos[key] = obj_boos.get(key, 0) + result[2][key]
    for key in result[3]: obj_plays[key] = obj_plays.get(key, 0) + result[3][key]
    for key in result[4]: obj_attempts[key] = obj_attempts.get(key, 0) + result[4][key]
    for key in result[5]: obj_clears[key] = obj_clears.get(key, 0) + result[5][key]

  print(obj_counts)

  print("Writing to files...")
  pickle.dump(obj_counts, file=open(f"object_count_data/obj_counts_{offset}_{offset + n_proc * chunk_size}", "wb"))
  pickle.dump(obj_likes, file=open(f"object_count_data/obj_likes_{offset}_{offset + n_proc * chunk_size}", "wb"))
  pickle.dump(obj_boos, file=open(f"object_count_data/obj_boos_{offset}_{offset + n_proc * chunk_size}", "wb"))
  pickle.dump(obj_plays, file=open(f"object_count_data/obj_plays_{offset}_{offset + n_proc * chunk_size}", "wb"))
  pickle.dump(obj_attempts, file=open(f"object_count_data/obj_attempts_{offset}_{offset + n_proc * chunk_size}", "wb"))
  pickle.dump(obj_clears, file=open(f"object_count_data/obj_clears_{offset}_{offset + n_proc * chunk_size}", "wb"))