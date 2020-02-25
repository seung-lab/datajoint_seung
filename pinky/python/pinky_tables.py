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
  # Tuning curve of manual traces
  -> ManualTrace
  -> Stimulus
  ---
  tuning_curve: longblob
  """

  def _make_tuples(self, key):

    trace = (ManualTrace() & key).fetch1("trace")

    condition = (Stimulus() & key).fetch1("condition")
    valid = ~np.isnan(condition)
    angle_list = np.unique(condition[valid])

    tuning = np.zeros((2,16))
    for i in range(16):

      angle = angle_list[i]
      section_list = get_section(condition, angle)

      n = 16
      trace_all = np.ones((len(section_list),n))*np.nan
      for j in range(len(section_list)):

        s = section_list[j]
          
        trace_section = trace[s[0]:s[1]]
        trace_all[j,:trace_section.shape[0]] = trace_section

      peak_all = np.nanmax(trace_all, axis=1)
      peak_mean = np.mean(peak_all)
      peak_std = np.std(peak_all)
      tuning[0,i] = peak_mean
      tuning[1,i] = peak_std

    key["tuning_curve"] = tuning[0,:]

    self.insert1(key)
    print("Computed tuning curve for cell {manual_id} in scan {scan_id}, slice {slice_idx}".format(**key))


@pinky
class EASETuning(dj.Computed):
  definition = """
  # Tuning curve of EASE traces
  -> EASETrace
  -> Stimulus
  ---
  tuning_curve: longblob
  """

  def _make_tuples(self, key):

    trace = (EASETrace() & key).fetch1("trace")

    condition = (Stimulus() & key).fetch1("condition")
    valid = ~np.isnan(condition)
    angle_list = np.unique(condition[valid])

    tuning = np.zeros((2,16))
    for i in range(16):

      angle = angle_list[i]
      section_list = get_section(condition, angle)

      n = 16
      trace_all = np.ones((len(section_list),n))*np.nan
      for j in range(len(section_list)):

        s = section_list[j]
          
        trace_section = trace[s[0]:s[1]]
        trace_all[j,:trace_section.shape[0]] = trace_section

      peak_all = np.nanmax(trace_all, axis=1)
      peak_mean = np.mean(peak_all)
      peak_std = np.std(peak_all)
      tuning[0,i] = peak_mean
      tuning[1,i] = peak_std

    key["tuning_curve"] = tuning[0,:]

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
