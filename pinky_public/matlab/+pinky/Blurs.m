%{
# Gaussian blur information
# add primary key here
version: smallint   # version number 
-----
zblur:   smallint   # gaussian width in z direction 
hash:    bigint unsigned    # a hash value for uniquely define this configuration key.hash = sum(prod(key.zvals,2)) *key.zblur;
zvals:   blob       # m* n matrix determing the z values 

# add additional attributes
%}

classdef Blurs < dj.Manual
end
