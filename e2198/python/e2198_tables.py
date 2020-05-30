import datajoint as dj
import numpy as np


# Schema e2198
e2198 = dj.schema("Seung_e2198")


@e2198
class GC(dj.Manual):
	definition = """
	# Retinal ganglion cells
	cell_id: int
	segment_id: int
	function_id: int
	---
	cell_type: varchar(5)
	"""


@e2198
class Segment(dj.Manual):
  definition = """
  # Segments
  -> Segmentation
  segment_id: int
  """


@e2198
class Mesh(dj.Manual):
  definition = """
  # Segment meshes
  -> Segment
  ---
  n_vertices: int
  n_triangles: int
  vertices: longblob
  triangles: longblob
  """


@e2198
class VoxelizedMesh(dj.Computed):
  definition = """
  # Voxelized meshes
  -> Segment
  ---
  n_fragments: int
  n_voxels: int
  n_vertices: int
  n_faces: int
  indices: longblob
  """

  def _make_tuples(self, key):
    pass


@e2198
class FootprintsEM(dj.Computed):
  definition = """
  # EM footprints
  -> Segment
  -> Blurs
  ---
  n_voxels: bigint
  idx_value: longblob
  """

  def _make_tuples(self, key):
    pass


@e2198
class Blurs(dj.Manual):
  definition = """
  # Gaussian blur information
  version: smallint
  ---
  zblur: smallint
  hash: bigint unsigned
  zvals: blob
  """