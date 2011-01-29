/mit/python/bin/python2.6 /afs/athena.mit.edu/user/j/g/jgross/web_scripts/alphabets/scripts/python/convert-recognition-turk-file-to-folders.py --path small-data-set --exclude-rejected recognition-results.txt
pushd ~/web_scripts/alphabets/results/recognition/unreviewed/small-data-set/ && ./combine_dot_m.py && popd
