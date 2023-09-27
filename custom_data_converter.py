import sys
import os
import json
import numpy as np

# test: python custom_data_converter.py /home/stefano/Data/fluid_sym_data/duck


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

    # fps defines the delta time
    fps = 60
    delta_t = 1.0 / fps

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

            params_path = os.path.join(folder_path, "params.json")
            params = json.load(open(params_path, "r"))
            c2w = np.array(params["c2w"])
            intrinsic = np.array(params["intrinsic"])
            print("c2w", c2w)
            print("intrinsic", intrinsic)

            for file in files:
                if "frame" in file:
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
                    "file_path": os.path.join("data", output_img),
                    "time": delta_t_mult * delta_t,
                    "c2w": c2w.tolist(),
                    "intrinsic": intrinsic.tolist(),
                }
                all_data.append(data)

    # save all_data as json
    all_data_path = os.path.join(output_folder_path, "all_data.json")
    with open(all_data_path, "w") as f:
        json.dump(all_data, f, indent=4)


if __name__ == "__main__":
    main()
