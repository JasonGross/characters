#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0

pushd $SCRIPTPATH
for file in recognition.input.success*
do
	mv $file ${file}2.bak
done
for file in upload-results.txt*
do
	mv $file ${file}2.bak
done
popd
pushd ~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0/bin
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo $SCRIPTPATH
./loadHITs.sh -input $SCRIPTPATH/recognition.input -question $SCRIPTPATH/recognition.question -properties $SCRIPTPATH/recognition.properties -sandbox >> $SCRIPTPATH/upload-results.txt
popd

