%{
# Traces from EASE masks
-> pinky.Scan
-> pinky.Neuron
---
trace_raw : longblob
trace : longblob
spike : longblob
%}

classdef EASETrace < dj.Manual
end
