#! /usr/bin/env python
#
# cmus_cover_art.py: display album art in feh with cmus
# Copyright (C) 2018  Mandy Wilkens <mwilkens241@gmail.com>
#
# Usage: Run script for instructions.
 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
  
import sys
import os
import time
import subprocess
from PIL import Image 

# Make sure to change this to where you cloned the repo
REPO_LOCATION = "~/.config/cmus/cmus-artwork"

def print_usage():
   """Display usage info and exit."""
 
   print ' ##############################################################################'
   print ' # cmus_cover_art.py: display album art in feh with cmus                      #'       
   print ' # Copyright (C) 2018  Mandy Wilkens <mwilkens241@gmail.com>                  #'
   print ' #                                                                            #'
   print ' # Tested on Ubuntu 18.04 with i3 window manager.                             #'
   print ' # Requirements: feh; probably python 2.x.                                    #'
   print ' ##############################################################################'
   print ' # Usage:                                                                     #'
   print ' #  1. Copy cmus_album_art.py to ~/.cmus/ and make executable.                #'
   print ' #  2. Create ~/.cmus/status_display_program.sh with these contents           #'
   print ' #     and make executable (remove spaces and border):                        #'
   print ' #                                                                            #'
   print ' #     #!/bin/sh                                                              #'
   print ' #     ~/.cmus/cmus-artwork/cmus_album_art.py "$*" &                          #'
   print ' #                                                                            #'
   print ' #  3. Set the status_display_program variable in cmus (with YOUR homedir!)   #'
   print ' #                                                                            #'
   print ' #     :set status_display_program=/home/user/.cmus/status_display_program.sh #'
   print ' #                                                                            #'
   print ' #  4. Enjoy desktop notifications from cmus! Be sure to :save.               #'
   print ' ##############################################################################'
   sys.exit(2)


def status_data(item):
   """Return the requested cmus status data."""
 
   # We loop through cmus status data and use each of its known data
   # types as 'delimiters', collecting data until we reach one,
   # inserting it into the dictionary -- rinse and repeat.
 
   # cmus helper script provides our data as argv[1].
   cmus_data = sys.argv[1]
 
   # Split the data into an easily-parsed list.
   cmus_data = cmus_data.split()
 
   # Our temporary collector list.
   collector = []
 
   # Dictionary that will contain our parsed-out data.
   cmus_info = {'status':"",
                'file':"",
                'artist':"",
                'album':"",
                'discnumber':"",
                'tracknumber':"",
                'title':"",
                'date':"",
                'duration':""}
 
   # Loop through cmus data and write it to our dictionary.
   last_found = "status"
   for value in cmus_data:
       collector.append(value)
       # Check to see if cmus value matches dictionary key.
       for key in cmus_info:
           # If a match has been found, record the data.
           if key == value:
               collector.pop()
               cmus_info[last_found] = " ".join(collector)
               collector = []
               last_found = key
 
   # Return whatever data main() requests.
   return cmus_info[item]

def get_cover_art():
    if status_data("status") == "playing":
        stamp = status_data("album").replace(" ","")
        # Extract cover art
        print "Getting Cover Art for %s" % stamp
        subprocess.call('rm '+REPO_LOCATION+'/temp.jpg', shell=True)
        subprocess.call('ffmpeg -i "'+ status_data('file') +'" -an -vcodec copy '+REPO_LOCATION+'/temp.jpg', shell=True)
        if os.path.isfile(REPO_LOCATION + "/temp.jpg"):
            subprocess.call("rm "+REPO_LOCATION+"/covers/*.jpg", shell=True)
            subprocess.call("cp "+REPO_LOCATION+"/temp.jpg "+REPO_LOCATION+"/covers/"+stamp+"_art.jpg", shell=True)
        else:
            print "Art not found in tags... checking folder"
            folder = os.path.dirname(status_data('file'))
            print "No Art Found!"
            subprocess.call('rm '+REPO_LOCATION+'/covers/*.jpg', shell=True)
            subprocess.call("cp "+REPO_LOCATION+"/noart.jpg "+REPO_LOCATION+"/covers/"+stamp+"_art.jpg", shell=True)

def main():
    getArt = False
    try:
       # See if script is being called by cmus before proceeding.
       if sys.argv[1].startswith("status"):
           getArt=True
    except:
        "do nothing"

    if getArt == True:
        try:
            get_cover_art()
        except Exception as e: print(e)
    else:
        print_usage()
 
if __name__ == "__main__":
   main()
