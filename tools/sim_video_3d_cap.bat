@REM @echo off
@REM 设置环境和参数
SET Anaconda3=D:/Anaconda3
SET env=pythoncr
SET DISK=G:
SET SimDir=%DISK%/works/gitcode/universe_sim

SET SimFileDir=%1
SET SimFileName=%2
SET param3=%3

SET PYTHONPATH=%SimDir%;
SET SimFilePath=%SimDir%/sim_scenes/%SimFileDir%/

CALL %Anaconda3%/Scripts/activate.bat %Anaconda3%
CALL conda activate %env%
%DISK%

cd %SimFilePath%
start python -m %SimFileName% 3d

cd %SimDir%\tools
python -m sim_video_3d_cap_ext --save_name=%SimFileName%.mp4 %param3%


