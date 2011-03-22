#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
pushd $SCRIPTPATH
for file in recognition-results.txt*
do
    mv $file ${file}2.bak
done
popd
pushd $MTURK_CMD_HOME/bin
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo $SCRIPTPATH
./getResults.sh -successfile $SCRIPTPATH/recognition.input.success -namevaluepairs -outputfile $SCRIPTPATH/recognition-results.txt -sandbox
popd
