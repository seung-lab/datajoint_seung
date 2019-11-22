%{
# voxelized meshes
-> pinky.Segment
---
indices                     : longblob                      # indices of nonzero voxels
%}


classdef VoxelizedMeshBackup < dj.Computed

	methods(Access=protected)

		function makeTuples(self, key)
		%!!! compute missing fields for key here
			 self.insert(key)
		end
	end

end