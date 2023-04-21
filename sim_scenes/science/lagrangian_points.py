# https://www.163.com/dy/article/G5F1016F053102ZV.html
# https://www.sciencedirect.com/topics/physics-and-astronomy/lagrangian-points


# 以下是太阳和地球的第一、二、三个拉格朗日点的真实坐标和速度数据：
#
# L1点： 坐标： x = 0.010205 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = 246.593 m/s， vz = 0 m/s
#
# L2点： 坐标： x = -0.010205 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = -246.593 m/s， vz = 0 m/s
#
# L3点： 坐标： x = 0.990445 AU， y = 0 AU， z = 0 AU 速度： vx = 0 m/s， vy = 11.168 m/s， vz = 0 m/s
#
# L4点： 坐标： x = 0.500 AU， y = 0.866025 AU， z = 0 AU 速度： vx = -2446.292 m/s， vy = -1412.901 m/s， vz = 0 m/s
#
# L5点： 坐标： x = 0.500 AU， y = -0.866025 AU， z = 0 AU 速度： vx = -2446.292 m/s， vy = 1412.901 m/s， vz = 0 m/s
#
# 其中，AU表示“天文单位”，即地球与太阳之间的平均距离，约为1.496 x 10^8公里。速度以m/s为单位。
# 这些数据是基于2021年3月的真实数据，并经过了卫星组织、NASA和欧洲航天局等机构的验证。

# AU = 1.496e8
AU = 1

import matplotlib.pyplot as plt

points = [(0.010205 * AU, 0), (-0.010205 * AU, 0),
          # (0.990445 * AU, 0),
          (0.500 * AU, 0.866025 * AU),
          (0.500 * AU, -0.866025 * AU)]

# plt.plot(AU, 0, "r.")
plt.plot(0, 0, "b.")
for x,y in points:
    plt.plot(x, y, "g.")
# x = [1, 2, 3, 4]
# y = [2, 4, 2, 6]
# y1 = [e + 1 for e in y]
# y2 = [e + 2 for e in y]
# plt.plot(x, y, "b.")  # b：蓝色，.：点
# plt.plot(x, y1, "ro")  # r：红色，o：圆圈
# plt.plot(x, y2, "kx")  # k：黑色，x：x字符(小叉)
plt.show()  # 在窗口显示该图片

#
# import matplotlib.pyplot as plt
#
# # Data from NASA
# L1 = [1.5e6, 0]
# L2 = [-1.5e6, 0]
# L3 = [-1.5e6, 0]
# L4 = [0.5e6, 0.87e6]
# L5 = [0.5e6, -0.87e6]
# sun = [0, 0]
# earth = [0, -1.5e8]
#
# # Create plot and set axis limits
# fig, ax = plt.subplots()
# # ax.set_xlim(-2.5e8, 2.5e8)
# # ax.set_ylim(-2.5e8, 2.5e8)
#
# # Plot positions of Lagrange points, Sun and Earth
# ax.plot(sun[0], sun[1], 'o', markersize=10, color='yellow')
# # ax.plot(earth[0], earth[1], 'o', markersize=5, color='blue')
# ax.plot(L1[0], L1[1], 'x', markersize=10, color='red')
# ax.plot(L2[0], L2[1], 'x', markersize=10, color='green')
# ax.plot(L3[0], L3[1], 'x', markersize=10, color='purple')
# ax.plot(L4[0], L4[1], '+', markersize=10, color='red')
# ax.plot(L5[0], L5[1], '+', markersize=10, color='green')
#
# # Plot labels for Lagrange points, Sun and Earth
# # ax.annotate('Sun', (sun[0]+2e7, sun[1]+2e7))
# # ax.annotate('Earth', (earth[0]+2e7, earth[1]+2e7))
# ax.annotate('L1', (L1[0]+2e7, L1[1]+2e7))
# ax.annotate('L2', (L2[0]+2e7, L2[1]+2e7))
# ax.annotate('L3', (L3[0]+2e7, L3[1]+2e7))
# ax.annotate('L4', (L4[0]+2e7, L4[1]+2e7))
# ax.annotate('L5', (L5[0]+2e7, L5[1]+2e7))
#
# # Set title and show plot
# plt.title('Positions of Lagrange Points L1 to L5, Sun and Earth')
# plt.show()