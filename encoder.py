# FFMPEG Encoder Script
# by Andrew Sturm
# Created 2020-04-25

# TODO: Put the os.walk in a separate function to prevent mishaps.

# Import
import sys, textwrap, os, fnmatch
from pathlib import Path

# Set window size.
os.system('mode con: cols=125 lines=30')

def clear():
    # Clear command for Windows
    if os.name == 'nt':
        _ = os.system('cls')

        # Clear command for Mac/*nix
    else:
        _ = os.system('clear')

def title():
    clear()
    titleFull = '*'
    title = '   FFMPEG h265 Encoder v1.0   '
    subtitle = '   h265 Encoder for Data Hoarding   '
    author = '   BY: ANDREW STURM   '
    date = '   CREATED ON: 2020-21-04   '
    space = 0

    for x in range(0,3):
        print(titleFull.center(125,'*'))
    print(title.center(125,'*'))
    print(titleFull.center(125, '*'))
    print(subtitle.center(125, '*'))
    print(titleFull.center(125, '*'))
    print(author.center(125,'*'))
    print(titleFull.center(125, '*'))
    print(date.center(125, '*'))
    for x in range(0,3):
        print(titleFull.center(125, '*'))
    while space != 16:
        print('')
        space = space + 1

def encode(workingdir):
       pattern = '*h265.mkv'
       matches = []
   
       for dirpath, subdirs, files in os.walk(workingdir, followlinks=False, topdown=False):
           filelist = []
           for file in files:
               if file in fnmatch.filter(files, pattern):
                     clear() # Just something to do. Nothing important.  
               elif file.endswith((".mkv",".mp4",".avi")):
                       filelist.append(os.path.join(dirpath, file))
                       matches.append(os.path.join(file))
                       
       for i in range(len(filelist)):
           try:
               infile = filelist[i]
               outfile = os.path.splitext(filelist[i])[0]

               cmd = 'ffmpeg -i "'+infile+'" -c:v libx265 -crf 24 -f mp4 -c:a aac -b:a 128k "'+outfile+'.h265.mkv"'
               print(cmd)
               os.system(cmd)
               i = i + 1
                    
           except KeyboardInterrupt:
               print('Exiting due to keyboard interrupt.')
               sys.exit()
           except:
               print('Unrecoverable error occured. Check ffmpeg logs.\n\nExiting...')
               sys.exit()

       print(matches)
            
def main():
   clear()
   title()
   workingdir = input("Please enter your working directory:\n")
   encode(workingdir)

main()
