@echo off
setlocal

set /p destDir=Please enter the installation directory: 

if not exist "%destDir%" (
    echo The directory "%destDir%" does not exist.
    goto :eof
)

copy "gui.exe" "%destDir%\gui.exe"
copy "mupen64plus_config.json" "%destDir%\mupen64plus_config.json"

if %errorlevel% equ 0 (
    echo Files were successfully copied to "%destDir%".
) else (
    echo There was an error installing the files.
)

:end
endlocal

pause