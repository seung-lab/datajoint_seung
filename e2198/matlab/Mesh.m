%{
# Segment meshes
-> e2198.Segment
---
n_vertices : bigint
n_triangles : bigint
vertices : longblob
triangles : longblob
%}


classdef Mesh < dj.Manual
end
