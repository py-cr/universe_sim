from ursina import Entity, time, application, Path
import os, shutil
import builtins
import numpy as np


class VideoRecorder(Entity):
    def __init__(self, temp_dir="video_temp", file_name="test", asset_folder=None, save_as_dir=None):
        self.temp_dir = temp_dir
        self.file_name = file_name
        self.save_as_dir = save_as_dir
        if asset_folder is None:
            asset_folder = application.asset_folder
        # G:\works\gitcode\universe_sim\sim_scenes\science
        self.file_path = Path(asset_folder) / self.temp_dir
        self.duration = 1.0
        self.fps = 30
        self.sd = 6
        self.t = 0
        self.i = 0
        if getattr(builtins, 'base', None) is not None:
            if self.file_path.exists():
                # os.rmdir(self.file_path)
                shutil.rmtree(self.file_path)

            self.file_path.mkdir()
            base.movie(namePrefix=f'\\{self.temp_dir}\\{self.file_name}', duration=self.duration, fps=self.fps,
                       format='png',
                       sd=self.sd)

    def screenshot(self):
        self.t += time.dt
        if self.t >= 1 / self.fps:
            base.screenshot(
                namePrefix=f'\\{self.temp_dir}\\{self.file_name}_' + str(self.i).zfill(self.sd) + '.png',
                defaultFilename=0,
            )
            self.t = 0

        self.i += 1

    def save_as_video(self):
        import imageio
        if not os.path.exists(self.file_path):
            return
        if self.save_as_dir is None:
            self.save_as_dir = "."

        writer = imageio.get_writer(Path(f'{self.save_as_dir}/{self.file_name}.mp4'), fps=self.fps)
        for filename in os.listdir(self.file_path):
            im = imageio.imread(self.file_path / filename)
            if len(im.shape) == 2:
                # 可能为透明图片（无影像数据）
                continue
            writer.append_data(im)
        writer.close()
        print('Saved VIDEO to:', Path(f'{self.save_as_dir}/{self.file_name}.mp4'))

    def save_as_gif(self):
        import imageio
        images = []
        if not os.path.exists(self.file_path):
            return

        if self.save_as_dir is None:
            self.save_as_dir = self.file_path.parent

        for filename in os.listdir(self.file_path):
            images.append(imageio.imread(self.file_path / filename))

        imageio.mimsave(Path(f'{self.save_as_dir}/{self.file_name}.gif'), images)
        # shutil.rmtree(self.file_path)  # delete temp folder
        print('Saved GIF to:', Path(f'{self.save_as_dir}/{self.file_name}.gif'))


if __name__ == '__main__':
    # Path("G:\\works\\gitcode\\universe_sim\\sim_scenes\\science")
    vr = VideoRecorder(asset_folder="G:\\works\\gitcode\\universe_sim\\sim_scenes\\science")
    # vr.save_as_gif()
    vr.save_as_video()


