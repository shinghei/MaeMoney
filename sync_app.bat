@ECHO OFF

REM Make environment variable changes local to this batch file
SETLOCAL

set CWRSYNCHOME=C:\Program Files\cwRsync

REM Set CYGWIN variable to 'nontsec'. That makes sure that permissions
REM on your windows machine are not updated as a side effect of cygwin
REM operations.
SET CYGWIN=nontsec

REM Make cwRsync home as a part of system PATH to find required DLLs
SET CWOLDPATH=%PATH%
SET PATH=%CWRSYNCHOME%\BIN;%PATH%

REM Set HOME variable to your windows home directory. That makes sure 
REM that ssh command creates known_hosts in a directory you have access.
SET HOME=%HOMEDRIVE%%HOMEPATH%

rsync.exe -ah --progress --exclude .svn /cygdrive/C/Dev/MaeMoney/src user@192.168.1.100:/home/user/apps/MaeMoney


pause