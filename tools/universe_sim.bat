@REM @echo off
@REM 设置环境和参数
SET Anaconda3=D:/Anaconda3
SET env=pythoncr
SET DISK=D:
SET SimDir=%DISK%/gitee/universe_sim

SET SimFileDir=%1
SET SimFileName=%2
SET param3=%3

SET PYTHONPATH=%SimDir%;
SET SimFilePath=%SimDir%/sim_scenes/%SimFileDir%/

CALL %Anaconda3%/Scripts/activate.bat %Anaconda3%
CALL conda activate %env%
%DISK%

cd %SimFilePath%
@REM  universe_sim.bat science speed_of_light_3d
python -m %SimFileName%
cd %SimDir%\tools



