import subprocess
import os
import shutil
import sys

command_dota = './darknet detector test /root/darknet/cfg/dota.data /root/darknet/cfg/yolo-dota.cfg ' \
               '/models/yolo-dota.cfg_450000.weights \
                {0} -dont_show'

command_tiny = './darknet detector test cfg/coco.data cfg/yolov3-tiny.cfg /models/yolov3-tiny.weights \
                {0} -dont_show'

OUTPUT_FILE_PATH = os.getenv('OUTPUT_FILE_PATH', './')


def _run_shell_command(command):
    output = subprocess.check_output(command, shell=True, ).decode("ascii")
    return output


def _save_txt_result(output, image_name):
    with open(os.path.join(OUTPUT_FILE_PATH, f'{image_name}.txt'), 'w+') as f:
        f.write(output)


def _save_predicted_image(image_name):
    source = 'predictions.jpg'
    target = os.path.join(OUTPUT_FILE_PATH, f'{image_name}.jpg')

    assert not os.path.isabs(source)

    # adding exception handling
    try:
        shutil.copy(source, target)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", sys.exc_info())


if __name__ == '__main__':
    images_root = '/root/darknet/images/airplane'
    images = os.listdir(images_root)
    for image in images:
        image_path = os.path.join(images_root, image)
        image_name = image.split('.')[0]
        print(f'current file is {image_path}')
        output = _run_shell_command(command_tiny.format(image_path))
        _save_predicted_image(image_name)
        _save_txt_result(output, image_name)
