from lib.engine import MPMSimulator
import numpy as np

_base_ = '../configs/default.py'

cfg = dict(
    dtype='float32',
    n_cameras = 11,
    n_frames = 14,
    H = 800,
    W = 800,
    dt = 1/24/200,
    xyz_min = [-0.5, 0.1, -0.5],
    xyz_max = [0.5, 1.2, 0.5],
    material = MPMSimulator.elasticity,
    pg_scale = [1000, 2000, 4000],
    data_dir = 'data/torus',
    base_dir = 'checkpoint/torus',
    dx = 0.16,
    cuda_chunk_size = 100,
    nerf_bs = 2**16,
    particle_chunk_size=2**10,
    taichi_cuda_memory=0.6,
    N_static = 6001,
    entropy_weight = 1e-3,
    volume_weight = 1e-3,
    # tv_weight = 1e-4,
    direct_nerf = False,
    hit_frame = 5,
    physical_params = dict(global_E=1e-1, global_nu=1e-2),
    write_out = True,
    random_particles=True,
    E = 1e5,
    nu = 0.1,
    rho = 1000,
)

del MPMSimulator
del np
