import os
import shutil
import sys

SCRIPT_FILE_PATH = os.getenv('SCRIPT_FILE_PATH')

if __name__ == '__main__':
    if SCRIPT_FILE_PATH is not None:
        print(f'SCRIPT_FILE_PATH is {SCRIPT_FILE_PATH}, copy to current dir.')
        new_script = os.path.join(SCRIPT_FILE_PATH, 'inference.py')

        try:
            shutil.copy(new_script, './')
        except IOError as e:
            print(f'no inference.py in SCRIPT_FILE_PATH, using default inference.py')
        except:
            print("Unexpected error:", sys.exc_info())

    else:
        print(f'SCRIPT_FILE_PATH is None, using default inference.py')
    from inference import run

    run()