# from ursina import *
# import os, shutil
# import numpy as np
#
# # import imageio    # gets imported in convert_to_gif
# # from panda3d.core import PNMImage
# # pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com imageio-ffmpeg
# import shutil
#
#
# class VideoRecorder(Entity):
#     def __init__(self, duration=50, name='untitled_video', **kwargs):
#         os.environ["PATH"] = os.environ["PATH"] + ";" + "F:\\Tools\\ffmpeg"
#         super().__init__()
#         self.recording = False
#         self.file_path = Path(application.asset_folder) / 'video_temp'
#
#         if os.path.exists(self.file_path):
#             shutil.rmtree(self.file_path)
#
#         os.mkdir(self.file_path)
#
#         # if os.path.exists(self.file_path):
#         #     os.rmdir(self.file_path)
#         #
#         # os.mkdir(self.file_path)
#
#         self.i = 0
#         self.duration = duration
#         self.fps = 50
#         self.video_name = name
#         self.t = 0
#
#         for key, value in kwargs.items():
#             setattr(self, key, value)
#
#         self.max_frames = int(self.duration * self.fps)
#         self.frames = []
#
#     def start_recording(self):
#         print('start recording,', self.duration, self.file_path)
#         window.fps_counter.enabled = False
#         window.exit_button.visible = False
#         self.frames = []
#         self.max_frames = self.duration * self.fps
#         if not self.file_path.exists():
#             self.file_path.mkdir()
#         base.movie(namePrefix=f'\\video_temp\\{self.video_name}', duration=self.duration, fps=self.fps, format='png', sd=4)
#
#         self.recording = True
#         invoke(self.stop_recording, delay=self.duration)
#
#     def stop_recording(self):
#         self.recording = False
#         window.fps_counter.enabled = True
#         window.exit_button.visible = True
#         print('stop recording')
#         # self.convert_to_gif()
#         self.convert_to_vid()
#
#     def update(self):
#         if not self.recording:
#             return
#
#             self.t += time.dt
#             if self.t >= 1 / 30:
#                 base.screenshot(
#                     namePrefix='\\video_temp\\' + self.video_name + '_' + str(self.i).zfill(4) + '.png',
#                     defaultFilename=0,
#                 )
#                 self.t = 0
#         self.i += 1
#
#     def convert_to_gif(self):
#         import imageio
#         images = []
#         if not os.path.exists(self.file_path):
#             return
#
#         for filename in os.listdir(self.file_path):
#             images.append(imageio.imread(self.file_path / filename))
#
#         imageio.mimsave(Path(f'{self.file_path.parent}/{self.video_name}.gif'), images)
#         shutil.rmtree(self.file_path)  # delete temp folder
#         print('saved gif to:', Path(f'{self.file_path.parent}/{self.video_name}.gif'))
#
#     def convert_to_vid(self):
#         import imageio
#         images = []
#         if not os.path.exists(self.file_path):
#             return
#
#         writer = imageio.get_writer('test.mp4', fps=self.fps)
#         for file in os.listdir(self.file_path):
#             im = imageio.imread(self.file_path / file)
#             writer.append_data(im)
#         writer.close()
#         print('Video saved!!')
#
#
# class VideoRecorderUI(WindowPanel):
#     def __init__(self, **kwargs):
#         self.duration_label = Text('duration:')
#         self.duration_field = InputField(default_value='5')
#         self.fps_label = Text('fps:')
#         self.fps_field = InputField(default_value='30')
#         self.name_label = Text('name:')
#         self.name_field = InputField(default_value='untitled_video')
#
#         self.start_button = Button(text='Start Recording [Shift+F12]', color=color.azure, on_click=self.start_recording)
#
#         super().__init__(
#             title='Video Recorder [F12]',
#             content=(
#                 self.duration_label,
#                 self.duration_field,
#                 self.fps_label,
#                 self.fps_field,
#                 self.name_label,
#                 self.name_field,
#                 Space(1),
#                 self.start_button,
#             ),
#         )
#         self.y = .5
#         self.scale *= .75
#         self.visible = False
#
#     def input(self, key):
#         if key == 'f12':
#             self.visible = not self.visible
#
#         if held_keys['shift'] and key == 'f12':
#             self.start_button.on_click()
#
#     def start_recording(self):
#         print(self.name_field)
#         if self.name_field.text == '':
#             self.name_field.blink(color.color(0, 1, 1, .5), .5)
#             print('enter name')
#             return
#
#         # self.start_button.color=color.lime
#         self.visible = False
#         application.video_recorder.duration = float(self.duration_field.text)
#         application.video_recorder.video_name = self.name_field.text
#         application.video_recorder.frame_skip = 60 // int(self.fps_field.text)
#         application.video_recorder.recording = True
#
#
# if __name__ == '__main__':
#     app = Ursina()
#     # window.size = (1600/3,900/3)
#     # cube = primitives.RedCube()
#     # cube.animate_x(5, duration=5, curve=curve.linear)
#     # cube.animate_x(0, duration=5, curve=curve.linear, delay=5)
#     # vr = VideoRecorder()
#     # invoke(setattr, vr, 'recording', True, delay=1)
#     # invoke(os._exit, 0, delay=6)
#     # vr.recording = True
#     window.size *= .5
#     from ursina.prefabs.first_person_controller import FirstPersonController
#     from ursina.shaders import lit_with_shadows_shader
#
#     random.seed(0)
#     Entity.default_shader = lit_with_shadows_shader
#
#     ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4, 4))
#
#     editor_camera = EditorCamera(enabled=False, ignore_paused=True)
#     player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8)
#     player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(1, 2, 1))
#
#     gun = Entity(model='cube', parent=camera, position=(.5, -.25, .25), scale=(.3, .2, 1), origin_z=-.5,
#                  color=color.red, on_cooldown=False)
#
#     shootables_parent = Entity()
#     mouse.traverse_target = shootables_parent
#
#     for i in range(16):
#         Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1, 2),
#                x=random.uniform(-8, 8),
#                z=random.uniform(-8, 8) + 8,
#                collider='box',
#                scale_y=random.uniform(2, 3),
#                color=color.hsv(0, 0, random.uniform(.9, 1))
#                )
#
#     sun = DirectionalLight()
#     sun.look_at(Vec3(1, -1, -1))
#     Sky()
#
#     vr = VideoRecorder(duration=10)
#
#
#     def input(key):
#         if key == '5':
#             vr.start_recording()
#         if key == '6':
#             vr.stop_recording()
#
#
#     app.run()
