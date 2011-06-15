#!/bin/bash
source hit_header.sh "$@"

pushd "$MTURK_CMD_HOME/bin" 1>/dev/null
./approveWork.sh -successfile "$SCRIPTPATH/$HITNAME.input.success" $SANDBOX
mv "$SCRIPTPATH/$HITNAME.input.success" "$SCRIPTPATH/approved-$HITNAME.input.success"
popd 1>/dev/null
