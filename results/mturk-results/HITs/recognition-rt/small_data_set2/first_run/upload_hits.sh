#!/bin/bash
source hit_header.sh "$@"

echo Backing up files...
pushd "$SCRIPTPATH" 1>/dev/null
for file in $HITNAME.input.success*
do
	mv "$file" "${file}2.bak" 2>/dev/null
done
for file in upload-results.txt*
do
	mv "$file" "${file}2.bak" 2>/dev/null
done
popd 1>/dev/null
pushd "$MTURK_CMD_HOME/bin" 1>/dev/null
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo Uploading HIT in $SCRIPTPATH to turk $SANDBOX
./loadHITs.sh -input "$SCRIPTPATH/$HITNAME.input" -question "$SCRIPTPATH/$HITNAME.question" -properties "$SCRIPTPATH/$HITNAME.properties" $SANDBOX >> "$SCRIPTPATH/upload-results.txt"
popd 1>/dev/null

