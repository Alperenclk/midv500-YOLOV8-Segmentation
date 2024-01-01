# For labels
# You have to change path of folder

import os
import json
import random
import shutil
from PIL import Image



root_folder = "< YOUR ROOT PATH >/midv500_data/midv500"             # Yo have to chnage here


def coco_segmentation_to_yolo(annotation, image_width, image_height):
    category_id = 0  
    quad = annotation['quad']

    normalized_quad = [point / dim for pair in quad for point, dim in zip(pair, [image_width, image_height])]
    yolo_data = f"{category_id} {' '.join(map(str, normalized_quad))}\n"

    return yolo_data

def convert_annotations(root_folder):
    output_folder = os.path.join(root_folder, "images")
    os.makedirs(output_folder, exist_ok=True)

    for subdir, dirs, files in os.walk(root_folder):
        if "ground_truth" in subdir:
            subdirs = os.listdir(subdir)
            for sub_dir in subdirs:
                if sub_dir in ["CA", "CS", "HA", "HS", "KA", "KS", "PA", "PS", "TA", "TS"]:
                    sub_dir_path = os.path.join(subdir, sub_dir)
                    for filename in os.listdir(sub_dir_path):
                        if filename.endswith(".json"):
                            json_path = os.path.join(sub_dir_path, filename)
                            with open(json_path, 'r') as json_file:
                                coco_data = json.load(json_file)

                            image_width = 1280  
                            image_height = 1920  

                            yolo_data = coco_segmentation_to_yolo(coco_data, image_width, image_height)

                            
                            output_path = os.path.join(output_folder, f"{filename.replace('.json', '.txt')}")
                            with open(output_path, 'w') as yolo_file:
                                yolo_file.write(yolo_data)

convert_annotations(root_folder)



# For Images
# It converts .tif to .jpg

def convert_tiff_to_jpg(tiff_path, jpg_path):
    # .tiff dosyasını açın ve .jpg formatına dönüştürün
    image = Image.open(tiff_path)
    image = image.convert('RGB')
    image.save(jpg_path+'.jpg')


def convert_tiff_in_subfolders(root_folder):
    images_folder = os.path.join(root_folder, 'images')
    os.makedirs(images_folder, exist_ok=True)
    for subdir, dirs, files in os.walk(root_folder):
            if "images" in subdir:
                subdirs = os.listdir(subdir)
                
                for sub_dir in subdirs:
                    if sub_dir in ["CA", "CS", "HA", "HS", "KA", "KS", "PA", "PS", "TA", "TS"]:
                        sub_dir_path = os.path.join(subdir, sub_dir)
                        for filename in os.listdir(sub_dir_path):
                            if filename.endswith(".tif"):
                                tiff_path = os.path.join(sub_dir_path, filename)
                                image_name = tiff_path.split('/')
                                image_name = image_name[-1]
                                image_name = image_name.split('.')
                                images_save = os.path.join(images_folder,image_name[0])
                                
                                convert_tiff_to_jpg(tiff_path, images_save)
                                
convert_tiff_in_subfolders(root_folder)

# For VALIDATION DATASET

path = '/home/novelty/idcard/yoloSegment/dataset/val'
if not os.path.exists(f'{path}/imagesNew'):
    os.mkdir(f'{path}/imagesNew')
if not os.path.exists(f'{path}/labelsNew'):
    os.mkdir(f'{path}/labelsNew')
files = os.listdir(f'{path}/images')
labels = os.listdir(f'{path}labels')
indexes =random.sample(range(3000), 1000)

for i in indexes:
    shutil.move(path+'/images/'+files[i],f'{path}/imagesNew')
    shutil.move(path+'/labels/'+labels[i],f'{path}labelsNew')