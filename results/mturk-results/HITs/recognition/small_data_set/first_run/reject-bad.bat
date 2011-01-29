SET i=%CD%
PUSHD "D:\mech-turk-tools-1.3.0\bin"
ECHO %i%
START rejectWork -rejectfile "%i%\recognition.input.reject"
START extendHITs -successfile "%i%\recognition.input.reject.success" -assignments 0
POPD
PAUSE
