%{
# Segment meshes
-> pinky.Segment
---
n_vertices : bigint
n_triangles : bigint
vertices : longblob
triangles : longblob
%}


classdef Mesh < dj.Manual
end
