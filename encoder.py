#!/usr/bin/python3

import argparse, configparser, fnmatch, os, sys
from pathlib import Path

def logo():
    print('''
##############################################################
##############################################################
#
# PYTHON 3
# FFMPEG h265 Encoder v1.0
#
# Created by: Andrew Sturm
# Created on: 2020-04-21
#
##############################################################
##############################################################

''')

def encode(workingdir):
# Declare variables
    matches = []
    filelist = []
      
# Load config.ini into the script
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
    except FileNotFoundError:
        print("FileNotFoundError: \'config.ini\' was not found and is required to run.\nRename/copy \'config.ini.example\' to \'config.ini\'.")   
        exit()

    pattern = config['settings']['pattern']
    fnpattern = ('*'+pattern)
    filepattern = ('.'+pattern)
    extensions = config['settings']['extensions']

# Attempt to run the main process
    for dirpath, subdirs, files in os.walk(workingdir, followlinks=False, topdown=False):
        for file in files:
            if file in fnmatch.filter(files, fnpattern):
                print("'"+file+"' doesn't match pattern. Excluding...")
            elif file.endswith(tuple(extensions)):
                filelist.append(os.path.join(dirpath, file))
    
    for i in range(len(filelist)):
        try:
            infile = filelist[i]
            outfile = os.path.splitext(filelist[i])[0]
    
            cmd = 'ffmpeg -i "'+infile+'" -c:v libx265 -crf 24 -f mp4 -c:a aac -b:a 128k "'+outfile+filepattern+'"'
            os.system(cmd)
            i = i + 1 # Probably not even necessary in Python. Old habits.
                    
        except KeyboardInterrupt:
            print('Exiting due to keyboard interrupt.')
            exit()
        except:
            print('Unrecoverable error occurred. Check ffmpeg logs.\n\nExiting...')
            exit()

#    print(matches)
            
def main(argv):
    # Declare variables
    workingdir = ""

    # Check for the correct arguments
    parser = argparse.ArgumentParser(prog='encoder.py', description='Compress your videos with h265.')
    parser.add_argument('-i', '--input', action="store", help='The directory where your video files to be encoded reside.', dest='workingdir', type=str)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    try:
        if args.workingdir != '':
            encode(args.workingdir)

    except FileNotFoundError:
        print("The path or directory does not exist. Please check the path and try again.")
   
# Start the main loop
if __name__ == "__main__":
    if sys.argv[1:] != []:
        main(sys.argv[1:])
    else:
        print("Usage: encoder.py --input \"/path/to/videos/\"")