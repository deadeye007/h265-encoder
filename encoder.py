# encoder.py
# Main encoder script

import argparse
import configparser
import fnmatch
import os
import subprocess
import sys


def encode(working_dir):

    # Declare variables
    file_list = []

    # Load config.ini into the script
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        pattern = config['settings']['pattern']
        fn_pattern = ('*' + pattern)
        file_pattern = ('.' + pattern)
        extensions = config['settings']['extensions']
        const_rate = config['ffmpeg']['const_rate']
        format = config['ffmpeg']['format']
        video_codec = config['ffmpeg']['video_codec']
        audio_codec = config['ffmpeg']['audio_codec']
        audio_bitrate = config['ffmpeg']['audio_bitrate']
        threads = config['ffmpeg']['threads']

    except FileNotFoundError:
        print("FileNotFoundError: \'config.ini\' was not found and is required \
        to run.\nRename/copy \'config.ini.example\' to \'config.ini\'.")
        exit()

    # Attempt to run the main process
    for dir_path, sub_dirs, files in os.walk(working_dir, followlinks=False,
                                             topdown=False):
        for file in files:
            if file in fnmatch.filter(files, fn_pattern):
                print(f"'{file}' doesn't match pattern. Excluding...")
            elif file.endswith(tuple(extensions)):
                file_list.append(os.path.join(dir_path, file))
                print(f"'{file}' matches pattern.")
    for i in range(len(file_list)):
        try:
            in_file = file_list[i]
            out_file = os.path.splitext(file_list[i])[0]

            cmd = f"ffmpeg \
            -i {in_file} \
            -threads {threads} \
            -c:v {video_codec} \
            -crf {const_rate} \
            -f {format} \
            -c:a {audio_codec} \
            -b:a {audio_bitrate} \
            {out_file}{file_pattern}"
            subprocess.run(cmd, shell=True)
            i = i + 1

        except KeyboardInterrupt:
            print('Exiting due to keyboard interrupt.')
            exit()

        else:
            print('Unrecoverable error occurred. Check ffmpeg logs. Exiting...')
            exit()


def main(argv):
    # Declare variables
    working_dir = ""

    # Check for the correct arguments
    parser = argparse.ArgumentParser(prog='encoder.py',
                                     description='Compress your videos with \
                                     h265.')
    parser.add_argument('-i', '--input', action="store",
                        help='The directory where your video files to be \
                        encoded reside.', dest='working_dir', type=str)
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    try:
        if args.working_dir != '':
            encode(args.working_dir)

    except FileNotFoundError:
        print("The path or directory does not exist. Please check the path and \
        try again.")


# Start the main loop
if __name__ == "__main__":
    if sys.argv[1:] != []:
        main(sys.argv[1:])
    else:
        print("Usage: encoder.py --input \"/path/to/videos/\"")
