<p align="center">
  <strong>宇宙模拟器（Python玩转宇宙）</strong>
</p> 

# 介绍
《宇宙模拟器》是一个基于Python语言的开源项目，通过万有引力定理来模拟宇宙的运行轨迹。该项目包含了太阳系中各行星的轨迹和运行状态，可以进行任意角度观察和交互操作。同时，该项目还模拟了引力弹弓的实验、月球的月相变化过程和戴森球的模拟等等。此外，该项目还包含了三体模拟，帮助用户更好地理解三体问题。这个项目不仅可以让大家更深入地了解宇宙，还提供了一个学习Python3D编程的平台。
# 模拟器效果图
<img src="images/1.png?raw=true" width="80.7%">
<img src="images/2.png?raw=true" width="80.7%">
<img src="images/3.png?raw=true" width="80.7%">
<img src="images/4.png?raw=true" width="80.7%">

# 抖音课堂：
<img src="https://gitcode.net/pythoncr/universe_sim/-/raw/master/images/douyin_x.jpg" width="40%">

# 课程下载
https://gitcode.net/pythoncr/universe_sim

# 目录说明

**bodies** 天体类、包含太阳和太阳系中的所有行星、以及超过太阳大小的巨大恒星
 
**common** 公共库代码
  
**data** 构建天体的 JSON 数据，可以通过 sim_scenes/ursina_json_sim.py 来运行
  
**images** 图片

**sim_scenes**  各种天体系统运行场景的【演示入口】，目前包含：太阳系、三体、科学和科幻各种场景

**simulators** 天体系统运行模拟器

**sounds** 音乐和声音

**textures**  天体纹理图片

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

# ursina模拟器（推荐模拟器）
python simulators\ursina_simulator.py

# matplotlib 模拟器（支持动画和导出 gif 文件）
python simulators\mpl_simulator.py

# mayavi模拟器
python simulators\mayavi_simulator.py
```

# 模拟场景运行
```shell script
# 进入当前代码的根目录
cd e:\universe_sim\
SET PYTHONPATH=%CD%

# 场景
# 从运行demo开始
python sim_scenes/demo.py

# 运行其他场景
python sim_scenes/xxx/xxx.py
```

# 版权声明：

* 本代码仅供学习交流使用，不得用于商业用途。如需引用、传递、分享本代码，请务必注明出处并附上本声明，否则将被视为侵权行为。

* 本代码仅为作者个人独立创作，未经作者允许，禁止将其用于任何商业用途或用于违反法律法规的行为。

* 如有任何问题或疑问，请联系作者（pythoncr@126.com）并注明代码来源，感谢您的支持和理解。



# 免责声明
* 本项目的代码和资料来源于多方面的信息和知识，作者已尽力确保其准确性和完整性。然而，由于人为因素或其他不可抗力因素，本项目无法保证其内容的完全准确性和及时性。
使用者应该自行验证和核实其所使用的任何代码和资料，作者不承担任何直接或间接的责任和义务。

* 本项目的开源代码和资料可能包含来自第三方的知识产权和版权，作者已尽力尊重和保护这些权益。
如果本项目的内容侵犯了任何人的知识产权和版权，请通过 pythoncr@126.com 与作者联系，作者会尽快删除相关内容。

* 本项目作者拥有对本项目的最终解释权和修改权，作者保留在任何时候修改或终止本项目的权利。
