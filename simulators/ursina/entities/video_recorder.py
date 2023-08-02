from ursina import *
import os, shutil
import builtins
import numpy as np


class VideoRecorder(Entity):
    """
    from simulators.ursina.entities.video_recorder import VideoRecorder
    vr = VideoRecorder()
    sys.modules["__main__"].update = vr.screenshot

    app.run()
    """

    def __init__(self, temp_dir="screenshot_tmp", asset_folder=None):
        self.temp_dir = temp_dir
        # self.save_as_dir = save_as_dir
        if asset_folder is None:
            asset_folder = application.asset_folder
        # G:\works\gitcode\universe_sim\sim_scenes\science
        self.file_path = Path(asset_folder) / self.temp_dir
        self.duration = 1.0
        self.fps = 30
        self.sd = 5
        self.t = 0
        self.i = 0
        self.id_no = 0

        if getattr(builtins, 'base', None) is not None:
            if self.file_path.exists():
                # os.rmdir(self.file_path)
                shutil.rmtree(self.file_path)

            self.file_path.mkdir()

    def screenshot(self):
        self.t += time.dt

        if self.t >= 1 / self.fps:
            base.saveCubeMap(
                namePrefix=f'\\{self.temp_dir}\\cmap_' + str(self.i).zfill(self.sd) + '_#.jpg',
                # size=8196  # 最大分辨率，用于图片
                # size=4096  # 建议动态视频用这个
                # namePrefix = 'cube_map_#.png'
            )
        self.t = 0

        self.i += 1
