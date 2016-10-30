@echo off
setlocal enableextensions enabledelayedexpansion
pushd "\\netapp2\psychsim\Programs\Python"

set startDateName="2015\11\17"
set /a i=1

:START
python dateReturn.py !startDateName! !i! > tempFile
set /p fileDateName= < tempFile
echo !fileDateName!
del tempFile
python fetchFile.py !fileDateName!
cd ..\eclipseLuna\workspace\PredicateExtraction
java -XX:+UseConcMarkSweepGC -Xmx10g -cp bin\ArticleExtraction7.2.jar GdeltPredicateExtraction !fileDateName!
cd ..\..\..\Python
python zipFiles.py !fileDateName!
echo "....................................................................................."
echo ".................................Waiting till next day..............................."
echo "....................................................................................."
python sleep.py
set /a i=!i!+1
GOTO START

endlocal

pause