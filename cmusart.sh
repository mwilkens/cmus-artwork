#!/bin/bash

# Directory Defines
CMUS_COVERS_DIR=~/.config/cmus/cmus-artwork/covers
CMUS_DIR=~/.config/cmus/cmus-artwork

# Refresh every 5 seconds
FEH_REFRESH=5

if [! -d "$CMUS_COVERS_DIR"]; then
    mkdir $CMUS_COVERS_DIR
fi

while (true)
do
    if ps ax | grep -v grep | grep 'cmus' > /dev/null
    then
        # feh usually fails in this mode when there's no art in the folder
        # so this loop just ensures that there's the default artwork in
        # the covers directory every time we refresh feh
        # this should be eliminated if possible, as it destroys the window
        if [ -f $CMUS_COVERS_DIR/*.jpg  ]; then
            echo "Error! No cover art!"
        else
            # copy the noart to the covers directory
            cp $CMUS_DIR/noart.jpg $CMUS_COVERS_DIR/noart.jpg
        fi
        # keeps running feh
        feh $CMUS_COVERS_DIR -R $FEH_REFRESH -B black -g 500x500 --auto-zoom
        sleep $FEH_REFRESH # make sure we don't overload things
    else
        echo "cmus is not running... exiting..."
    fi
done
