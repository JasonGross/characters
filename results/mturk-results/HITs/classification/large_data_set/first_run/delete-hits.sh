#!/bin/bash
source hit_header.sh "$@"

pushd "$MTURK_CMD_HOME/bin"
./deleteHITs.sh -successfile "$SCRIPTPATH/$HITNAME$SANDBOX.input.success" -approve -expire -force $SANDBOX
mv "$SCRIPTPATH/$HITNAME$SANDBOX.input.success" "$SCRIPTPATH/deleted-$HITNAME$SANDBOX.input.success"
popd
