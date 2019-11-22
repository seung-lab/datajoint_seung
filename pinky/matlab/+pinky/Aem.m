%{
# my newest table
segmentation:       int         # segmentation version number 
scan_id:            int         # scan ID 
batch_id:           int         # batch ID 
-----
footprints:         longblob    # d*K sparse matrix 

# add additional attributes
%}

classdef Aem < dj.Computed

	methods(Access=protected)

		function makeTuples(self, key)
		%!!! compute missing fields for key here
			 self.insert(key)
		end
	end

end