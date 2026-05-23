@echo off
setlocal EnableDelayedExpansion

REM Agent1 first for 10 times, Agent2 first for 10 times
set TIMES=10

REM set the test rave parameter: explore = 0.5, rave_const = 300
python update_meta.py 0.3 300

REM Set the output file name
set OUTPUT_FILE=test/rave_0.3_300_rave_0.1_300.txt

REM Set a temporary file name
set TEMP_FILE=temp.txt

echo ----------------------------------- >> %OUTPUT_FILE%
echo rave_0.3_300 vs rave_0.1_300 >> %OUTPUT_FILE%
echo ----------------------------------- >> %OUTPUT_FILE%

REM Agent1 vs Agent2
for /l %%i in (1,1,%TIMES%) do (
    echo game %%i

    REM Run the command and redirect output to a temporary file
    python Hex.py "a=test;python agents\Group3\TestAgent.py" "a=rave;python agents\Group3\CapAgent.py" -v > "%TEMP_FILE%"
    
    REM Initialize a flag to start capturing output after 'Game over'
    set "capture=false"

    REM Read the temporary file line by line
    for /f "delims=" %%a in ('type "%TEMP_FILE%"') do (
        REM If 'Game over' has been encountered or the flag is set, append the line to the output file
        if "!capture!" == "true" (
            echo %%a >> "%OUTPUT_FILE%"
        ) else (
            REM Check if 'Game over' is in the line and set the flag
            echo %%a | find "Game over" > nul && (
                set "capture=true"
                echo %%a >> "%OUTPUT_FILE%"
            )
        )
    )
    echo ----------------------------------- >> %OUTPUT_FILE%
)

echo ----------------------------------- >> %OUTPUT_FILE%
echo rave_0.1_300 vs rave_0.3_300>> %OUTPUT_FILE%
echo ----------------------------------- >> %OUTPUT_FILE%

REM Agent2 vs Agent1
for /l %%i in (1,1,%TIMES%) do (
    echo game %%i

    REM Run the command and redirect output to a temporary file
    python Hex.py "a=rave;python agents\Group3\CapAgent.py" "a=test;python agents\Group3\TestAgent.py" -v > "%TEMP_FILE%"
    
    REM Initialize a flag to start capturing output after 'Game over'
    set "capture=false"

    REM Read the temporary file line by line
    for /f "delims=" %%a in ('type "%TEMP_FILE%"') do (
        REM If 'Game over' has been encountered or the flag is set, append the line to the output file
        if "!capture!" == "true" (
            echo %%a >> "%OUTPUT_FILE%"
        ) else (
            REM Check if 'Game over' is in the line and set the flag
            echo %%a | find "Game over" > nul && (
                set "capture=true"
                echo %%a >> "%OUTPUT_FILE%"
            )
        )
    )
    echo ----------------------------------- >> %OUTPUT_FILE%
)

REM Delete the temporary file
if exist "%TEMP_FILE%" del "%TEMP_FILE%"

endlocal
