%{
# Manual ROI masks
-> pinky.Slice
-> pinky.Neuron
---
mask : longblob
%}

classdef ManualMask < dj.Manual
end
