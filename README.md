# YOLO to DB Model Format Converter

## Description
This script processes YOLO segmentation data and converts it to the format required by the DB (Differentiable Binarization) model. It transforms relative YOLO coordinates into absolute image coordinates and can optionally draw polygons on the images. The output includes processed text files and optional ground truth files for further use.

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
    git clone https://github.com/redHood08-t/YOLO-to-DB-Converter.git
    cd YOLO-to-DB-Converter
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Make sure you have the necessary dependencies like OpenCV and NumPy installed.

## Usage
1. **Prepare your dataset**: Ensure you have YOLO `.txt` files with segmentation data and corresponding `.png` images in the same directory.
2. **Set input and output paths**: Adjust the file paths in the script to point to your input data and desired output directories:
    ```python
    input_pattern = '/path/to/your/input/files/*.txt'
    output_path = '/path/to/your/output/text_files'
    output_img_path = '/path/to/your/output/images'
    ```

3. **Run the script** to convert YOLO segmentation data into DB model format:
    ```bash
    python yolo_segmentation.py
    ```

4. **Output**: The script will create:
    - Processed text files in the required DB format with absolute polygon coordinates and class labels.
    - Optionally, `.gt` ground truth files.
    - Copies of the original images into the output directory.
    
5. A list of processed images is saved to `test_list.txt` in the output directory.

## Features
- **Convert YOLO segmentation to DB model format**: 
    This script converts YOLO relative segmentation data into absolute coordinates for use with the DB model, making it easier to work with image segmentation tasks.
    
- **Draw polygons on images** *(optional)*: 
    You can draw polygons based on segmentation data on the images for visual verification (commented out by default but easily activated).
    
- **Multiprocessing support**: 
    Uses Python's `multiprocessing.Pool` to process multiple images at once, improving performance with large datasets.
    
- **Progress tracking**: 
    Displays a progress bar using `tqdm` for tracking the processing of files.
    
- **Error handling**: 
    Handles missing files, incorrect formats, and NaN values in segmentation data with clear error messages.

## Contributing
Contributions are welcome! If you'd like to help improve this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a pull request with explanations of your improvements or bug fixes.

Please ensure you write clear commit messages and document your code.

## License
This project is licensed under the MIT License. The full license text can be found in the `LICENSE` file.
