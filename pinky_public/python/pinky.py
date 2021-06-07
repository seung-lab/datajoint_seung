import datajoint as dj
import numpy as np

import pandas as pd

from utils import get_section, div0


# Schema pinky
pinky = dj.schema("seung_pinky")


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
class Pupil(dj.Manual):
  definition = """
  # Pupil position and size
  -> Scan
  ---
  pupil_r: longblob
  pupil_x: longblob
  pupil_y: longblob
  """


@pinky
class Treadmill(dj.Manual):
  definition = """
  # Treadmill activity
  -> Scan
  ---
  speed: longblob
  vel: longblob
  """


@pinky 
class Segmentation(dj.Manual):
  definition = """
  # Segmentation information
  segmentation: smallint
  ---
  timestamp: date
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
  loc: blob
  """


@pinky
class Neurite(dj.Manual):
  definition = """
  # Axon, dendrite information
  -> Neuron
  ---
  axon_len: float
  dendrite_len: float
  """


@pinky
class SynDegree(dj.Manual):
  definition = """
  # Synapse, connection degree
  -> Neuron
  ---
  syn_out_deg: int
  syn_in_deg: int
  conn_out_deg: int
  conn_in_deg: int
  total_syn_out_deg: int
  total_syn_in_deg: int
  """


@pinky
class SynDensity(dj.Computed):
  definition = """
  # Synapse, connection density
  -> Neurite
  -> SynDegree
  ---
  syn_out_dens: float
  syn_in_dens: float
  conn_out_dens: float
  conn_in_dens: float
  total_syn_out_deg: float
  total_syn_in_deg: float
  """

  def _make_tuples(self, key):
    
    axon_len = (Neurite() & key).fetch1("axon_len")
    dend_len = (Neurite() & key).fetch1("dendrite_len")
    
    deg_list = (SynDegree() & key).fetch()
    
    key["syn_out_dens"] = div0(deg_list[0][3],axon_len)
    key["syn_in_dens"] = div0(deg_list[0][4],dend_len)
    key["conn_out_dens"] = div0(deg_list[0][5],axon_len)
    key["conn_in_dens"] = div0(deg_list[0][6],dend_len)
    key["total_syn_out_deg"] = div0(deg_list[0][7],axon_len)
    key["total_syn_in_deg"] = div0(deg_list[0][8],dend_len)

    self.insert1(key)
    print("Computed synapse density for cell {segment_id}.".format(**key))
  

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
  trace: longblob
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


# @pinky
# class ManualTuning(dj.Computed):
#   definition = """
#   # Tuning curve from manual traces
#   -> ManualTrace
#   -> Stimulus
#   ---
#   orientation: longblob
#   direction: longblob
#   """

#   def _make_tuples(self, key):

#     trace = (ManualTrace() & key).fetch1("spike")
#     condition = (Stimulus() & key).fetch1("condition")
    
#     valid = ~np.isnan(condition)
#     angle_list = np.unique(condition[valid])
    
#     # Orientation tuning curve
#     orientation_tuning = np.zeros((8,))
#     for i in range(8):
#       angle = angle_list[i]
#       section_list = get_section(condition, angle)

#       peak_all1 = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all1[j] = np.max(trace_section)
            
#       angle = angle_list[i+8]
#       section_list = get_section(condition, angle)

#       peak_all2 = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all2[j] = np.max(trace_section)
        
#       peak_all = np.concatenate((peak_all1, peak_all2))    
#       peak_mean = np.mean(peak_all)
#       orientation_tuning[i] = peak_mean

#     # Direction tuning curve
#     direction_tuning = np.zeros((16,))
#     for i in range(16):

#       angle = angle_list[i]
#       section_list = get_section(condition, angle)

#       peak_all = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all[j] = np.max(trace_section)
      
#       peak_mean = np.mean(peak_all)
#       direction_tuning[i] = peak_mean    

#     key["orientation"] = orientation_tuning
#     key["direction"] = direction_tuning

#     self.insert1(key)
#     print("Computed tuning curve for cell {manual_id} in scan {scan_id}".format(**key))


# @pinky
# class EASETuning(dj.Computed):
#   definition = """
#   # Tuning curve from EASE traces
#   -> EASETrace
#   -> Stimulus
#   ---
#   orientation: longblob
#   direction: longblob
#   """

#   def _make_tuples(self, key):

#     trace = (EASETrace() & key).fetch1("spike")
#     condition = (Stimulus() & key).fetch1("condition")
    
#     valid = ~np.isnan(condition)
#     angle_list = np.unique(condition[valid])
    
#     # Orientation tuning curve
#     orientation_tuning = np.zeros((8,))
#     for i in range(8):
#       angle = angle_list[i]
#       section_list = get_section(condition, angle)

#       peak_all1 = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all1[j] = np.max(trace_section)
            
#       angle = angle_list[i+8]
#       section_list = get_section(condition, angle)

#       peak_all2 = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all2[j] = np.max(trace_section)
        
#       peak_all = np.concatenate((peak_all1, peak_all2))    
#       peak_mean = np.mean(peak_all)
#       orientation_tuning[i] = peak_mean

#     # Direction tuning curve
#     direction_tuning = np.zeros((16,))
#     for i in range(16):

#       angle = angle_list[i]
#       section_list = get_section(condition, angle)

#       peak_all = np.zeros(len(section_list))
#       for j in range(len(section_list)):

#         s = section_list[j]
#         trace_section = trace[s[0]:s[1]]
#         peak_all[j] = np.max(trace_section)
      
#       peak_mean = np.mean(peak_all)
#       direction_tuning[i] = peak_mean    

#     key["orientation"] = orientation_tuning
#     key["direction"] = direction_tuning

#     self.insert1(key)
#     print("Computed tuning curve for cell {segment_id} in scan {scan_id}".format(**key))


@pinky
class PycSubgraph(dj.Manual):
  definition = """
  # Pyramidal cell subgraph
  -> Segmentation
  id: int
  ---
  pre_root_id: bigint unsigned
  post_root_id: bigint unsigned
  ctr_pt_position: blob
  pre_pt_position: blob
  post_pt_position: blob
  cleft_size: int
  spine_vol: float
  """


@pinky
class PycSynapse(dj.Manual):
  definition = """
  # Pyramidal cell synapse information
  -> Segmentation
  id: int
  ---
  pre_root_id: bigint unsigned
  post_root_id: bigint unsigned
  ctr_pt_position: blob
  pre_pt_position: blob
  post_pt_position: blob
  cleft_size: int
  """
                
    
@pinky
class Synapse(dj.Manual):
  definition = """
  # Synapse information
  -> Segmentation
  id: int
  ---
  pre_root_id: bigint unsigned
  post_root_id: bigint unsigned
  cleft_vx: int
  ctr_pt_nm: blob
  pre_pos_vx: blob
  ctr_pos_vx: blob
  post_pos_vx: blob
  """