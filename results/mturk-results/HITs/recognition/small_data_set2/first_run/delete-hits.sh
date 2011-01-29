#/bin/bash
source hit_header.sh "$@"

pushd $MTURK_CMD_HOME/bin
./deleteHITs.sh -successfile $SCRIPTPATH/$HITNAME.input.success -approve -expire -force $SANDBOX
mv $SCRIPTPATH/$HITNAME.input.success $SCRIPTPATH/deleted-$HITNAME.input.success
popd
