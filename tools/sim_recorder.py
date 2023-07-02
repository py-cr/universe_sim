import cv2
from PIL import ImageGrab
import numpy as np
import argparse
import time

global img
global point1, point2


def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放
        point2 = (x, y)
        cv2.rectangle(img2, point1, point2, (0, 0, 255), thickness=2)
        cv2.imshow('image', img2)


def select_roi(frame):
    global img, point1, point2
    img = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    winname = 'image'
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(winname, on_mouse)
    cv2.imshow(winname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return point1, point2


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int, default=30, help='frame per second')
    parser.add_argument('--total_time', type=int, default=10, help='video total time')
    parser.add_argument('--savename', type=str, default='video.mp4', help='save file name')
    parser.add_argument('--screen_type', default=0, type=int, choices=[0, 1], help='1: full screen, 0: region screen')
    args = parser.parse_args()

    print('等到3秒，请切换到录屏的页面')
    if args.screen_type == 0:
        print('Press Esc to close window')

    last_time = time.time() * 1000
    time.sleep(3)

    curScreen = ImageGrab.grab()  # 获取屏幕对象
    if args.screen_type:
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

    wait_ms = 1000 / args.fps
    imageNum = 0

    while True:
        current_time = time.time() * 1000
        next_frame_time = last_time + wait_ms
        if current_time < next_frame_time:
            time.sleep((next_frame_time - current_time) / 1000)
            print((next_frame_time - current_time) / 1000)

        last_time = time.time() * 1000
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

    print("保存中...")
    video.release()
    cv2.destroyAllWindows()
    print("完成")
