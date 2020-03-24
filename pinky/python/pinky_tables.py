import datajoint as dj
import numpy as np

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
    

@pinky
class Slice(dj.Manual):
  definition = """
  # Slices within scan
  -> Scan
  slice_idx: int
  ---
  depth: int
  """


@pinky 
class Segmentation(dj.Manual):
  definition = """
  # Segmentation information
  segmentation: smallint
  ---
  timestamp: timestamp
  """


@pinky
class Neuron(dj.Manual):
  definition = """
  # Cells with soma
  -> Segmentation
  segment_id: bigint unsigned
  manual_id: int
  """


@pinky
class Soma(dj.Manual):
  definition = """
  # Soma information
  -> Neuron
  ---
  soma_x: int
  soma_y: int
  soma_z: int
  """


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
  # Tuning curve from manual masks
  -> ManualTrace
  -> Stimulus
  ---
  orientation: longblob
  direction: longblob
  """

  def _make_tuples(self, key):

    trace = (ManualTrace() & key).fetch1("spike")
    condition = (Stimulus() & key).fetch1("condition")
    
    valid = ~np.isnan(conditions)
    angle_list = np.unique(conditions[valid])
    
    # Orientation tuning curve
    orientation_tuning = np.zeros((8,))
    for i in range(8):
      angle = angle_list[i]
      section_list = get_section(conditions, angle)

      peak_all1 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all1[j] = np.max(trace_section)
            
      angle = angle_list[i+8]
      section_list = get_section(conditions, angle)

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
      section_list = get_section(conditions, angle)

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
  # Tuning curve from EASE masks
  -> EASETrace
  -> Stimulus
  ---
  orientation: longblob
  direction: longblob
  """

  def _make_tuples(self, key):

    trace = (EASETrace() & key).fetch1("spike")
    condition = (Stimulus() & key).fetch1("condition")
    
    valid = ~np.isnan(conditions)
    angle_list = np.unique(conditions[valid])
    
    # Orientation tuning curve
    orientation_tuning = np.zeros((8,))
    for i in range(8):
      angle = angle_list[i]
      section_list = get_section(conditions, angle)

      peak_all1 = np.zeros(len(section_list))
      for j in range(len(section_list)):

        s = section_list[j]
        trace_section = trace[s[0]:s[1]]
        peak_all1[j] = np.max(trace_section)
            
      angle = angle_list[i+8]
      section_list = get_section(conditions, angle)

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
      section_list = get_section(conditions, angle)

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
class white_list(dj.Manual):
  definition = """
  -> Segment
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
