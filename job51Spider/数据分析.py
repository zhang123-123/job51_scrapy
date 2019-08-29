# -*- coding: utf-8 -*-
# python的数据分析库
# pandas  numpy
# import pandas as pd
# import numpy
#
# pd.read_clipboard()
# pd.read_csv()
# pd.read_excel()
# # pd.read_html()
# pd.read_json()

# python 的图表绘制
# matplotlib
# pyecharts 用python对echart做了个封装
# turtle/seaborn
# import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# image data
a = np.array([0.313660827978, 0.365348418405, 0.423733120134,
              0.365348418405, 0.439599930621, 0.525083754405,
              0.423733120134, 0.525083754405, 0.651536351379]).reshape(3,3)

"""
for the value of "interpolation", check this:
http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
for the value of "origin"= ['upper', 'lower'], check this:
http://matplotlib.org/examples/pylab_examples/image_origin.html
"""
plt.imshow(a, interpolation='nearest', cmap='bone', origin='lower')
plt.colorbar(shrink=.92)

plt.xticks(())
plt.yticks(())
plt.show()