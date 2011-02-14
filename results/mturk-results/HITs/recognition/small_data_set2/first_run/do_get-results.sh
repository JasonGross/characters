#/bin/bash
source hit_header.sh "$@"

pushd $SCRIPTPATH
./get-results.sh
/mit/python/bin/python2.6 ~/web_scripts/alphabets/scripts/python/convert-recognition-turk-file-to-folders.py --path "small-data-set-2" --exclude-rejected $SCRIPTPATH/$HITNAME-results.txt
cp -u ./combine_dot_m.py ~/web_scripts/alphabets/results/recognition/unreviewed/small-data-set-2/
pushd ~/web_scripts/alphabets/results/recognition/unreviewed/small-data-set-2/
./combine_dot_m.py
popd
popd
