# 🧠 YOLO Keyboard Part 1  
**Custom YOLOv8 Object Detection for Keyboard Key Classification**

This project provides scripts and configuration for converting a labeled keyboard dataset from Pascal VOC format to YOLOv8 format, splitting the data into train/validation/test sets, and preparing for training a YOLOv8 model to detect and classify individual keyboard keys. The dataset focuses on 60 unique keyboard key classes.

The repository includes helper scripts, a dataset configuration file, and a structure reference. Note that the `data/` folder (containing raw and processed datasets) is excluded from the repository via `.gitignore` to avoid uploading large files.

## 📂 Repository Structure

Based on the analyzed directory:

```
└── rohitjangra7370-yolo_keyboard_part_1/
    ├── README.md               ← This file (project documentation)
    ├── data.yaml               ← YOLOv8 dataset configuration file
    ├── structure.txt           ← Reference folder structure for the project
    └── scripts/
        ├── convert_voc_to_yolo.py ← Script to convert Pascal VOC XML annotations to YOLO TXT format
        └── split_train_val.py    ← Script to split raw dataset into train/val/test sets
```

For a more detailed recommended project structure (including optional elements like virtual environment and training script), refer to `structure.txt`:

```
~/yolo_keyboard_project/
├── venv/                   ← Python virtual environment
├── data/                   ← Raw and split images+annotations
│   ├── raw/                ← Downloaded Kaggle dataset: images + XMLs
│   ├── images/             ← Split image files
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── labels/             ← Converted YOLO TXT labels
│       ├── train/
│       ├── val/
│       └── test/
├── scripts/                ← Helper Python scripts
│   ├── split_data.py       ← (Note: Actual file is split_train_val.py)
│   └── convert_voc_to_yolo.py
├── data.yaml               ← YOLOv8 dataset config
└── train_yolo.sh           ← Shell script to launch training
```

*Notes on structure:*
- The `data/` folder is not included in the repository but should be created locally.
- Use a `.gitkeep` file if you need to track empty directories in Git.
- The structure assumes a root project folder like `yolo_keyboard_project/`, but the repository is named `rohitjangra7370/yolo_keyboard_part_1`.

## 🔗 Dataset & Preparation

The project uses a keyboard dataset in Pascal VOC format (images + XML annotations). Download the dataset from sources like Kaggle or the provided Google Drive link (if available). For example:

