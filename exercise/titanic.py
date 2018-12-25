#!/usr/bin/python3

#import pandas as pd
# data = {
#     "Id": [1, 2, 3, 4, 5, 6, 7, 8, 9],
#     "Sex": [1, 0, 0, 0, 1, 1, 1, 1, 0],
#     "Age": [22, 38, 26, 35, 35, None, 54, 2, 27],
#     "Survived": [0, 1, 0, 1, 0, 1, 1, 0, 1]
# }
#
# df = pd.DataFrame(data)
# df.fillna(df.mean(), inplace=True)
# print("平均年齢は: {}".format(df.mean()["Age"]))
# males = df["Sex"] == 1
# females = df["Sex"] == 0
# count_m = df.loc[males, "Survived"].sum()
# count_f = df.loc[females, "Survived"].sum()
# print("男性の生存率は: {}".format(count_m/males.sum() * 100) + "%")
# print("女性の生存率は: {}".format(count_f/females.sum() * 100) + "%")

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


fig, ax = plt.subplots()

Path = mpath.Path
path_data = [
    (Path.MOVETO, (1.58, -2.57)),
    (Path.CURVE4, (0.35, -1.1)),
    (Path.CURVE4, (-1.75, 2.0)),
    (Path.CURVE4, (0.375, 2.0)),
    (Path.LINETO, (0.85, 1.15)),
    (Path.CURVE4, (2.2, 3.2)),
    (Path.CURVE4, (3, 0.05)),
    (Path.CURVE4, (2.0, -0.5)),
    (Path.CLOSEPOLY, (1.58, -2.57)),
    ]
codes, verts = zip(*path_data)
path = mpath.Path(verts, codes)
patch = mpatches.PathPatch(path, facecolor='r', alpha=0.5)
ax.add_patch(patch)

# plot control points and connecting lines
x, y = zip(*path.vertices)
line, = ax.plot(x, y, 'go-')

ax.grid()
ax.axis('equal')
plt.show()

