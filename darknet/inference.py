import subprocess
import os
import shutil
import sys

command_dota = './darknet detector test ./cfg/dota.data ./cfg/yolo-dota.cfg ' \
               '/models/yolo-dota.cfg_450000.weights \
                {0} -dont_show'

command_tiny = './darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg ' \
               '/models/yolov3-tiny.weights \
                {0} -dont_show'

COMMAND = command_dota
OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH', './')


def _run_shell_command(command):
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


def exist(image_path_predicted):
    return os.path.exists(image_path_predicted)


def run():
    images_root = '/root/darknet/images/airplane'
    images = os.listdir(images_root)
    for image in images:
        image_path = os.path.join(images_root, image)
        image_name = image.split('.')[0]
        image_path_predicted = os.path.join(OUTPUT_FILE_PATH, f'{image_name}.jpg')
        if exist(image_path_predicted):
            print(f'{image_path} is already predicted, now skip it.')
        else:
            print(f'{image_path} is not predicted, start to predict it.')
            output = _run_shell_command(COMMAND.format(image_path))
            _copy_file('predictions.jpg', image_path_predicted)
            _save_txt_result(output, image_name)
