%{
# A segment including a cell soma
-> pinky.Segment
---
soma_id                     : int unsigned                  # soma id in Allen annotation database
soma_x=null                 : int unsigned                  # x location of soma in grid coordinates
soma_y=null                 : int unsigned                  # y location of soma in grid coordinates
soma_z=null                 : int unsigned                  # z location of soma in grid coordinates
%}


classdef AllenSoma < dj.Manual
end