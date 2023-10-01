import sys
import os
import json
import numpy as np

# test: python custom_data_converter.py /home/stefano/Data/fluid_sym_data/duck


def rot_x(theta):
    return np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])


def rot_y(theta):
    return np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])


def rot_z(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])


def lookat(eye, target, up):
    z = eye - target
    z = z / np.linalg.norm(z)
    x = np.cross(up, z)
    x = x / np.linalg.norm(x)
    y = np.cross(z, x)
    y = y / np.linalg.norm(y)
    return np.vstack((x, y, z)).T


def main():
    # input data folder
    input_folder_path = sys.argv[1]
    print("input folder path", input_folder_path)

    # make sure input folder path exists
    if not os.path.exists(input_folder_path):
        raise ValueError("input folder path does not exist")

    input_folder = os.path.basename(input_folder_path)
    print("input folder", input_folder)

    # output data folder
    output_folder_path = os.path.join("data", input_folder)
    print("output folder path", output_folder_path)

    # delete output folder if it exists, create if it does not exist
    if os.path.exists(output_folder_path):
        os.system("rm -rf {}".format(output_folder_path))
    os.mkdir(output_folder_path)

    # create all_data.json
    all_data = []

    #
    nr_original_frames = 60  # TODO: read from input data
    select_one_every = 5  # TODO: make this a parameter
    nr_frames = (nr_original_frames // select_one_every) + 1
    print("nr_original_frames", nr_original_frames)
    print("select_one_every", select_one_every)
    print("nr_frames", nr_frames)

    # fps defines the delta time
    fps = nr_frames
    delta_t = 1.0 / fps
    print("delta_t", delta_t)

    # center cameras (shift)
    shift = np.array([0.0, 0.0, 1.0])

    # get all Rt and intrinsic
    Rt_all = []
    intrinsic_all = []
    camera_idxs = []
    for folder in os.listdir(input_folder_path):
        # if folder name contains "camera"
        if "camera" in folder:
            cam_idx = int(folder.split("_")[1])
            camera_idxs.append(cam_idx)
            folder_path = os.path.join(input_folder_path, folder)
            params_path = os.path.join(folder_path, "params.json")
            params = json.load(open(params_path, "r"))
            t = np.array(params["Rt"])[:3, 3] + shift
            Rt = np.eye(4)
            Rt[:3, 3] = t
            # compute R from lookat
            Rt[:3, :3] = lookat(
                t,
                np.array([0, 0, 0]),
                np.array([0, 0, 1]),
            )
            intrinsic = np.array(params["intrinsic"])
            # print("Rt", Rt)
            # print("intrinsic", intrinsic)
            Rt_all.append(Rt)
            intrinsic_all.append(intrinsic)
    # order Rt_all and intrinsic_all by camera_idxs
    Rt_all = [Rt_all[i] for i in np.argsort(camera_idxs)]
    intrinsic_all = [intrinsic_all[i] for i in np.argsort(camera_idxs)]

    # world axis transform
    axis_rot = rot_x(-np.pi / 2)
    axis_transform = np.eye(4)
    axis_transform[:3, :3] = axis_rot

    # apply to every Rt
    for i in range(len(Rt_all)):
        Rt_all[i] = np.matmul(axis_transform, Rt_all[i])

    Rt_all = np.array(Rt_all)
    intrinsic_all = np.array(intrinsic_all)
    # print("Rt_all", Rt_all.shape)
    # print("intrinsic_all", intrinsic_all.shape)

    # get poses centers
    # centers = Rt_all[:, :3, 3]
    # print("centers", centers)
    # dists = np.linalg.norm(centers, axis=1)
    # print(dists)
    # find mean
    # mean_center = np.mean(centers, axis=0)
    # print("mean_center", mean_center)
    # # shift all poses by -mean_center
    # Rt_all[:, :3, 3] -= mean_center

    # # scale to unit sphere
    # centers = Rt_all[:, :3, 3]
    # # find distance from origin
    # dists = np.linalg.norm(centers, axis=1)
    # print("centers distances", dists)

    # for each camera_i folder in input folder
    data_path = os.path.join(output_folder_path, "data")
    os.makedirs(data_path)
    for folder in os.listdir(input_folder_path):
        # if folder name contains "camera"
        if "camera" in folder:
            cam_idx = int(folder.split("_")[1])
            print("cam_idx", cam_idx)
            # for each frame_i folder in camera_i folder
            folder_path = os.path.join(input_folder_path, folder)
            files = os.listdir(folder_path)
            files.sort()
            img_idx = 0
            imgs_counter = 0

            Rt = Rt_all[cam_idx][:3, :4]
            intrinsic = intrinsic_all[cam_idx]
            # params_path = os.path.join(folder_path, "params.json")
            # params = json.load(open(params_path, "r"))
            # Rt = np.array(params["Rt"])
            # intrinsic = np.array(params["intrinsic"])
            # print("Rt", Rt)
            # print("intrinsic", intrinsic)

            for file in files:
                if "params" in file:
                    continue
                if "frame" in file:
                    # if not a selected frame
                    print("imgs_counter", imgs_counter)
                    if imgs_counter % select_one_every != 0:
                        # skip loop iteration
                        imgs_counter += 1
                        continue
                    imgs_counter += 1

                    # if a selected frame
                    output_img = f"r_{cam_idx}_{img_idx}.png"
                    img_idx += 1
                    delta_t_mult = img_idx
                if "background" in file:
                    output_img = f"r_{cam_idx}_{-1}.png"
                    delta_t_mult = -1

                input_img_path = os.path.join(folder_path, file)
                output_img_path = os.path.join(data_path, output_img)

                # copy image to output folder
                print("copying image", input_img_path, output_img_path)
                os.system(f"cp {input_img_path} {output_img_path}")

                data = {
                    "file_path": os.path.join(".", "data", output_img),
                    "time": delta_t_mult * delta_t,
                    "c2w": Rt.tolist(),
                    "intrinsic": intrinsic.tolist(),
                }
                all_data.append(data)

    # save all_data as json
    all_data_path = os.path.join(output_folder_path, "all_data.json")
    with open(all_data_path, "w") as f:
        json.dump(all_data, f, indent=4)


if __name__ == "__main__":
    main()
