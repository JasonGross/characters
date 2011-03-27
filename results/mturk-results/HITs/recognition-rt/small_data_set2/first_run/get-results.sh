#!/bin/bash
source hit_header.sh "$@"

pushd "$SCRIPTPATH"
for file in "$HITNAME-results.txt*"
do
    mv "$file" "${file}2.bak"
done
popd
pushd "$MTURK_CMD_HOME/bin"
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo $SCRIPTPATH
./getResults.sh -successfile "$SCRIPTPATH/$HITNAME.input.success" -namevaluepairs -outputfile "$SCRIPTPATH/$HITNAME-results.txt" $SANDBOX
popd
