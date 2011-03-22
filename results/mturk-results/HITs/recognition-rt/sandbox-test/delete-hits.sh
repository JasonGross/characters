#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
pushd $MTURK_CMD_HOME/bin
./deleteHITs.sh -successfile $SCRIPTPATH/recognition.input.success -approve -expire -force -sandbox 
mv $SCRIPTPATH/recognition.input.success $SCRIPTPATH/deleted-recognition.input.success
popd
