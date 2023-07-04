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
    screenshot = win32ui.CreateBitmap()  # win32ui.CreateBitmap() GetBitmapBits() MemoryError
    screenshot.CreateCompatibleBitmap(window_img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    # 截图至内存设备描述表
    mem_dc.BitBlt((0, 0), (width, height), window_img_dc, (0, 0), win32con.SRCCOPY)
    # 将截图保存到文件中
    # screenshot.SaveBitmapFile(mem_dc, 'screenshot.bmp')
    # TODO: Traceback (most recent call last):
    #   File "G:\works\gitcode\universe_sim\tools\sim_video_3d_cap.py", line 79, in sim_window_screen_shot
    #     img = screen_shot(img_dc)
    #   File "G:\works\gitcode\universe_sim\tools\sim_video_3d_cap.py", line 50, in screen_shot
    #     signedIntsArray = screenshot.GetBitmapBits(True)
    # MemoryError
    signedIntsArray = screenshot.GetBitmapBits(True)
    # 下面3个语句都能实现转换，推荐第1个
    # TODO: G:\works\gitcode\universe_sim\tools\sim_video_3d_cap.py:52:
    #  DeprecationWarning: The binary mode of fromstring is deprecated, as it behaves surprisingly on unicode inputs. Use frombuffer instead
    #   img = np.fromstring(signedIntsArray, dtype='uint8')
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


def video_write(video, l_frames, r_frames):
    min_index = min(r_frames.keys())
    max_index = max(r_frames.keys())

    for index in range(min_index, max_index + 1):
        rv = r_frames.get(index, None)
        lv = l_frames.get(index, None)
        if rv is None or lv is None:
            continue
        merged_list = [np.concatenate((lv[i], sublist), axis=0) for i, sublist in enumerate(rv)]
        try:
            video.write(np.array(merged_list))
        except Exception as e:
            print("video.write ERROR:", str(e))
            traceback.print_exc()
            break


def handle_3d_video(video, l_frames, r_frames):
    temp_frame_data = get_frame_temp_data()

    if temp_frame_data is not None:
        cnt = len(temp_frame_data)
        for idx, data in enumerate(temp_frame_data):
            print("对视频进行3D处理(%s/%s)" % (idx + 1, cnt + 1))
            video_write(video, data.left_frames, data.right_frames)

    print("对视频进行3D处理(%s/%s)" % (cnt + 1, cnt + 1))
    video_write(video, l_frames, r_frames)
    # min_index = min(r_frames.keys())
    # max_index = max(r_frames.keys())
    #
    # for index in range(min_index, max_index + 1):
    #     rv = r_frames.get(index, None)
    #     lv = l_frames.get(index, None)
    #     if rv is None or lv is None:
    #         continue
    #     merged_list = [np.concatenate((lv[i], sublist), axis=0) for i, sublist in enumerate(rv)]
    #     try:
    #         video.write(np.array(merged_list))
    #     except Exception as e:
    #         print("video.write ERROR:", str(e))
    #         traceback.print_exc()
    #         break


import pickle


class FrameData:
    def __init__(self, left_frames, right_frames):
        self.left_frames = left_frames
        self.right_frames = right_frames

    def save(self, file_name):
        FrameData.dump(file_name, self)

    @staticmethod
    def dump(file_name, data):
        with open(file_name, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(file_name):
        with open(file_name, 'rb') as f:
            data = pickle.load(f)
            return data


def clear_frame_temp_files():
    import shutil
    if os.path.exists("frame_temp"):
        shutil.rmtree("frame_temp")


def create_frame_temp_files(file_index, left_frames, right_frames):
    data = FrameData(left_frames, right_frames)
    if not os.path.exists("frame_temp"):
        os.mkdir("frame_temp")

    file_name = os.path.join("frame_temp", str(file_index).rjust(10, '0')) + ".frames"
    data.save(file_name)


def get_frame_temp_data():
    if not os.path.exists("frame_temp"):
        return None
    temp_frame_data = []
    for f in os.listdir("frame_temp"):
        if f.endswith(".frames"):
            temp_file = os.path.join("frame_temp", f)
            fd = FrameData.load(temp_file)
            print("读取临时文件", temp_file)
            temp_frame_data.append(fd)

    return temp_frame_data


def make_3d_video():
    args = get_args()
    # handle = get_window_handle()
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
    clear_frame_temp_files()
    while True:
        img = sim_window_screen_shot()
        if img is None:
            print("\n模拟器窗口已关闭，退出录屏")
            break

        _3d_card = img[4:20, 3:20, ]
        _3d_card_p = _3d_card[10, 10,]
        index = int(_3d_card_p[1]) + int(_3d_card_p[0])
        if index < last_index:
            index_base += (last_index + 1)
            create_frame_temp_files(index + index_base, l_frames, r_frames)
            r_frames.clear()
            l_frames.clear()

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

    handle_3d_video(video, l_frames, r_frames)

    print("视频保存中")
    video.release()
    cv2.destroyAllWindows()
    clear_frame_temp_files()
    # crop('video.mp4')
    print("视频保存完成")


if __name__ == '__main__':
    make_3d_video()
    # data = FrameData([1111, 211, 3], [5, 6, 7])
    # file_name = 'test11.frame'
    # data.save(file_name)
    #
    # d = FrameData.load(file_name)
    # print(d)
