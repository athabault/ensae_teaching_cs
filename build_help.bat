rem we remove everything from dist
echo off

rem python 3.4

set pythonexe="c:\python34\python"
%pythonexe% clean_pyd.py

rem help

rem echo ####################################################### 1A

rem %pythonexe% -u setup.py build_pres

rem if not exist dist\html_pres mkdir dist\html_pres
rem xcopy /E /C /I /Y _doc\presentation\build\html dist\html_pres

echo ####################################################### 2A

%pythonexe% -u setup.py build_pres_2A

if not exist dist\html_pres_2A mkdir dist\html_pres_2A
xcopy /E /C /I /Y _doc\presentation_2A\build\html dist\html_pres_2A
