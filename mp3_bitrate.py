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

# set to false for quieter output
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
  mp3list={}
  if os.path.isdir(path):
    filesindir= os.listdir(path)

    for directory, subdirectories, filenames in os.walk(path):
      if filenames != []:
        for filename in filenames:
          if fnmatch.fnmatch(filename, '*.mp3'):
            current_file_name = os.path.join(directory,filename)
            if debug==True:
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
              if bitrate <= 128:
                if debug==True:
                  print("lowQ;%s;%s") %(current_file_name, bitrate)
              elif bitrate >= 128:
                if debug==True:
                  print(" hiQ;%s;%s") %(current_file_name, bitrate)
              if md5sum in mp3list:
                print("duplicated file %s:%s !") %(mp3list[md5sum],md5sum)
              else:
                mp3list[md5sum]=current_file_name
            except mutagen.mp3.HeaderNotFoundError:
              print("%s;corrupted mp3;%s") %(current_file_name, md5sum)
              mp3list['corrupted']=current_file_name
  else:
    print("%s is a file, not a directory") %path

  #print(mp3list)


if __name__ == "__main__":
  indexer(path)
