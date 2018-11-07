import shutil
import os
import time

RICO_DIR = 'E:\\rico-dataset\\combined'
OUTPUT_DIR = 'E:\\sketches-test\\rico-data'

NUM_PER_DIR = 1000


def copy_file(src_path, dst_path):
    if not os.path.isfile(src_path):
        print(src_path, "not exist!")
    else:
        fpath, fname = os.path.split(dst_path)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.copyfile(src_path, dst_path)
        # print('copy', src_path, '>', dst_path)


if __name__ == '__main__':

    start_time = time.time()

    # 检查输出文件夹状态
    if not os.path.exists(OUTPUT_DIR):
        print('### Making root directory to save classified directories ... OK')
        os.makedirs(OUTPUT_DIR)
    print('### Checking root directory to save classified directories ... OK')

    num_files = int(len(os.listdir(RICO_DIR)) / 2)

    i = 0
    while i < num_files:
        dir_path = os.path.join(OUTPUT_DIR, str(i) + '-' + str(i + NUM_PER_DIR - 1)) \
            if i + NUM_PER_DIR - 1 < num_files else os.path.join(OUTPUT_DIR, str(i) + '-' + str(num_files - 1))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        i = i + NUM_PER_DIR
    print('### RICO directories created. Each directory contains', NUM_PER_DIR, 'files.')

    for dir_name in os.listdir(OUTPUT_DIR):
        if os.path.isdir(os.path.join(OUTPUT_DIR, dir_name)):
            print('>>> Creating directory', dir_name, '...', end=' ')
            beg_index = int(dir_name.split('-')[0])
            end_index = int(dir_name.split('-')[1])
            for i in range(beg_index, end_index + 1):
                copy_file(os.path.join(RICO_DIR, str(i) + '.json'),
                          os.path.join(OUTPUT_DIR, dir_name, str(i) + '.json'))
                copy_file(os.path.join(RICO_DIR, str(i) + '.jpg'),
                          os.path.join(OUTPUT_DIR, dir_name, str(i) + '.jpg'))
            print('OK')
    print('---------------------------------')
    print('Duration: {:.2f} s'.format(time.time() - start_time))