rem @ECHO OFF

rem Make environment variable changes local to this batch file
SETLOCAL

call C:\N900\scripts\Windows\common_env.bat

rem Set CYGWIN variable to 'nontsec'. That makes sure that permissions
rem on your windows machine are not updated as a side effect of cygwin
rem operations.
set CYGWIN=nontsec

rem Make cwRsync home as a part of system PATH to find required DLLs
set CWOLDPATH=%PATH%
set PATH=%RSYNC_DIR%;%PATH%

rem Set HOME variable to your windows home directory. That makes sure 
rem that ssh command creates known_hosts in a directory you have access.
set HOME=%HOMEDRIVE%%HOMEPATH%

set MM_PC=/cygdrive/C/Dev/MaeMoney/src
set MM_N900=/home/user/apps/MaeMoney



rsync.exe -ah --progress --exclude .svn %MM_PC% user@%N900_IP%:%MM_N900%
pause