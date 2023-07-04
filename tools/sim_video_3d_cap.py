import cv2
from PIL import ImageGrab, Image
import numpy as np
import argparse
import time
import os
import win32gui
import win32ui
import win32con
import win32api
import traceback


def get_window_handle(window_name="宇宙模拟器(universe sim)"):
    """
    获取模拟器窗口句柄
    @param window_name:
    @return:
    """
    handle = win32gui.FindWindow(None, window_name)
    return handle


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fps', type=int, default=30, help='frame per second')
    parser.add_argument('--total_time', type=int, default=10000000, help='video total time')
    parser.add_argument('--save_name', type=str, default='video.mp4', help='save file name')
    # parser.add_argument('--screen_type', default=0, type=int, choices=[0, 1], help='1: full screen, 0: region screen')
    args = parser.parse_args()
    print("total_time:", args.total_time)
    print("fps:", args.fps)
    print("save_name:", args.save_name)
    return args


def screen_shot(window_img_dc):
    width, height = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN), \
                    win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    # 创建一个内存设备描述表
    mem_dc = window_img_dc.CreateCompatibleDC()
    # 创建位图对象
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(window_img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), window_img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    # screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')
    signedIntsArray = screenshot.GetBitmapBits(True)
    # 下面3个语句都能实现转换，推荐第1个
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)
    # 内存释放
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    img = img[:, :, 0:3]  # 去掉透明数据
    return img


# def is_blank_screen(img_arr):
#     for x in range(500, 600):
#         for y in range(10, 20):
#             pix = img_arr[x, y, ]
#             # 检查标题栏，此时标题栏的颜色为白色
#             if pix.sum() > 600:
#                 return True
#     return False


def sim_window_screen_shot(wait_ses=-1):
    times = wait_ses * 100
    while True:
        handle = get_window_handle()
        if handle > 0:
            desktop_dc = win32gui.GetWindowDC(handle)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            try:
                img = screen_shot(img_dc)
            except Exception as e:
                print("ERROR:", str(e))
                traceback.print_exc()
                return None
            return img
        if wait_ses < 0:
            return None
        time.sleep(0.01)
        times -= 1
        if times <= 0:
            return None


def create_video(args, height, width):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(args.save_name, fourcc, args.fps, (width, height))
    return video


def show_image(img):
    from PIL import Image
    image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    image = Image.fromarray(image)
    print(type(image))  # 结果为<class 'PIL.JpegImagePlugin.JpegImageFile'>
    print(image.size)  # 结果为(822，694)，这里注意Image输出的结果先显示列数，后显示行数
    image.show()


if __name__ == '__main__':
    args = get_args()
    handle = get_window_handle()
    # print(get_args())
    print("请在10秒内打开模拟器")
    img = sim_window_screen_shot(10)
    if img is None:
        print("没有找到模拟器窗口，录屏失败！")
        exit(1)

    # show_image(img)
    video = create_video(args, img.shape[0], img.shape[1])
    imageNum = 0
    index_base = 0
    last_index = 0
    r_frames = {}
    l_frames = {}
    print("开始录屏")
    while True:
        img = sim_window_screen_shot()
        if img is None:
            print("\n模拟器窗口已关闭，退出录屏")
            break

        _3d_card = img[4:20, 3:20, ]
        _3d_card_p = _3d_card[10, 10,]
        index = _3d_card_p[1] + _3d_card_p[0]
        if index < last_index:
            index_base += (last_index + 1)

        last_index = index
        index = index + index_base

        if _3d_card_p[2] < 100:
            _3d_card_color = "b"
            _3d_card_direct = "right"
            if index not in r_frames.keys():
                r_frames[index] = img[:864, :768, ]
        else:
            _3d_card_color = "w"
            _3d_card_direct = "left"
            if index not in l_frames.keys():
                l_frames[index] = img[:864, :768, ]

        # if is_blank_screen(img):
        #     if imageNum % args.fps == 0:
        #         print('x', end='')
        #
        #     continue

        if imageNum % args.fps == 0:
            print('.', end='')
        # else:
        #     print(imageNum, end='')

        imageNum += 1

        # frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # if imageNum < args.fps * args.total_time:
        #     # img = img[:432,:768,]
        #     # show_image(frame)
        #     video.write(img)
    min_index = min(r_frames.keys())
    max_index = max(r_frames.keys())
    for index in range(min_index, max_index + 1):
        rv = r_frames.get(index, None)
        lv = l_frames.get(index, None)
        if rv is None or lv is None:
            continue
        merged_list = [np.concatenate((lv[i], sublist), axis=0) for i, sublist in enumerate(rv)]
        # show_image(np.array(merged_list))

        video.write(np.array(merged_list))

    print("视频保存中")
    video.release()
    cv2.destroyAllWindows()
    # crop('video.mp4')
    print("视频保存完成")
