import pandas as pd
from pyecharts import Line

df = pd.read_csv('diff.csv')
attr = [i[0] for i in df.values]
v1 = [i[1] for i in df.values]
line = Line("okcn/okquanter价差监控")
line.add("价差", attr, v1, mark_point=["average"])
# line.add("商家B", attr, v2, is_smooth=True, mark_line=["max", "average"])
line.render('./data/index.html')