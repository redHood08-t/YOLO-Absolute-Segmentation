import glob
from pathlib import Path
import math
import shutil
import numpy as np
import cv2
from multiprocessing import Pool, Manager
from tqdm import tqdm

def yolo_segmentation_to_absolute(segmentation_data, img_width, img_height):
    """
    Converts YOLO relative segmentation coordinates to absolute image coordinates.

    Args:
        segmentation_data (list of floats): List of relative YOLO coordinates (x, y).
        img_width (int): Image width.
        img_height (int): Image height.

    Returns:
        list: List of absolute coordinates (x, y) for the polygon.
    """
    absolute_coords = []
    
    # Iterate through segmentation data backwards (Yolo format is reversed)
    for i in range(len(segmentation_data) - 1, 0, -2):
        x = segmentation_data[i - 1] * img_width
        y = segmentation_data[i] * img_height
        if not math.isnan(x) and not math.isnan(y):
            absolute_coords.extend([int(x), int(y)])
        else:
            raise ValueError("Segmentation data contains NaN values")
    
    return absolute_coords

def draw_polygon_on_image(img, polygon_points):
    """
    Draws a polygon on the image given the list of points.

    Args:
        img (numpy array): Image on which to draw the polygon.
        polygon_points (list of int): List of absolute (x, y) coordinates.

    Returns:
        numpy array: Image with the polygon drawn.
    """
    points = np.array([(polygon_points[i], polygon_points[i+1]) for i in range(0, len(polygon_points), 2)], np.int32)
    points = points.reshape((-1, 1, 2))
    img = cv2.polylines(img, [points], isClosed=True, color=(0, 0, 255), thickness=2)
    
    return img

def convert_file(input_path, output_path, output_img_path, progress_queue):
    """
    Processes a single file: converts YOLO segmentation data, and writes the output to the specified location.

    Args:
        input_path (str): Path to the input YOLO text file.
        output_path (str): Path to save the processed output files.
        output_img_path (str): Path to save output images.
        progress_queue (multiprocessing.Queue): Queue to update the progress bar.
    """
    try:
        img_path = input_path.replace('.txt', '.png')
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image file not found or unable to read: {img_path}")

        img_height, img_width = img.shape[:2]

        # Ensure directories exist
        Path(output_path).mkdir(exist_ok=True, parents=True)
        Path(output_img_path).mkdir(exist_ok=True, parents=True)
        shutil.copy(img_path, f'{output_img_path}/{Path(input_path).stem}.png')

        # Process the YOLO segmentation file and save results
        with open(input_path, 'r') as infile, open(f'{output_path}/{Path(input_path).stem}.png.txt', 'w') as outfile:
            for line in infile:
                parts = line.strip().split()
                class_id = parts[0]
                if class_id == '1':  # Skip class_id 1
                    continue
                segmentation_data = list(map(float, parts[1:]))
                absolute_segmentation = yolo_segmentation_to_absolute(segmentation_data, img_width, img_height)
                absolute_segmentation_str = ','.join(map(str, absolute_segmentation))
                outfile.write(f"{absolute_segmentation_str},{class_id}\n")

        # Save the ground truth file (duplicate for now, can be customized)
        with open(input_path, 'r') as infile, open(f'{output_path}/{Path(input_path).stem}.png.gt', 'w') as outfile:
            for line in infile:
                parts = line.strip().split()
                class_id = parts[0]
                if class_id == '1':  # Skip class_id 1
                    continue
                segmentation_data = list(map(float, parts[1:]))
                absolute_segmentation = yolo_segmentation_to_absolute(segmentation_data, img_width, img_height)
                absolute_segmentation_str = ','.join(map(str, absolute_segmentation))
                outfile.write(f"{absolute_segmentation_str},{class_id}\n")

        # Update the progress queue
        progress_queue.put(1)

    except FileNotFoundError as e:
        print(f"File not found: {input_path} - {e}")
    except ValueError as e:
        print(f"Value error in file {input_path}: {e}")
    except Exception as e:
        print(f"An error occurred in file {input_path}: {e}")

def process_files(file_paths, output_path, output_img_path):
    """
    Processes a list of YOLO segmentation files in parallel and displays progress.

    Args:
        file_paths (list of str): List of file paths to process.
        output_path (str): Path to save the processed output.
        output_img_path (str): Path to save output images.
    """
    manager = Manager()
    progress_queue = manager.Queue()
    total_files = len(file_paths)

    with Pool() as pool:
        # Wrap the file processing loop with tqdm for progress tracking
        for _ in tqdm(pool.starmap(convert_file, [(file_path, output_path, output_img_path, progress_queue) for file_path in file_paths]), total=total_files):
            progress_queue.get()

if __name__ == "__main__":
    input_pattern = '/home/abadri/abadri/DB_V2/data/mashintahrir_det_papers/val/*.txt'
    input_files = glob.glob(input_pattern)
    output_path = '/home/abadri/abadri/DB_V2/data/mashintahrir_det_papers_db/test_gts'
    output_img_path = '/home/abadri/abadri/DB_V2/data/mashintahrir_det_papers_db/test_images'

    process_files(input_files, output_path, output_img_path)

    # Generate a list of processed images
    images = glob.glob('/home/abadri/abadri/DB_V2/data/mashintahrir_det_papers_db/test_images/*.png')
    with open('/home/abadri/abadri/DB_V2/data/mashintahrir_det_papers_db/test_list.txt', 'w') as tx:
        for image in images:
            tx.write(f'{Path(image).stem}.png\n')
