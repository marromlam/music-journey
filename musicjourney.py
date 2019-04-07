# -*- coding: utf-8 -*-

################################################################################
#                                                                              #
#                               Music Journey                                  #
#                                                                              #
#       Author: Marcos Romero                                                  #
#   Created on: 6th April 2019                                                 #
#                                                                              #
#    This is a very simple python3 code to download CSV-Spotify-playlists.     #
#    You need eyed3 package and also youtube-dl. Just that!
#                                                                              #
#   To run this, simply launch your terminal, cd to this file folder and       #
#   then run:
#      $ python3 magicjourney.py --list [your playlist csv]                    #
#                                                                              #
################################################################################



################################################################################
# Loading packages and libraries ###############################################

import sys                                                             # default
import csv                                                             # default
import urllib                                                          # default
import urllib.request                                                  # default
import re                                                              # default
import subprocess                                                      # default
import os                                                              # default
import argparse                                                        # default

import eyed3           # pip3 install eyed3, it's needed to tag downloaded songs

FNULL = open(os.devnull, 'w')         # in order to youtube-dl not printing shit

################################################################################



################################################################################
# Functions ####################################################################

def SearchYouTube(X): # --------------------------------------------------------
  query   = urllib.parse.urlencode({"search_query": X})
  content = urllib.request.urlopen("http://www.youtube.com/results?" + query)
  results = re.findall(r'href=\"\/watch\?v=(.{11})', content.read().decode())
  Y       = "http://www.youtube.com/watch?v=" + results[0]
  return Y



def Download(Y): # -------------------------------------------------------------
  # I do need youtube-dl installed to work
  order = 'youtube-dl -x --audio-format "mp3" -o "newsong.%(ext)s" ' + Y
  subprocess.call([order], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)



def Tagger(Ti, Ar, Al, Nu): # --------------------------------------------------
  file = eyed3.load('newsong.mp3')
  file.tag.artist    = Ar
  file.tag.album     = Al
  file.tag.title     = Ti
  file.tag.track_num = Nu
  # --> year when we know how to export it (exportify doesn't do this stuff)
  file.tag.save()
  filename = "{0} - {1}.mp3".format(file.tag.artist, file.tag.title)
  path     = os.path.join(os.getenv("HOME"),"MusicJourney")
  #os.rename('newsong.mp3', filename)

  if not os.path.isdir(path):
    cmd = "mkdir -p " + path
    print("   Creating directory:",path + ".")
    subprocess.call([cmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

  if os.path.exists(os.path.join(path,filename)):
    print("   This song was downloaded before.")
  else:
    cmd = 'mv "newsong.mp3" ' + os.path.join(path,'"'+filename+'"')
    subprocess.call([cmd], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)

  return filename



def DownLink(csvname): # -------------------------------------------------------

  # Get file
  csvname = csvname.split(".")[0]
  csvfile = csv.reader(open(csvname + ".csv", "r"))
  data    = list(csvfile)
  songs   = len(data)
  print('Playlist ' + csvname + ' correctly loaded.')
  print('Start downloading...\n')

  # Loop over songs
  for l in range(1, songs, 1):
    # Get info
    ti = data[l][1];  ar = data[l][2]; al = data[l][3]; n = int(data[l][5])
    # String to search at YouTube
    string  = data[l][1] + ' ' + data[l][2]

    print(' # ' + ti +' - '+ar)
    try:
      # Search song's video
      songurl = SearchYouTube(string)
      # Download song
      Download(songurl)
      # Tag it!
      filename = Tagger(ti, ar, al, n)
      #print('   Success!')
    except:
      print('   An error occurred :( sorry.')

  print('\nPlaylist ' + csvname + ' finished.')
  print('Songs stored at:',os.path.join(os.getenv("HOME"),"MusicJourney"),'.')

################################################################################



################################################################################
# Command line ArgumentParser ##################################################

help = ["Magic Journey: a YouTube Spotify playlist downloader",
        "CSV file with songs to download"]
parser = argparse.ArgumentParser(description=help[0])
parser.add_argument('--list', default='', type=str, help=help[1])
args = parser.parse_args()

DownLink(args.list)

################################################################################
