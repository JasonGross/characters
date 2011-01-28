#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
echo hitid	hittypeid> characterrequest.input.reject.success
echo assignmentIdToReject	assignmentIdToRejectComment> characterrequest.input.reject
echo 1GDXXCJU0XTRJ4GXICN1TS8OK5XASW	177OZPRGN4BZM26WSL4SAIC1EZRJMQ>> characterrequest.input.reject.success
echo 1SSOU0B7KFFQVTKIJXN53H0J2HH06H	"Blank submission.">> characterrequest.input.reject
pushd $MTURK_CMD_HOME/bin
echo $SCRIPTPATH
./rejectWork -rejectfile $SCRIPTPATH/%(reject_file)s &
./extendHITs.sh -successfile $SCRIPTPATH/%(success_file)s -assignments %(num_add)d
popd
