import cv2
from PIL import ImageGrab
import numpy as np
import argparse
import time
import os
import win32gui
import win32ui
import win32con
import win32api

FFMPEG_PATH = "F:\\Tools\\ffmpeg"


def crop(mp4_file):
    # "ffmpeg -i input.mp4 -vf crop=1724:972:194:108 output.mp4 -y"
    cmd = 'SET PATH=%PATH%;"' + FFMPEG_PATH + '" & '
    cmd = cmd + 'ffmpeg -i "' + mp4_file + '" -vf crop=1724:972:194:108 "' + mp4_file + '_crop.mp4" -y'
    val = os.system(cmd)
    if val == 0:
        print("裁剪视频成功")
    else:
        print("裁剪视频失败")


def get_window_img_dc(window_name="宇宙模拟器(universe sim)"):
    # 获取桌面
    # hdesktop = win32gui.GetDesktopWindow()
    handle = win32gui.FindWindow(None, window_name)
    return handle


def record():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int, default=30, help='frame per second')
    parser.add_argument('--window_name', type=str, default='宇宙模拟器(universe sim)', help='window_name')
    parser.add_argument('--total_time', type=int, default=10000000, help='video total time')
    parser.add_argument('--savename', type=str, default='video_right.mp4', help='save file name')
    parser.add_argument('--screen_type', default=0, type=int, choices=[0, 1], help='1: full screen, 0: region screen')
    args = parser.parse_args()

    if args.screen_type == 0:
        print('Press Esc to close window')

    if args.screen_type:
        curScreen = ImageGrab.grab()  # 获取屏幕对象
        height, width = curScreen.size
        min_x, min_y, max_x, max_y = 0, 0, width, height
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(args.savename, fourcc, args.fps, (height, width))
    else:
        # point1, point2 = select_roi(curScreen)
        # print(point1, point2)  # (184, 71) (1719, 932)
        point1, point2 = (194, 108), (1724, 972)
        print(point1, point2)  # (184, 71) (1719, 932)
        min_x = min(point1[0], point2[0])
        min_y = min(point1[1], point2[1])
        max_x = max(point1[0], point2[0])
        max_y = max(point1[1], point2[1])
        width, height = max_y - min_y, max_x - min_x
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(args.savename, fourcc, args.fps, (height, width))

    # wait_ms = 1000 / args.fps
    imageNum = 0
    print("查找模拟器窗口")
    while True:
        handle = get_window_img_dc()
        if handle > 0:
            print(handle)
            break
        time.sleep(0.001)
    print("开始捕捉...")

    while True:
        handle = get_window_img_dc()
        if handle == 0:
            print("模拟器窗口关闭")
            break

        # current_time = time.time() * 1000
        # next_frame_time = last_time + wait_ms
        # if current_time < next_frame_time:
        #     time.sleep((next_frame_time - current_time) / 1000)
        #     print((next_frame_time - current_time) / 1000)
        #
        # last_time = time.time() * 1000
        imageNum += 1
        captureImage = ImageGrab.grab()  # 抓取屏幕
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        if args.screen_type == 0:
            frame = frame[min_y:max_y, min_x:max_x, :]
        # print(imageNum, args.fps, args.total_time)
        if imageNum < args.fps * args.total_time:
            video.write(frame)
        # 退出条件
        # if cv2.waitKey(50) == ord('q') or imageNum > args.fps * args.total_time:
        #
        k = cv2.waitKey(1)
        # print(k)
        if k == 27 or imageNum > args.fps * args.total_time:  # Esc key to stop
            print("退出...")
            break

    print("视频保存")
    video.release()
    cv2.destroyAllWindows()
    # crop('video.mp4')
    print("完成")


if __name__ == '__main__':
    record()
