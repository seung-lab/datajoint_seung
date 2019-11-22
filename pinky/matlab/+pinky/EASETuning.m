%{
# Tuning curve of EASE traces
-> pinky.EASETrace
-> pinky.Stimulus
---
tuning_curve : longblob
%}

classdef EASETuning < dj.Computed
    
    methods(Access=protected)
        
        function makeTuples(self, key)
        end
    end
    
end