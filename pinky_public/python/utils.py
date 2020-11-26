import numpy as np


def get_section(conditions, angle):
    
  valid = conditions==angle
  valid_diff = np.diff(valid)
  valid_diff = valid_diff.reshape((1,-1))
  
  edge_idx = np.where(valid_diff==1)[1]
      
  section_list = []
  
  for i in range(len(edge_idx)//2):
    section_list.append((edge_idx[np.remainder(len(edge_idx),2)+i*2]+1, edge_idx[np.remainder(len(edge_idx),2)+i*2+1]+1))
  
  return section_list


def str2array(s):
    
    elem = s[1:-1].split(" ")
    
    array = []
    for e in elem:
        
        if e!="":
            array.append(int(e))
            
    return np.array(array)