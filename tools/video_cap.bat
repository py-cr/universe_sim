@REM @echo off
@REM 设置环境和参数
SET Anaconda3=D:/Anaconda3
SET env=pythoncr
SET DISK=D:
SET SimDir=%DISK%/gitee/universe_sim

SET SimFileName=%1

CALL %Anaconda3%/Scripts/activate.bat %Anaconda3%
CALL conda activate %env%
%DISK%

cd %SimDir%\tools
@REM video_cap.bat speed_of_light_3d
python -m sim_video_3d_cap_ext --save_name=%SimFileName%_2.mp4


