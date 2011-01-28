#!/bin/bash
function ask-boolean() {
  if [ "$2" == "" ]; then
    echo -n "Press ENTER to continue..."
    read
    let $1=1
  else
    while true; do
      echo -n "$1 (y/n)"
      read yn
      case $yn in
             [yY] | [yY]es ) let $2=1; break ;;
              [nN] | [nN]o ) let $2=0; break ;;
[qQxX] | [qQ]uit | [eE]xit ) exit ;;
        * ) echo "Enter yes or no" ;;
      esac
    done
  fi
}


SCRIPTPATH=`dirname $(readlink -f $0)`
pushd $SCRIPTPATH
ask-boolean "Get Turk results?" GO
if [ $GO == 1 ]; then
  ./mturk-results/HITs/get-seventeen/get-results.sh
fi
ask-boolean "Convert Turk file to folders?" GO
if [ $GO == 1 ]; then
  rm -rf turk-*/*
  ../scripts/python/convert-turk-file-to-folders.py mturk-results/HIT-results-firsts.txt mturk-results/HIT-results-17.txt
fi
ask-boolean "Compress strokes?" GO
if [ $GO == 1 ]; then
  ./compress-strokes_standalone.py
fi
ask-boolean "Move Turk to approved?" GO
if [ $GO == 1 ]; then
  rm -rf {accepted,rejected,extra}-{images,strokes,extra-info}
  ../scripts/python/move-turk-to-approved.py
fi
ask-boolean "Remake images?" GO
if [ $GO == 1 ]; then
  ../scripts/python/convert-alphabet-strokes-to-pngs.py
fi
ask-boolean "Rebuild data objects?" GO
if [ $GO == 1 ]; then
  rm ../object-storage/get_accepted_image_list.obj ../object-storage/get_rejected_image_list.obj ../object-storage/get_rejected_image_list.obj ../object-storage/get_turk_*.obj
  /mit/python/bin/python2.6 ../scripts/python/characters.py
fi
ask-boolean "Make matlab?" GO
if [ $GO == 1 ]; then
  ../scripts/python/make-matlab.py --no-prompt
fi
ask-boolean "Make dataset?" GO
if [ $GO == 1 ]; then
  ../scripts/python/build-public-dataset.py
fi
popd

