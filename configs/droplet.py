from lib.engine import MPMSimulator
import numpy as np

_base_ = "../configs/default.py"

cfg = dict(
    dtype='float32',
    n_cameras=11,
    n_frames=13,
    H=800,
    W=800,
    dt=1 / 4800,
    xyz_min=[-0.4, 0.1, -0.4],
    xyz_max=[0.4, 1.0, 0.4],
    material=MPMSimulator.viscous_fluid,
    pg_scale=[1000, 2000, 4000],
    data_dir="data/droplet",
    base_dir="checkpoint/droplet",
    dx=0.25, # 0.16,
    cuda_chunk_size=10,
    nerf_bs=2**15, # 2**17,
    particle_chunk_size=2**9, # 2**10,
    taichi_cuda_memory=0.6, # 0.65,
    N_static=6001,
    entropy_weight=1e-3, #0.001,
    volume_weight=1e-3, # 0.0001,
    # tv_weight = 1e-4,
    # direct_nerf = False, # default?
    hit_frame=4,
    physical_params=dict(global_mu=0.1, global_kappa=0.1),
    write_out=True,
    # random_particles=True, # default?
    kappa=1e3,
    mu=1.0,
    rho=1000,
    N_dynamic=150, # 201,
)

del MPMSimulator
del np
