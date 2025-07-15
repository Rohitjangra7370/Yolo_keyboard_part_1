# Save as scripts/split_train_val.py
import os
import random
import shutil
from tqdm import tqdm

def split_train_validation():
    """Split existing train data into train/validation sets"""
    
    # Paths
    raw_train = "data/raw/dataset_final/train"
    raw_test = "data/raw/dataset_final/test"
    
    # Create destination directories
    os.makedirs("data/images/train", exist_ok=True)
    os.makedirs("data/images/val", exist_ok=True)
    os.makedirs("data/images/test", exist_ok=True)
    os.makedirs("data/labels/train", exist_ok=True)
    os.makedirs("data/labels/val", exist_ok=True)
    os.makedirs("data/labels/test", exist_ok=True)
    
    # Get all images from train folder
    train_images = [f for f in os.listdir(raw_train) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    random.shuffle(train_images)
    
    # Split train into train/val (85%/15%)
    split_point = int(0.85 * len(train_images))
    train_split = train_images[:split_point]
    val_split = train_images[split_point:]
    
    # Copy train split
    for img_name in tqdm(train_split, desc="Copying train images"):
        # Copy image
        src_img = os.path.join(raw_train, img_name)
        dst_img = os.path.join("data/images/train", img_name)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding XML
        xml_name = img_name.rsplit('.', 1)[0] + '.xml'
        src_xml = os.path.join(raw_train, xml_name)
        dst_xml = os.path.join("data/labels/train", xml_name)
        if os.path.exists(src_xml):
            shutil.copy2(src_xml, dst_xml)
    
    # Copy val split
    for img_name in tqdm(val_split, desc="Copying val images"):
        # Copy image
        src_img = os.path.join(raw_train, img_name)
        dst_img = os.path.join("data/images/val", img_name)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding XML
        xml_name = img_name.rsplit('.', 1)[0] + '.xml'
        src_xml = os.path.join(raw_train, xml_name)
        dst_xml = os.path.join("data/labels/val", xml_name)
        if os.path.exists(src_xml):
            shutil.copy2(src_xml, dst_xml)
    
    # Copy test data unchanged
    test_images = [f for f in os.listdir(raw_test) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for img_name in tqdm(test_images, desc="Copying test images"):
        # Copy image
        src_img = os.path.join(raw_test, img_name)
        dst_img = os.path.join("data/images/test", img_name)
        shutil.copy2(src_img, dst_img)
        
        # Copy corresponding XML
        xml_name = img_name.rsplit('.', 1)[0] + '.xml'
        src_xml = os.path.join(raw_test, xml_name)
        dst_xml = os.path.join("data/labels/test", xml_name)
        if os.path.exists(src_xml):
            shutil.copy2(src_xml, dst_xml)
    
    print(f"Split complete:")
    print(f"  Train: {len(train_split)} images")
    print(f"  Val: {len(val_split)} images")
    print(f"  Test: {len(test_images)} images")

if __name__ == "__main__":
    split_train_validation()
