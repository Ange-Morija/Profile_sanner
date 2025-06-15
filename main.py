# -*- coding: utf-8 -*-
"""
DigiTwin LIDAR Vehicle Profile Processing
"""

import numpy as np
import os

def reading_lidar(path, translate=False):
    """
    Reads a LIDAR text file and converts polar distances to cartesian (x, y).
    If translate=True, shifts x by 3.84m for the second scanner.
    """
    raw_file = np.loadtxt(path)
    coord_file = []
    for row in raw_file:
        row_xy = compute_xy(row, translate)
        coord_file.append(row_xy)
    return coord_file

def compute_xy(list_distance, translate=False):
    """
    Converts a single scan row of polar distances to (x, y) pairs in mm.
    """
    list_xy = []
    delta_alpha = np.deg2rad(0.5)
    alpha = np.deg2rad(180)  # Starting at 180°, as per assignment!
    for distance in list_distance:
        if distance == 0:
            # skip filtered points
            list_xy.append((0, 0))
        else:
            x = distance * np.cos(alpha)
            y = distance * np.sin(alpha)
            if translate:
                x += 3.84 * 1000  # shift in meters for LIDAR1
            x *= 1000  # meters to mm
            y *= 1000
            list_xy.append((x, y))
        alpha += delta_alpha
    return list_xy

def merge(file_1, file_2, duration, speed):
    """
    Interleaves scan rows from two scanners and assigns Z coordinates.
    """
    nb_1 = len(file_1)
    nb_2 = len(file_2)

    speed_mmps = speed * (1000 / 3.6)  # km/h to mm/s
    length = speed_mmps * duration     # vehicle length in mm

    z_1 = np.linspace(0, length, nb_1).tolist()
    z_2 = np.linspace(0, length, nb_2).tolist()

    merge_data = []
    merge_z = []

    min_len = min(nb_1, nb_2)
    for i in range(min_len):
        merge_data.append(file_1[i])
        merge_data.append(file_2[i])
        merge_z.append(z_1[i])
        merge_z.append(z_2[i])

    if nb_1 > nb_2:
        merge_data.extend(file_1[nb_2:])
        merge_z.extend(z_1[nb_2:])
    elif nb_2 > nb_1:
        merge_data.extend(file_2[nb_1:])
        merge_z.extend(z_2[nb_1:])

    return merge_data, merge_z

def build_cloud(id, duration, speed, base_path="input_data/measurements/"):
    """
    Loads, processes, and merges the two LIDAR files for a vehicle.
    Returns a list of (x, y, z) point tuples in meters.
    """
    file_id = f"{id:02d}"  # e.g., 05
    raw_lidar_0 = os.path.join(base_path, f"LIDAR0_{file_id}.txt")
    raw_lidar_1 = os.path.join(base_path, f"LIDAR1_{file_id}.txt")

    data_from_0 = reading_lidar(raw_lidar_0)
    data_from_1 = reading_lidar(raw_lidar_1, translate=True)

    XY, Z = merge(data_from_0, data_from_1, duration, speed)

    points = []
    for scan_idx, row in enumerate(XY):
        z = Z[scan_idx] / 1000  # to meters
        for x, y in row:
            if x != 0 or y != 0:  # skip zero points
                # Optional: flip Y if needed for your viewer
                points.append([x / 1000000, -y / 1000000, z])  # in meters, Y negated
    return np.array(points)

def compute_dimensions(points):
    """
    Computes width, height, length (in meters) from 3D point cloud.
    """
    xs, ys, zs = points[:,0], points[:,1], points[:,2]
    width = np.max(xs) - np.min(xs)
    height = np.max(ys) - np.min(ys)
    length = np.max(zs) - np.min(zs)
    return width, height, length

def process_all_vehicles(info_path="input_data/vehicle_info.txt",
                         data_path="input_data/measurements/",
                         output_dir="python_helper"):
    """
    Processes all vehicles described in the info file, saves clouds and prints dimensions.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(info_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    dimensions_dict = {}
    points_dict = {}

    print("VehicleID\tWidth (m)\tHeight (m)\tLength (m)")
    for i in range(1, len(lines)):  # skip header
        line = lines[i].strip().split('\t')
        id = int(line[0])
        duration = float(line[1])
        speed = float(line[2])

        try:
            points = build_cloud(id, duration, speed, base_path=data_path)
            width, height, length = compute_dimensions(points)
            
            np.savetxt(f"{output_dir}/Cloud_{id:02d}.txt", points, fmt="%.4f")
            print(f"{id:02d}\t\t{width:.2f}\t\t{height:.2f}\t\t{length:.2f}")
            
             # Adding the dimensiosnto the dictionniary
            dimensions_dict[id] = {"width": width, "height": height, "length": length}
            points_dict[id] = points
            
            # Writing the file of the dimensions
            with open(f"{output_dir}/dimensions.txt", "w", encoding="utf-8") as output:
                output.write("VehicleID\tWidth(m)\tHeight(m)\tLength(m)\n")
                for vid, dims in dimensions_dict.items():
                    output.write(f"{vid}\t{dims['width']:.3f}\t{dims['height']:.3f}\t{dims['length']:.3f}\n")

            
        except Exception as e:
            print(f"Error processing vehicle {id:02d}: {e}")

if __name__ == "__main__":
    process_all_vehicles()
