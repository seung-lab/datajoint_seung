import datajoint as dj
import numpy as np

import pandas as pd

from utils import get_section


# Schema pinky
pinky = dj.schema("Seung_pinky")


@pinky
class Scan(dj.Manual):
  definition = """
  # Functional scan
  scan_id: int
  ---
  depth: int
  laser_power: int
  wavelength: int
  """

  def to_df(self):

    data = {"scan_id": Scan().fetch("scan_id"),
            "depth": Scan().fetch("depth"),
            "laser_power": Scan().fetch("laser_power"),
            "wavelength": Scan().fetch("wavelength")
            }

    return pd.DataFrame(data=data)
    

@pinky
class Slice(dj.Manual):
  definition = """
  # Slices within scan
  -> Scan
  slice_idx: int
  ---
  depth: int
  """

  def to_df(self):

    data = {"scan_id": Slice().fetch("scan_id"),
            "slice_idx": Slice().fetch("slice_idx"),
            "depth": Slice().fetch("depth")
            }


@pinky 
class Segmentation(dj.Manual):
  definition = """
  # Segmentation information
  segmentation: smallint
  ---
  timestamp: timestamp
  """

  def to_df(self):

    data = {"segmentation": Segmentation().fetch("segmentation"),
            "timestamp": Segmentation().fetch("timestamp")
            }

    return pd.DataFrame(data=data)


@pinky
class Neuron(dj.Manual):
  definition = """
  # Cells with soma
  -> Segmentation
  segment_id: bigint unsigned
  manual_id: int
  """

  def to_df(self):

    data = {"segmentation": Neuron().fetch("segmentation"),
            "segment_id": Neuron().fetch("segment_id"),
            "manual_id": Neuron().fetch("manual_id")
            }

    return pd.DataFrame(data=data)


@pinky
class Soma(dj.Manual):
  definition = """
  # Soma information
  -> Neuron
  ---
  loc: blob
  """

  def to_df(self):

    data = {"segmentation": Soma().fetch("segmentation"),
            "segment_id": Soma().fetch("segment_id"),
            "manual_id": Soma().fetch("manual_id"),
            "loc": Soma().fetch("loc")
            }

    return pd.DataFrame(data=data)


@pinky
class ManualMask(dj.Manual):
  definition = """
  # Manual ROI masks
  -> Slice
  -> Neuron
  ---
  mask: longblob
  """


@pinky
class EASEMask(dj.Manual):
  definition = """
  # EASE ROI masks
  -> Slice
  -> Neuron
  ---
  mask: longblob
  """


@pinky
class Stimulus(dj.Manual):
  definition = """
  # Visual stimulus
  -> Scan
  ---
  movie: longblob
  condition: longblob
  """


@pinky
class ManualTrace(dj.Manual):
  definition = """
  # Traces from manual masks
  -> ManualMask
  ---
  trace_raw: longblob
  trace_detrend: longblob
  trace_dff: longblob
  spike: longblob
  """
  

@pinky
class EASETrace(dj.Manual):
  definition = """
  # Traces from EASE masks
  -> Scan
  -> Neuron
  ---
  trace_raw: longblob
  trace: longblob
  spike: longblob
  """


@pinky
class ManualTuning(dj.Computed):
  definition = """
  # Tuning curve from manual traces
  -> ManualTrace
  -> Stimulus
  ---
  orientation: longblob
  direction: longblob
  """

  def _make_tuples(self, key):

    trace = (ManualTrace() & key).fetch1("spike")
    condition = (Stimulus() & key).fetch1("condition")
    
    valid = ~np.isnan(condition)
    angle_list = np.unique(condition[valid])
    
    # Orientation tuning curve
    orientation_tuning = np.zeros((8,))
    for i in range(8):
      angle = angle_list[i]
      section_list = get_section(condition, angle)

      peak_all1 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all1[j] = np.max(trace_section)
            
      angle = angle_list[i+8]
      section_list = get_section(condition, angle)

      peak_all2 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all2[j] = np.max(trace_section)
        
      peak_all = np.concatenate((peak_all1, peak_all2))    
      peak_mean = np.mean(peak_all)
      orientation_tuning[i] = peak_mean

    # Direction tuning curve
    direction_tuning = np.zeros((16,))
    for i in range(16):

      angle = angle_list[i]
      section_list = get_section(condition, angle)

      peak_all = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all[j] = np.max(trace_section)
      
      peak_mean = np.mean(peak_all)
      direction_tuning[i] = peak_mean    

    key["orientation"] = orientation_tuning
    key["direction"] = direction_tuning

    self.insert1(key)
    print("Computed tuning curve for cell {manual_id} in scan {scan_id}".format(**key))


