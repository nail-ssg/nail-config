@echo off
if exist env goto :installed
set _branch-3.6=win32-3.6.0
set _branch-3.5=win32-3.5.3
set _branch-last=win32-3.6.0
set suffix=%~n0
set tag=%suffix:install-=%
echo set branch=%%_branch-%tag%%% >_setvalue.cmd
call _setvalue.cmd
del _setvalue.cmd
if not "%suffix%"=="last" set tag=win32bit-%tag%
git clone https://github.com/nail-ssg/winvirtenv.git env
pushd env
git checkout "tags/%tag%" -b %branch%
popd
echo call env\scripts\activate> workon.cmd
echo call workon^&^&call deactivate^&^&rd /q /s env^&^&del workon.cmd> uninstall.cmd
call workon
if exist requirements.txt pip install -r requirements.txt
exit /b

:installed
echo Environment installed. Run uninstall.cmd before new install.