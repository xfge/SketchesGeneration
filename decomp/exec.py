import os
import shutil
import subprocess
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

apk_dir = cfg.get('decode', 'apk_dir')
temp_dir = cfg.get('decode', 'temp_dir')
token_file_dir = cfg.get('decode', 'token_file_dir')

soot_output = cfg.get('decode', 'soot_output')

TIME_OUT = 240


def remove_dir(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)


if __name__ == '__main__':

    for file in os.listdir(apk_dir):
        if file.endswith('.apk'):
            print('---------------------------------------------')

            file_name = os.path.splitext(file)[0]
            apk_path = os.path.join(apk_dir, file)
            apktool_out_path = os.path.join(temp_dir, file_name)

            subprocess.call(['apktool', 'd', apk_path, '-f', '-o', apktool_out_path])

            # 检查 apktool decode 结果文件状态
            if not os.path.isdir(apktool_out_path):
                print('E: Apktool decoding failed.')
                continue

            # 执行 soot 程序
            if not os.path.exists(soot_output):
                os.makedirs(soot_output)
            # todo sootrun 路径
            cmd = ['java', '-jar', '/Users/gexiaofei/soot/SootRun/out/artifacts/SootRun_jar/SootRun.jar',
                   '-d', soot_output,
                   '-android-jars', cfg.get('decode', 'android_jars'),
                   '-package', file_name,
                   '-process-dir', apk_path,
                   '-apktool-dir', apktool_out_path,
                   '-token-dir', token_file_dir,
                   '-process-multiple-dex', '-allow-phantom-refs']

            print('I: Entering another thread to perform soot analysis (time out = ' + str(TIME_OUT) + 's).',
                  'Execution output will be shown until the subprocess ended.')
            try:
                out_bytes = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=240)
            except subprocess.TimeoutExpired as e:
                # 处理超时异常
                print(str(e.output, encoding='utf-8'))
                print('E:', type(e), 'Soot analysis times out >>> Skip', file)
            except subprocess.CalledProcessError as e:
                # 处理调用失败异常
                print(str(e.output, encoding='utf-8'))
                print('E:', type(e))
            else:
                print(str(out_bytes, encoding='utf-8'))
            finally:
                print('I: Finished. Removing intermediate files (Apktool files) ...')
                # 使用完毕后删除 apktool 生成目录
                remove_dir(apktool_out_path)
                remove_dir(soot_output)
