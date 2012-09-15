#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mp3_bitrate.py 

import os, sys, hashlib, fnmatch

try:
  from mutagen.mp3 import MP3
  import mutagen
except ImportError:
  print("install mutagen!!\non Debian like distributions, you can do: apt-get install python-mutagen")
  sys.exit(1)

# set to false for quiet output
#debug = True 
debug = False 


# TODO
# store info in sqlite or so 
# by now, > to a file does it.

if len(sys.argv) > 1:
  path=sys.argv[1]
else:
  print("usage: %s /path/to/mp3s/") %sys.argv[0]
  sys.exit(1)

def indexer(path):
  if os.path.isdir(path):
    filesindir= os.listdir(path)

    for directory, subdirs, filenames in os.walk(path):
      if filenames != []:
        for filename in filenames:
          if fnmatch.fnmatch(filename, '*.mp3'):
            current_file_name = os.path.join(directory,filename)
            print current_file_name
            f = open(current_file_name, 'rb')
            h = hashlib.md5()
            h.update(f.read())
            md5sum = h.hexdigest()
            f.close()
            try:
              input_file = MP3(current_file_name)
              raw_bitrate = input_file.info.bitrate
              bitrate = (raw_bitrate / 1000)
              if debug == True:
               print("%s; %s; %s") %(current_file_name, bitrate, md5sum)
            except mutagen.mp3.HeaderNotFoundError:
              print("corrupted mp3")
      
  else:
    print("%s is file") %path


if __name__ == "__main__":
  indexer(path)
