#!/bin/bash
source hit_header.sh "$@"

pushd "$SCRIPTPATH"
./get-results.sh
/mit/python/bin/python2.6 ~/web_scripts/alphabets/scripts/python/convert-$HITNAME-turk-file-to-folders.py "$SCRIPTPATH/$HITNAME-results.txt" --path "$TASKNAME" --exclude-rejected --exclude "$SCRIPTPATH/$HITNAME-rejected.txt"
cp -u ./combine_dot_m.py ~/"web_scripts/alphabets/results/$HITNAME/unreviewed/$TASKNAME/"
pushd ~/"web_scripts/alphabets/results/$HITNAME/unreviewed/$TASKNAME/"
./combine_dot_m.py
popd
popd
