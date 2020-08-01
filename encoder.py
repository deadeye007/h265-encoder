# FFMPEG Encoder Script
# by Andrew Sturm
# Created 2020-04-25

# TODO: Put the os.walk in a separate function to prevent mishaps.

# Import
import argparse, configparser, fnmatch, os, sys, textwrap
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

# Load config.ini into the script
       try:
           config = configparser.ConfigParser()
           config.read('config.ini')
       except FileNotFoundError:
           print("FileNotFoundError: \'config.ini\' was not found and is required to run.\nRename/copy \'config.ini.example\' to \'config.ini\'.")   
           exit()
       pattern = config[settings][pattern]
       extensions = config[settings][extensions]

       for dirpath, subdirs, files in os.walk(workingdir, followlinks=False, topdown=False):
           filelist = []
           for file in files:
               if file in fnmatch.filter(files, pattern):
                     clear() # Just something to do. Nothing important.  
               elif file.endswith(extensions):
                       filelist.append(os.path.join(dirpath, file))
                       matches.append(os.path.join(file))
                       
       for i in range(len(filelist)):
           try:
               infile = filelist[i]
               outfile = os.path.splitext(filelist[i])[0]

               cmd = 'ffmpeg -i "'+infile+'" -c:v libx265 -crf 24 -f mp4 -c:a aac -b:a 128k "'+outfile+'.h265.mkv"'
               print(cmd)
# TURNED OFF FOR DEBUGGING
#               os.system(cmd)
               i = i + 1
                    
           except KeyboardInterrupt:
               print('Exiting due to keyboard interrupt.')
               sys.exit()
           except:
               print('Unrecoverable error occured. Check ffmpeg logs.\n\nExiting...')
               sys.exit()

       print(matches)
            
def main(argv):
    # Check for the correct arguments
    parser = argparse.ArgumentParser(prog='encoder.py', description='Compress your videos with h265.', add_help=False)
    parser.add_argument('--input', help='The directory where your video files to be encoded reside.', dest='workingdir', nargs='?')
    parser.add_argument('--help', help='Get usage help.', nargs=None)
#    parser.add_argument('--version', help='Get program version.', nargs=None)
#    subparsers = parser.add_subparsers(dest='cmd_name')
#    subparsers.add_parser('input')
#    subparsers.add_parser('help')
    
    args = parser.parse_args()

    try:
        if str(args) in "--help":
            parser.print_help(help)

        elif str(args) in "--input":
            print(workingdir)
#            encode(workingdir)

    except FileNotFoundError:
        print("The path or directory does not exist. Please check the path and try again.")
   
#    except:
#        print("Invalid argument.\n\nUsage: encoder.py -in \"/path/to/videos/\"")
#        exit()


# Start the main loop
if __name__ == "__main__":
    if sys.argv[1:] != []:
        main(sys.argv[1:])
    else:
        print("Usage: encoder.py --input \"/path/to/videos/\"")