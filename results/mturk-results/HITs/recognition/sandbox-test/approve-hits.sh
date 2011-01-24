#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
pushd $MTURK_CMD_HOME/bin
./approveWork.sh -successfile $SCRIPTPATH/recognition.input.success -sandbox
mv $SCRIPTPATH/recognition.input.success $SCRIPTPATH/recognition.input.success
popd
