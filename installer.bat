@echo off
setlocal

set /p destDir=Please enter the Mupen64Plus directory: 

if not exist "%destDir%" (
    echo The directory "%destDir%" does not exist.
    goto :eof
)

copy "gui.exe" "%destDir%\gui.exe"
copy "mupen64plus_config.json" "%destDir%\mupen64plus_config.json"

if %errorlevel% equ 0 (
    echo Files were successfully installed to "%destDir%".
) else (
    echo There was an error installing the files.
    goto :eof
)

set /p createShortcut=Do you want to create a shortcut for the Mupen64Plus GUI on your desktop? (y/n): 
if /i "%createShortcut%" neq "y" goto :eof

set desktop=%USERPROFILE%\Desktop

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.ExpandEnvironmentStrings("%%USERPROFILE%%\Desktop\Mupen64Plus GUI.lnk") >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%destDir%\gui.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs

del CreateShortcut.vbs

echo Shortcut has been created on your desktop.

:end
endlocal

pause