@pinky
class EASETuning(dj.Computed):
  definition = """
  # Tuning curve from EASE traces
  -> EASETrace
  -> Stimulus
  ---
  orientation: longblob
  direction: longblob
  """

  def _make_tuples(self, key):

    trace = (EASETrace() & key).fetch1("spike")
    condition = (Stimulus() & key).fetch1("condition")
    
    valid = ~np.isnan(condition)
    angle_list = np.unique(condition[valid])
    
    # Orientation tuning curve
    orientation_tuning = np.zeros((8,))
    for i in range(8):
      angle = angle_list[i]
      section_list = get_section(condition, angle)

      peak_all1 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all1[j] = np.max(trace_section)
            
      angle = angle_list[i+8]
      section_list = get_section(condition, angle)

      peak_all2 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all2[j] = np.max(trace_section)
        
      peak_all = np.concatenate((peak_all1, peak_all2))    
      peak_mean = np.mean(peak_all)
      orientation_tuning[i] = peak_mean

    # Direction tuning curve
    direction_tuning = np.zeros((16,))
    for i in range(16):

      angle = angle_list[i]
      section_list = get_section(condition, angle)

      peak_all = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all[j] = np.max(trace_section)
      
      peak_mean = np.mean(peak_all)
      direction_tuning[i] = peak_mean    

    key["orientation"] = orientation_tuning
    key["direction"] = direction_tuning

    self.insert1(key)
    print("Computed tuning curve for cell {segment_id} in scan {scan_id}".format(**key))


@pinky
class Segment(dj.Manual):
  definition = """
  # Segments
  -> Segmentation
  segment_id: bigint unsigned
  """


@pinky
class Mesh(dj.Manual):
  definition = """
  # Segment meshes
  -> Segment
  ---
  n_vertices: int
  n_triangles: int
  vertices: longblob
  triangles: longblob
  """


@pinky
class VoxelizedMesh(dj.Computed):
  definition = """
  # Voxelized meshes
  -> Segment
  ---
  n_fragments: int
  n_voxels: int
  n_vertices: int
  n_faces: int
  indices: longblob
  """

  def _make_tuples(self, key):
    pass


@pinky
class FootprintsEM(dj.Computed):
  definition = """
  # EM footprints
  -> Segment
  -> Blurs
  ---
  n_voxels: bigint
  idx_value: longblob
  """

  def _make_tuples(self, key):
    pass


@pinky
class Blurs(dj.Manual):
  definition = """
  # Gaussian blur information
  version: smallint
  ---
  zblur: smallint
  hash: bigint unsigned
  zvals: blob
  """


@pinky
class PycSubgraph(dj.Manual):
  definition = """
  # Pyramidal subgraph
  -> Segmentation
  id: int
  ---
  valid: tinyint
  pre_pt_position: blob
  pre_pt_supervoxel_id: bigint unsigned
  pre_pt_root_id: bigint unsigned
  ctr_pt_position: blob
  post_pt_position: blob
  post_pt_supervoxel_id: bigint unsigned
  post_pt_root_id: bigint unsigned
  size: int
  spine_vol: float
  """

  def to_df(self):
      
    data = {"id": PycSubgraph().fetch("id"),
            "valid": PycSubgraph().fetch("valid"),
            "pre_pt_position": PycSubgraph().fetch("pre_pt_position"),
            "pre_pt_supervoxel_id": PycSubgraph().fetch("pre_pt_supervoxel_id"),
            "pre_pt_root_id": PycSubgraph().fetch("pre_pt_root_id"),
            "ctr_pt_position": PycSubgraph().fetch("ctr_pt_position"),
            "post_pt_position": PycSubgraph().fetch("post_pt_position"),
            "post_pt_supervoxel_id": PycSubgraph().fetch("post_pt_supervoxel_id"),
            "post_pt_root_id": PycSubgraph().fetch("post_pt_root_id"),
            "size": PycSubgraph().fetch("size"),
            "spine_vol": PycSubgraph().fetch("spine_vol")
           }
    
    return pd.DataFrame(data=data)
                
    
@pinky
class PotentialPycSubgraph(dj.Manual):
  definition = """
  # Potential pyramidal subgraph
  -> Segmentation
  no: int
  id: int
  ---
  pre_pt_root_id: bigint unsigned
  ctr_pt_position: blob
  post_pt_root_id: bigint unsigned
  size: int
  n_partner: int
  """
    
  def to_df(self):
        
    data = {"no": PotentialPycSubgraph().fetch("no"),
            "id": PotentialPycSubgraph().fetch("id"),
            "pre_pt_root_id": PotentialPycSubgraph().fetch("pre_pt_root_id"),
            "ctr_pt_position": PotentialPycSubgraph().fetch("ctr_pt_position"),
            "post_pt_root_id": PotentialPycSubgraph().fetch("post_pt_root_id"),
            "size": PotentialPycSubgraph().fetch("size"),
            "n_partner": PotentialPycSubgraph().fetch("n_partner")
           }
        
    return pd.DataFrame(data=data)