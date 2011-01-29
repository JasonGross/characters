#/bin/bash
source hit_header.sh "$@"

pushd $SCRIPTPATH
for file in $HITNAME.input.success*
do
	mv $file ${file}2.bak
done
for file in upload-results.txt*
do
	mv $file ${file}2.bak
done
popd
pushd $MTURK_CMD_HOME/bin
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo $SCRIPTPATH
./loadHITs.sh -input $SCRIPTPATH/$HITNAME.input -question $SCRIPTPATH/$HITNAME.question -properties $SCRIPTPATH/$HITNAME.properties $SANDBOX >> $SCRIPTPATH/upload-results.txt
popd

