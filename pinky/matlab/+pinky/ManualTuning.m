%{
# Tuning curve of manual traces
-> pinky.ManualTrace
-> pinky.Stimulus
---
tuning_curve : longblob
%}

classdef ManualTuning < dj.Computed
    
    methods(Access=protected)
        
        function makeTuples(self, key)
        end
    end
    
end