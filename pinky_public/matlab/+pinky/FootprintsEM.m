%{
# EM footprints
-> pinky.Segment
-> pinky.Blurs
-----
n_voxels: bigint        # number of voxels 
idx_value: longblob     # M*2 matrix, [idx, value]  
%}

classdef FootprintsEM < dj.Computed
    
    methods(Access=protected)
        
        function makeTuples(self, key)
            %!!! compute missing fields for key here
            % get options
            options = evalin('base', 'options');
            dims_2p = options.dims_2p;
            
            % load non-zero voxels
            [indices, n_voxels] = fetch1(pinky.VoxelizedMesh & ...
                sprintf('segmentation=%d', key.segmentation) & ...
                sprintf('segment_id=%d', key.segment_id),...
                'indices', 'n_voxels');
            
            if n_voxels > options.min_voxels
                [ridx, cidx, zidx] = ind2sub(dims_2p, indices);
                rcidx = sub2ind(dims_2p(1:2), ridx, cidx);
                
                % project to the slected z planes
                temp = abs(bsxfun(@minus, zidx, options.zvals));   % distance to the selected planes
                temp(temp>2*options.zblur) = inf;
                v = exp(-temp.^2 / options.norm_z);
                
                %%
                zidx = repmat(options.zvals, [length(rcidx), 1]);
                rcidx = repmat(rcidx, [1, length(options.zvals)]);
                temp = sparse(rcidx(:), zidx(:), v(:), dims_2p(1)*dims_2p(2), dims_2p(3));
                [ii, jj, value] = find(temp);
                idx = sub2ind([dims_2p(1)*dims_2p(2), dims_2p(3)], ii, jj);
                key.idx_value = [idx, value];
                key.n_voxels = length(value);
            else
                key.n_voxels = 0;
                key.idx_value = [];
            end
            key.version = options.version;
            self.insert(key)
        end
    end
    
end
