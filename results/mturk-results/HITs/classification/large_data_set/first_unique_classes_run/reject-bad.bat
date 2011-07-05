SET i=%CD%
PUSHD "D:\mech-turk-tools-1.3.0\bin"
ECHO %i%
START rejectWork -rejectfile "%i%\classification.input.reject"
START extendHITs -successfile "%i%\classification.input.reject.success" -assignments 0
POPD
PAUSE
