import numpy as np
import win32gui
import win32ui
import win32con
import win32api
import cv2
from PIL import ImageGrab
import time
from dataclasses import dataclass


@dataclass
class Args:
    savename: str = ''
    fps: int = 0
    total_time: int = 0


def get_window_img_dc(window_name):
    # 获取桌面
    # hdesktop = win32gui.GetDesktopWindow()
    handle = win32gui.FindWindow(None, window_name)
    # 分辨率适应
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # 创建设备描述表
    desktop_dc = win32gui.GetWindowDC(handle)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    return img_dc, width, height


window_img_dc, width, height = get_window_img_dc("solar_system")


def screenshot():
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


def show_image(img):
    # img = Image.open(r".\image.jpg")
    # img = img.convert("RGBA")  # 转换获取信息
    # pixdata = img.load()
    # cv.imshow("name",img)
    from PIL import Image
    image = Image.fromarray(img)
    print(type(image))  # 结果为<class 'PIL.JpegImagePlugin.JpegImageFile'>
    print(image.size)  # 结果为(822，694)，这里注意Image输出的结果先显示列数，后显示行数
    image.save(r"./1.jpg")
    image.show()


if __name__ == '__main__':
    # parser.add_argument('--fps', type=int, default=30, help='frame per second')
    # parser.add_argument('--total_time', type=int, default=10, help='video total time')
    # parser.add_argument('--savename', type=str, default='video.mp4', help='save file name')
    # parser.add_argument('--screen_type', default=0, type=int, choices=[0, 1], help='1: full screen, 0: region screen')

    img = screenshot()

    height, width, _ = img.shape

    args = Args()
    args.savename = "video.mp4"
    args.fps = 30
    args.total_time = 10

    # left, top, right, bottom = 194, 108, 1724, 972
    # bbox = (left, top, right, bottom)
    # # curScreen = ImageGrab.grab(bbox)  # 获取屏幕对象
    # # point1, point2 = select_roi(curScreen)
    # # print(point1, point2)  # (184, 71) (1719, 932)
    # point1, point2 = (194, 108), (1724, 972)
    # print(point1, point2)  # (184, 71) (1719, 932)
    # min_x = min(point1[0], point2[0])
    # min_y = min(point1[1], point2[1])
    # max_x = max(point1[0], point2[0])
    # max_y = max(point1[1], point2[1])
    # width, height = max_y - min_y, max_x - min_x
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(args.savename, fourcc, args.fps, (height, width))

    wait_ms = 1000 / args.fps
    imageNum = 0

    while True:
        # current_time = time.time() * 1000
        # next_frame_time = last_time + wait_ms
        # if current_time < next_frame_time:
        #     time.sleep((next_frame_time - current_time) / 1000)
        #     print((next_frame_time - current_time) / 1000)

        last_time = time.time() * 1000
        if imageNum == 0:
            captureImage = img
        else:
            captureImage = screenshot()
        imageNum += 1
        frame = cv2.cvtColor(np.array(captureImage), cv2.COLOR_RGB2BGR)
        # if args.screen_type == 0:
        #     frame = frame[min_y:max_y, min_x:max_x, :]
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
