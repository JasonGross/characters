SET i=%CD%
ECHO hitid	hittypeid> characterrequest.input.reject.success
ECHO assignmentIdToReject	assignmentIdToRejectComment> characterrequest.input.reject
ECHO 1GDXXCJU0XTRJ4GXICN1TS8OK5XASW	177OZPRGN4BZM26WSL4SAIC1EZRJMQ>> characterrequest.input.reject.success
ECHO 1SSOU0B7KFFQVTKIJXN53H0J2HH06H	"Blank submission.">> characterrequest.input.reject
PUSHD "D:\mech-turk-tools-1.3.0\bin"
ECHO %i%
START rejectWork -rejectfile "%i%\characterrequest.input.reject"
START extendHITs -successfile "%i%\characterrequest.input.reject.success" -assignments 1
POPD
PAUSE
