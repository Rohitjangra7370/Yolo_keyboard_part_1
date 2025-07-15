import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

def get_keyboard_classes():
    """Define all keyboard key classes exactly as found in your XMLs."""
    return [
        '0','1','2','3','4','5','6','7','8','9',
        'a','accent','ae','alt-left','altgr-right',
        'b','c','caret','comma','d','del','e','enter',
        'f','g','h','hash','i','j','k','keyboard','l',
        'less','m','minus','n','o','oe','p','plus',
        'point','q','r','s','shift-left','shift-lock',
        'shift-right','space','ss','strg-left','strg-right',
        't','tab','u','ue','v','w','x','y','z'
    ]

def convert_box(img_size, box):
    """Convert Pascal VOC box to YOLO format."""
    dw = 1.0 / img_size[0]
    dh = 1.0 / img_size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x * dw, y * dh, w * dw, h * dh

def convert_annotation(xml_file, txt_file, classes):
    """Convert one XML annotation into YOLO `.txt` format."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    yolo_lines = []
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in classes:
            print(f"Warning: Unknown class '{class_name}' in {xml_file}")
            continue
        class_id = classes.index(class_name)
        bnd = obj.find('bndbox')
        xmin = float(bnd.find('xmin').text)
        xmax = float(bnd.find('xmax').text)
        ymin = float(bnd.find('ymin').text)
        ymax = float(bnd.find('ymax').text)
        x_center, y_center, w, h = convert_box(
            (img_width, img_height), (xmin, xmax, ymin, ymax)
        )
        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    with open(txt_file, 'w') as f:
        f.write('\n'.join(yolo_lines))

def convert_data():
    """Convert all XML files in train/val/test splits to YOLO format."""
    classes = get_keyboard_classes()
    for split in ['train', 'val', 'test']:
        xml_dir = f"data/labels/{split}"
        if not os.path.isdir(xml_dir):
            print(f"Skipping {split} – directory not found")
            continue
        xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
        for xml_file in tqdm(xml_files, desc=f"Converting {split}"):
            xml_path = os.path.join(xml_dir, xml_file)
            txt_path = os.path.join(xml_dir, xml_file.replace('.xml', '.txt'))
            try:
                convert_annotation(xml_path, txt_path, classes)
            except Exception as e:
                print(f"Error converting {xml_file}: {e}")
    print(f"Conversion complete! Total classes: {len(classes)}")
    return classes

if __name__ == "__main__":
    convert_data()
