import glob
import json
import os
import shutil
import subprocess
import sys
import time

from PIL import Image

"""
assume the image_name doesn't contains '.', export file format:
20210326_120658.image_name.json
20210326_120658.image_name.txt
20210326_120658.image_name.001.jpg
20210326_120658.image_name.002.jpg 
"""
JSON_FILE_SPLIT_COUNT = 3
JSON_FILE_IMAGE_INDEX = 1
MAX_FRAME_COUNT = 20
GSD_CSV_FILE = '/root/darknet/images/dota_gsd.csv'
CONFIDENCE_THRESHOLD = 0.5
FACTOR = 0.2
GSD_VALUE = 0.126281619876

command_dota = './darknet detector test ./cfg/dota.data ./cfg/yolo-dota.cfg ' \
               '/models/yolo-dota.cfg_450000.weights \
                {0} -dont_show -out result.json'

command_tiny = './darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg ' \
               '/models/yolov3-tiny.weights \
                {0} -dont_show -out result.json'

OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH', './')
IMAGES_ROOT_PATH = os.getenv('IMAGES_ROOT_PATH', '/root/darknet/images/tennis-court')
COMMAND_LINE = os.getenv('COMMAND_LINE', 'dota')
INFERENCE_COMMAND = {
    'dota': command_dota,
    'tiny': command_tiny,
}.get(COMMAND_LINE, command_dota)

command_latest_one_json_file = f"ls {OUTPUT_FILE_PATH}/*.json | head -1"
command_remove_oldest_files = f"ls -t {OUTPUT_FILE_PATH}/*.json | sed -e '1,{MAX_FRAME_COUNT}d' | cut -b 1-15" \
                              f"| xargs -d '\\n' -i sh -c 'rm {{}}*' "


def _shell(command):
    print(f'cmd=[{command}]')
    output = subprocess.check_output(command, shell=True, ).decode("ascii")
    return output


def _save_txt_result(output, image_name):
    with open(os.path.join(OUTPUT_FILE_PATH, f'{image_name}.txt'), 'w') as f:
        f.write(output)


def _copy_file(source, target):
    try:
        shutil.copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


def _exist(image_path_predicted):
    return os.path.exists(image_path_predicted)


def _delete_oldest_files_if_is_full():
    listing = glob.glob(f'{OUTPUT_FILE_PATH}/*.json')
    if len(listing) >= MAX_FRAME_COUNT:
        oldest_file = min(listing, key=os.path.getctime)
        time_prefix = oldest_file.split('/')[-1].split('.')[0]
        to_be_remove = glob.glob(f'{OUTPUT_FILE_PATH}/{time_prefix}*')
        for f in to_be_remove:
            try:
                os.remove(f)
            except:
                print("Error while deleting file : ", f)


def _calculate_area_and_crop_images(json_file, prefix, gsd_v=0.0):
    with open(json_file, 'r') as f:
        json_dict = json.load(f)
    image = Image.open(json_dict[0]['filename'])
    width, height = image.size

    with open(f'{prefix}.csv', 'w') as f:
        for i, obj in enumerate(json_dict[0]['objects']):
            name = obj['name']
            center_x = obj['relative_coordinates']['center_x'] * width
            center_y = obj['relative_coordinates']['center_y'] * height
            w = obj['relative_coordinates']['width'] * width
            h = obj['relative_coordinates']['height'] * height
            confidence = obj['confidence']
            x = int(center_x - w / 2.0)
            y = int(center_y - h / 2.0)
            w = int(w)
            h = int(h)
            print(i, name, x, y, w, h, confidence)

            # save crop_image
            if confidence < CONFIDENCE_THRESHOLD:
                box = (x, y, x + w, y + h)
                crop = image.crop(box)
                print(f"{prefix}.{i:04}.jpg")
                crop.save(f"{prefix}.{i:04}.jpg")
                # crop_img = image[y:y + h, x:x + w]
                # cv2.imwrite(f"{prefix}.{i:04}.jpg", crop_img)

            real_w = w * gsd_v * FACTOR
            real_h = h * gsd_v * FACTOR
            area = real_h * real_w

            line = f'{i:04}, {area}, {real_h}, {real_w}'
            print(line, file=f)


def run():
    images_root = IMAGES_ROOT_PATH
    images = os.listdir(images_root)
    images.sort()
    images_len = len(images)

    # find the last inference image
    newest_file = _shell(command_latest_one_json_file).split('.')
    if len(newest_file) != JSON_FILE_SPLIT_COUNT:
        index = -1
        print(f'there is no output in output_path')
    else:
        image_name = newest_file[JSON_FILE_IMAGE_INDEX]
        index = [x.split('.')[-2] for x in images].index(image_name)
        print(f'image_name is {image_name}, index is {index}')

    # read gsd.csv for area calculation
    # TODO: maybe it is different for each image

    # circle loop all the images
    while True:
        index = (index + 1) % images_len
        image = images[index]

        cur_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        image_path = os.path.join(images_root, image)
        image_name = image.split('.')[0]

        json_path_predicted = os.path.join(OUTPUT_FILE_PATH, f'{cur_time}.{image_name}.json')

        _shell(INFERENCE_COMMAND.format(image_path))
        _delete_oldest_files_if_is_full()
        _copy_file('result.json', json_path_predicted)
        crop_image_prefix = f'{OUTPUT_FILE_PATH}/{cur_time}.{image_name}'
        _calculate_area_and_crop_images('result.json', crop_image_prefix, gsd_v=GSD_VALUE)
