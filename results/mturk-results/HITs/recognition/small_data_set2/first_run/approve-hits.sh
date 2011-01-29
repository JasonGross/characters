#/bin/bash
source hit_header.sh "$@"

pushd $MTURK_CMD_HOME/bin
./approveWork.sh -successfile $SCRIPTPATH/$HITNAME.input.success $SANDBOX
mv $SCRIPTPATH/$HITNAME.input.success $SCRIPTPATH/$HITNAME.input.success
popd
