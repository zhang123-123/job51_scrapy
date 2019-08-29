# -*- coding: utf-8 -*-
# from pyecharts import Pie
# attr = ["python", "php", "c", "java", "html"]
# v1 = [11, 12, 13, 10, 10, 10]
# pie = Pie("饼图示例")
# pie.add("python", attr, v1, is_label_show=True)
# pie.show_config()
# pie.render()
# //导入饼图Pie
from pyecharts import Pie
# 设置行名
columns = ["一月", "二月", "三月", "四月", "五月", "六月"]
# 设置数据
data1 = [114, 55, 27, 125, 27, 105]
data2 = [25, 80, 70, 100, 50, 66]
data3 = [25, 80, 70, 100, 50, 66]
# //设置主标题与副标题，标题设置居中，设置宽度为900
pie = Pie("饼状图", title_pos='center', width=1500)
# //加入数据，设置坐标位置为【25，50】，上方的colums选项取消显示
pie.add("python", columns, data1, center=[25, 50], is_label_show=False)
# //加入数据，设置坐标位置为【75，50】，上方的colums选项取消显示，显示label标签
pie.add("php", columns, data2, center=[75, 50], is_label_show=True)
pie.add("java", columns, data3, center=[125, 50], is_label_show=True)
# //保存图表
pie.render()

