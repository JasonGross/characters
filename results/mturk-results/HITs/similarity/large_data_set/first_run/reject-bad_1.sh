#!/bin/bash
source hit_header.sh "$@"

pushd "$SCRIPTPATH"
echo "hitid	hittypeid"> "$HITNAME.input.reject.success"
echo "1N6Q12GGLAPD0GNILE3NX12T6TX8SQ	1Y18M0NWG8NIOS0IMRO4GIJF7KCWDQ">>"$HITNAME.input.reject.success"
echo "assignmentIdToReject	assignmentIdToRejectComment"> "$HITNAME.input.reject"
#echo '1ESSP6U8IPGNR6M0YH1BCBFNGKZ4H4	"You did not make an honest effort to state which characters were the same and which were different."'>> $HITNAME.input.reject
pushd "$MTURK_CMD_HOME/bin"
echo "$SCRIPTPATH"
./rejectWork.sh -rejectfile "$SCRIPTPATH/$HITNAME.input.reject"
./extendHITs.sh -successfile "$SCRIPTPATH/$HITNAME.input.reject.success" -assignments 1
popd
popd