📥 **Download the dataset archive** from Google Drive:  
[**Download archive.zip (dataset_final)**](https://drive.google.com/drive/folders/1OmSOyWVL7AtxDsxprQzkF2bjdKDrnQdn?usp=sharing)

> The Drive folder contains:
> - `archive.zip`: Zipped version of the `dataset_final` folder (images + XMLs)
> - Sample detection results for Part 1 (before/after images)

After downloading, unzip and place the contents in `data/raw/dataset_final/` with subfolders:
- `train/` (original training images and XMLs)
- `test/` (original test images and XMLs)

The dataset will be split into train/val/test (85%/15% split for the original train data) using the provided script.

## 🧠 Classes

The model detects **60 unique keyboard keys**. The full list of classes is defined in `data.yaml` and the conversion script:

- '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
- 'a', 'accent', 'ae', 'alt-left', 'altgr-right'
- 'b', 'c', 'caret', 'comma', 'd', 'del', 'e', 'enter'
- 'f', 'g', 'h', 'hash', 'i', 'j', 'k', 'keyboard', 'l'
- 'less', 'm', 'minus', 'n', 'o', 'oe', 'p', 'plus'
- 'point', 'q', 'r', 's', 'shift-left', 'shift-lock'
- 'shift-right', 'space', 'ss', 'strg-left', 'strg-right'
- 't', 'tab', 'u', 'ue', 'v', 'w', 'x', 'y', 'z'

These classes match those found in the XML annotations. You can customize the number of classes or labels by editing `data.yaml`.

## ⚙️ Setup Instructions

### 1. 📦 Install Dependencies
Ensure you have Python 3.8+ installed. Create a virtual environment (optional, as suggested in `structure.txt`):

```bash
python -m venv venv
source venv/bin/activate  # On Unix/Mac
# or venv\Scripts\activate on Windows
```

Install required packages:

```bash
pip install ultralytics tqdm
```

- `ultralytics`: For YOLOv8 model training.
- `tqdm`: For progress bars in scripts.

### 2. 🧪 Prepare the Dataset
Download and place the raw dataset in `data/raw/dataset_final/` as described above.

Run the splitting script to create train/val/test sets:

```bash
python scripts/split_train_val.py
```

*Script Details (`split_train_val.py`):*
- Imports: `os`, `random`, `shutil`, `tqdm`.
- Function: `split_train_validation()`.
- Paths: Reads from `data/raw/dataset_final/train` and `data/raw/dataset_final/test`.
- Creates directories: `data/images/{train,val,test}` and `data/labels/{train,val,test}`.
- Splits original train data: 85% to train, 15% to val (random shuffle).
- Copies images and corresponding XMLs.
- Copies test data unchanged.
- Outputs: Prints split counts (e.g., "Train: X images", "Val: Y images", "Test: Z images").

This script handles images with extensions `.jpg`, `.jpeg`, `.png` and their matching `.xml` files.

### 3. 🔄 Convert Annotations to YOLO Format
Convert Pascal VOC XML labels to YOLO TXT format:

```bash
python scripts/convert_voc_to_yolo.py
```

*Script Details (`convert_voc_to_yolo.py`):*
- Imports: `os`, `xml.etree.ElementTree as ET`, `tqdm`.
- Functions:
  - `get_keyboard_classes()`: Returns the list of 60 classes (matches `data.yaml`).
  - `convert_box(img_size, box)`: Converts VOC bounding box to YOLO format (center x/y, width/height normalized).
  - `convert_annotation(xml_file, txt_file, classes)`: Parses XML, extracts objects, converts boxes, and writes YOLO lines (e.g., "class_id x_center y_center width height").
  - `convert_data()`: Processes train/val/test splits, converts all XMLs in `data/labels/{split}`, skips unknown classes with warnings, handles errors.
- Output: Prints "Conversion complete! Total classes: 60" and generates `.txt` files alongside XMLs.

### 4. 🚀 Train YOLOv8 Model
Use the `data.yaml` configuration for training:

*`data.yaml` Details:*
- `path: data` (root dataset path).
- `train: images/train` (relative path to train images).
- `val: images/val` (relative path to validation images).
- `test: images/test` (relative path to test images).
- `nc: 60` (number of classes).
- `names:` (array of 60 class names, as listed above).

Run training (example command; adjust as needed):

```bash
yolo task=detect mode=train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640
```

For automation, consider adding a shell script like `train_yolo.sh` as suggested in `structure.txt`.

## 🖼️ Sample Results
After training, evaluate results on test images. Place sample before/after detection images in an `assets/` folder or link from Google Drive.

Example placeholders:
- 📸 Original Image
- 🎯 YOLO Prediction

(Upload your own results to the repository or Drive for previews.)

## 📌 Notes
- The `data/` folder is excluded from Git using `.gitignore` to prevent uploading large datasets.
- If directories are empty, add `.gitkeep` files to track them in Git.
- Customize classes, paths, or splits by editing `data.yaml` or scripts.
- The repository analyzed includes 5 files with an estimated 2.1k tokens.
- Potential discrepancies: `structure.txt` references `split_data.py` and `train_yolo.sh`, which are not in the repository (use `split_train_val.py` instead; add `train_yolo.sh` if needed).
- For issues with unknown classes during conversion, check XMLs against the defined classes list.

## 📬 Contact
Made with 💻 by Rohit Jangra.  
Repository: [rohitjangra7370/yolo_keyboard_part_1](https://github.com/rohitjangra7370/yolo_keyboard_part_1)  

Let me know if you need further customizations, such as generating previews from Drive images.
