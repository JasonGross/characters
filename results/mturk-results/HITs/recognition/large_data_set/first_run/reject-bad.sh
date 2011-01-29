#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
pushd $MTURK_CMD_HOME/bin
echo $SCRIPTPATH
./rejectWork -rejectfile $SCRIPTPATH/%(reject_file)s &
./extendHITs.sh -successfile $SCRIPTPATH/%(success_file)s -assignments %(num_add)d
popd
