<p align="center">
  <strong>宇宙模拟器（Python玩转宇宙）</strong>
</p> 

# 介绍
这个宇宙模拟器是基于万有引力定理的模拟器，它可以模拟出宇宙中各个天体之间的引力作用，进而模拟它们的运动轨迹。万有引力定理是指，在宇宙中，任意两个物体之间都会有一个相互吸引的力，这个力的大小与它们的质量成正比，与它们之间的距离的平方成反比。利用这个定理，我们可以模拟出天体的运动，预测它们的位置和轨迹。这个宇宙模拟器还包含了一些可视化的功能，可以让用户更加直观地了解天体的运动状态。


这个宇宙模拟器是基于万有引力定理的模拟器，它可以模拟出宇宙中各个天体之间的引力作用，进而模拟它们的运动轨迹。万有引力定理是指，在宇宙中，任意两个物体之间都会有一个相互吸引的力，这个力的大小与它们的质量成正比，与它们之间的距离的平方成反比。利用这个定理，我们可以模拟出天体的运动，预测它们的位置和轨迹。这个宇宙模拟器还包含了一些可视化的功能，可以让用户更加直观地了解天体的运动状态。

结合下面的信息，再写一个。 项目名为：宇宙模拟器（Python玩转宇宙），内容包含太阳系、大恒星比较、引力弹弓、月球、戴森球、三体模拟等等

宇宙模拟器是一个基于Python语言的开源项目，通过数值模拟万有引力定理来模拟宇宙的运行轨迹。该项目包含了太阳系中各行星、卫星的轨迹和运行状态，可以进行实时观察和交互操作。同时，该项目还可以模拟不同恒星之间的相互作用，比较它们的不同特点和影响，还可以进行引力弹弓的实验，以及月球和戴森球的模拟等等。此外，该项目还包含了三体模拟，可帮助用户更好地理解三体问题。这个项目不仅可以让你更深入地了解宇宙，还可以为你提供一个学习Python编程的平台。

我们可以自己通过调整天体的初始坐标、质量和矢量速度等等参数来自定义各种场景来控制天体的运行效果。

# 模拟器效果图
<img src="https://gitcode.net/pythoncr/three_body_sim/-/raw/master/images/solar_system_3.png" width="80.7%">


# 抖音课堂：
<img src="https://gitcode.net/pythoncr/three_body_sim/-/raw/master/images/douyin_x.jpg" width="40%">

# 课程下载
https://gitcode.net/pythoncr/universe_sim

# 目录说明

**bodies** 天体类、包含太阳以及太阳系中的所有行星
 
**common** 公共库代码
  
**data** 构建天体的 JSON 数据
   
**scenes**  各种天体系统运行场景 **演示入口**

**textures**  天体纹理图片

**simulators** 天体系统运行模拟器
    
**images** 图片

# 安装 Python 库
```shell script
# 先安装基础包
pip install -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com ursina
```

# 支持三种模拟器
```shell script
# 进入当前代码的根目录
cd e:\universe_sim\
SET PYTHONPATH=%CD%

# matplotlib 模拟器（支持动画和导出 gif 文件）
python simulators\mpl_simulator.py

# mayavi模拟器
python simulators\mayavi_simulator.py

# ursina模拟器
python simulators\ursina_simulator.py
```

# 模拟场景运行
```shell script
# 进入当前代码的根目录
cd e:\universe_sim\
SET PYTHONPATH=%CD%

# 场景
# 从运行demo开始
python sim_scenes/demo.py

# 三体场景
# 3个太阳、1个地球（效果1）
python sim_scenes/three_body_01.py

# 3个太阳、1个地球（效果2）
python sim_scenes/three_body_02.py

# 太阳系场景
# 以下展示的效果为太阳系真实的距离
# 由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
python sim_scenes/solar_system_1.py

# 以下展示的效果非太阳系真实的距离和大小
# 1、由于宇宙空间尺度非常大，如果按照实际的天体大小，则无法看到天体，因此需要对天体的尺寸进行放大
# 2、为了达到最佳的显示效果，对每个行星天体的距离进行了缩放
python sim_scenes/solar_system_2.py

# 以下展示的效果非太阳系真实的距离和大小
# 1、由于宇宙空间尺度非常大，按照实际的大小无法看到行星天体，因此需要对天体的尺寸进行放大
# 2、为了达到最佳的显示效果，对每个行星天体的距离进行了缩放
# 3、加入了小行星的演示效果
python sim_scenes/solar_system_3.py

# 太阳、地球运行效果
python sim_scenes/sun_earth.py

# 太阳、地球、木星运行效果
python sim_scenes/sun_earth_jupiter.py 
```

版权声明：

本代码仅供学习交流使用，不得用于商业用途。如需引用、传递、分享本代码，请务必注明出处并附上本声明，否则将被视为侵权行为。

本代码仅为作者个人独立创作，未经作者允许，禁止将其用于任何商业用途或用于违反法律法规的行为。

如有任何问题或疑问，请联系作者并注明代码来源，感谢您的支持和理解。


本项目的开源代码和资料仅供学习和参考使用，不能用于商业目的。任何直接或间接使用本项目的全部或部分内容所导致的后果，均由使用者自行承担责任，与本项目作者无关。

本项目的代码和资料来源于多方面的信息和知识，作者已尽力确保其准确性和完整性。然而，由于人为因素或其他不可抗力因素，本项目无法保证其内容的完全准确性和及时性。使用者应该自行验证和核实其所使用的任何代码和资料，作者不承担任何直接或间接的责任和义务。

本项目的开源代码和资料可能包含来自第三方的知识产权和版权，作者已尽力尊重和保护这些权益。如果本项目的内容侵犯了任何人的知识产权和版权，请通过pythoncr@126.com与作者联系，作者会尽快删除相关内容。

本项目作者拥有对本项目的最终解释权和修改权，作者保留在任何时候修改或终止本项目的权利。

# 免责声明
* 本项目开源代码和资料主要用于教学，任何直接或间接因使用我方的任何内容所导致的全部后果与我方无关，若使用者无法对使用我方内容后的任何后果负责，请不要使用我方的任何内容。若我方的任何内容侵犯了您的法律权益，请联系pythoncr@126.com，作者会第一时间删除侵权内容。