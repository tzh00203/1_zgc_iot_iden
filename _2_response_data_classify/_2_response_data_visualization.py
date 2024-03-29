"""
    将处理的responseData进行可视化操作
"""

from __utils.__path_util import global_path
import json
from pyecharts import options as opts
from pyecharts.charts import Pie

protocol_type_path = global_path.__sinan_cluster_root_path__ + "protocol_type.json"


def protocol_visualize_pie():
    """
    把协议类型可视化为病状图
    :return: None
    """
    f1 = open(protocol_type_path, "r", encoding="utf-8").read()
    protocol_type_json = json.loads(f1)
    print("The number of categories: ", len(protocol_type_json))
    data = protocol_type_json
    # 将字典数据转换为列表形式
    data_list = [list(z) for z in zip(data.keys(), data.values())]

    # 创建 Pie 实例
    pie = (
        Pie()
        .add("", data_list)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="response_types_pie"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="right", orient="vertical")
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    # 渲染图表到 HTML 文件
    pie.render("protocol_type_pie_chart.html")


if __name__ == "__main__":
    protocol_visualize_pie()




