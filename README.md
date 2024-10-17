# YOLO Segmentation to Absolute Coordinates and Polygon Drawing

## Description
This script processes YOLO segmentation data, converts relative coordinates into absolute image coordinates, and can optionally draw the resulting polygons onto images. The output includes text files with absolute polygon coordinates and ground truth files.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation
To use this script, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/username/repository_name.git
    cd repository_name
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Make sure that you have OpenCV and NumPy installed on your system.

## Usage
1. **Prepare your dataset**: Ensure you have YOLO `.txt` files with segmentation data and corresponding `.png` images in the same directory.
2. **Set input and output paths**: Adjust the file paths in the script to point to your input data and desired output directories. For example:
    ```python
    input_pattern = '/path/to/your/input/files/*.txt'
    output_path = '/path/to/your/output/text_files'
    output_img_path = '/path/to/your/output/images'
    ```

3. **Run the script** to convert YOLO segmentation data into absolute coordinates:
    ```bash
    python yolo_segmentation.py
    ```

4. **Output**: The script will create:
    - Processed text files with absolute polygon coordinates and class labels.
    - Ground truth files in `.gt` format.
    - Copies of the original images into the output directory.
    
5. A list of processed images is saved to `test_list.txt` in the output directory.

## Features
- **Convert YOLO segmentation to absolute coordinates**: 
    Converts relative segmentation points from YOLO format into absolute pixel coordinates, making it easier to use with other image processing tasks.
    
- **Draw polygons on images** *(optional)*: 
    You can draw polygons based on segmentation data on the images for visual verification (currently commented out in the code, but easily activated).
    
- **Multiprocessing support**: 
    Utilizes Python's `multiprocessing.Pool` to process multiple images simultaneously, improving performance for large datasets.
    
- **Progress tracking**: 
    Displays a progress bar using `tqdm` for better tracking of file processing.
    
- **Error handling**: 
    Provides detailed error handling for missing files, incorrect formats, or NaN values in segmentation data.

## Contributing
Contributions are welcome! If you'd like to improve this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a pull request explaining your improvements or bug fixes.

Please make sure to write clear commit messages and document your code changes.

## License
This project is licensed under the MIT License. You can find the full license text in the `LICENSE` file.
