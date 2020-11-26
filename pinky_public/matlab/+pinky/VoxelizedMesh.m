%{
# Voxelized meshes
-> pinky.Segment
-----
n_fragments          : int                    # number of fragments
n_voxels             : int                    # number of voxels
n_vertices           : int                    # number of vertices
n_faces              : int                    # number of faces
indices              : longblob               # indices of nonzero voxels
%}

classdef VoxelizedMesh < dj.Computed
    
    methods(Access=protected)
        
        function makeTuples(self, key)
            options = evalin('base', 'options');
            % computed the indices of nonzero voxels
            [vertices, faces, n_vertices, n_triangles]= fetch1((pinky.Mesh & sprintf(...
                'segmentation=%d and segment_id=%d', key.segmentation, key.segment_id)),...
                'vertices', 'triangles', 'n_vertices', 'n_triangles');
            key.n_vertices = n_vertices;
            key.n_faces = n_triangles;
            key.n_fragments = 1;
            % voxelization
            [subs_2p, ~] = mesh2volume(vertices, faces, options);
            key.indices = sub2ind(options.dims_2p, subs_2p(:,1), subs_2p(:,2), subs_2p(:,3));
            key.n_voxels = size(key.indices, 1);
            
            self.insert(key)
        end
    end
    
end
