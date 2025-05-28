"""
可视化组件
提供数据可视化功能
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import DataProcessor
from typing import Optional, List, Dict

class Visualizer:
    """可视化类，用于生成数据可视化"""
    
    def __init__(self, data_processor: DataProcessor):
        """
        初始化可视化器
        
        Args:
            data_processor: 数据处理器实例
        """
        self.data_processor = data_processor
    
    def display_visualization_options(self):
        """显示可视化选项"""
        if self.data_processor.data is None:
            return
            
        st.subheader("数据可视化")
        
        # 获取列类型
        column_types = self.data_processor.get_column_types()
        
        # 创建选项卡
        tab1, tab2, tab3 = st.tabs(["基本图表", "相关性分析", "时间序列"])
        
        # 基本图表选项卡
        with tab1:
            self._display_basic_charts(column_types)
        
        # 相关性分析选项卡
        with tab2:
            self._display_correlation_analysis()
        
        # 时间序列选项卡
        with tab3:
            self._display_time_series_options(column_types)
    
    def _display_basic_charts(self, column_types: Dict):
        """
        显示基本图表选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择图表类型
        chart_type = st.selectbox(
            "选择图表类型",
            options=["柱状图", "折线图", "散点图", "直方图", "箱线图", "饼图"],
            key="basic_chart_type"
        )
        
        # 根据图表类型显示不同的选项
        if chart_type == "柱状图":
            self._display_bar_chart_options(column_types)
        elif chart_type == "折线图":
            self._display_line_chart_options(column_types)
        elif chart_type == "散点图":
            self._display_scatter_plot_options(column_types)
        elif chart_type == "直方图":
            self._display_histogram_options(column_types)
        elif chart_type == "箱线图":
            self._display_box_plot_options(column_types)
        elif chart_type == "饼图":
            self._display_pie_chart_options(column_types)
    
    def _display_bar_chart_options(self, column_types: Dict):
        """
        显示柱状图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择X轴
        x_column = st.selectbox(
            "选择X轴(分类变量)",
            options=column_types["分类型"] + column_types["布尔型"],
            key="bar_x_column"
        )
        
        # 选择Y轴
        y_column = st.selectbox(
            "选择Y轴(数值变量)",
            options=column_types["数值型"],
            key="bar_y_column"
        )
        
        # 选择颜色变量(可选)
        color_column = st.selectbox(
            "选择颜色变量(可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"],
            key="bar_color_column"
        )
        
        # 生成图表按钮
        if st.button("生成柱状图", key="generate_bar_chart"):
            # 准备数据
            df = self.data_processor.data
            
            # 创建图表
            if color_column != "无":
                fig = px.bar(
                    df, 
                    x=x_column, 
                    y=y_column, 
                    color=color_column,
                    title=f"{x_column} vs {y_column} 柱状图",
                    labels={x_column: x_column, y_column: y_column}
                )
            else:
                fig = px.bar(
                    df, 
                    x=x_column, 
                    y=y_column,
                    title=f"{x_column} vs {y_column} 柱状图",
                    labels={x_column: x_column, y_column: y_column}
                )
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_line_chart_options(self, column_types: Dict):
        """
        显示折线图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择X轴
        x_column = st.selectbox(
            "选择X轴",
            options=column_types["数值型"] + column_types["日期型"],
            key="line_x_column"
        )
        
        # 选择Y轴
        y_column = st.selectbox(
            "选择Y轴",
            options=column_types["数值型"],
            key="line_y_column"
        )
        
        # 选择颜色变量(可选)
        color_column = st.selectbox(
            "选择颜色变量(可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"],
            key="line_color_column"
        )
        
        # 生成图表按钮
        if st.button("生成折线图", key="generate_line_chart"):
            # 准备数据
            df = self.data_processor.data
            
            # 创建图表
            if color_column != "无":
                fig = px.line(
                    df, 
                    x=x_column, 
                    y=y_column, 
                    color=color_column,
                    title=f"{x_column} vs {y_column} 折线图",
                    labels={x_column: x_column, y_column: y_column}
                )
            else:
                fig = px.line(
                    df, 
                    x=x_column, 
                    y=y_column,
                    title=f"{x_column} vs {y_column} 折线图",
                    labels={x_column: x_column, y_column: y_column}
                )
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_scatter_plot_options(self, column_types: Dict):
        """
        显示散点图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择X轴
        x_column = st.selectbox(
            "选择X轴",
            options=column_types["数值型"],
            key="scatter_x_column"
        )
        
        # 选择Y轴
        y_column = st.selectbox(
            "选择Y轴",
            options=column_types["数值型"],
            key="scatter_y_column"
        )
        
        # 选择颜色变量(可选)
        color_column = st.selectbox(
            "选择颜色变量(可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"] + column_types["数值型"],
            key="scatter_color_column"
        )
        
        # 选择大小变量(可选)
        size_column = st.selectbox(
            "选择大小变量(可选)",
            options=["无"] + column_types["数值型"],
            key="scatter_size_column"
        )
        
        # 生成图表按钮
        if st.button("生成散点图", key="generate_scatter_plot"):
            # 准备数据
            df = self.data_processor.data
            
            # 创建图表参数
            scatter_params = {
                "x": x_column,
                "y": y_column,
                "title": f"{x_column} vs {y_column} 散点图",
                "labels": {x_column: x_column, y_column: y_column}
            }
            
            # 添加颜色参数
            if color_column != "无":
                scatter_params["color"] = color_column
            
            # 添加大小参数
            if size_column != "无":
                scatter_params["size"] = size_column
            
            # 创建图表
            fig = px.scatter(df, **scatter_params)
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_histogram_options(self, column_types: Dict):
        """
        显示直方图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择变量
        column = st.selectbox(
            "选择变量",
            options=column_types["数值型"],
            key="hist_column"
        )
        
        # 选择分箱数
        bins = st.slider(
            "选择分箱数",
            min_value=5,
            max_value=100,
            value=30,
            step=5,
            key="hist_bins"
        )
        
        # 选择颜色变量(可选)
        color_column = st.selectbox(
            "选择颜色变量(可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"],
            key="hist_color_column"
        )
        
        # 生成图表按钮
        if st.button("生成直方图", key="generate_histogram"):
            # 准备数据
            df = self.data_processor.data
            
            # 创建图表
            if color_column != "无":
                fig = px.histogram(
                    df, 
                    x=column, 
                    color=color_column,
                    nbins=bins,
                    title=f"{column} 直方图",
                    labels={column: column}
                )
            else:
                fig = px.histogram(
                    df, 
                    x=column,
                    nbins=bins,
                    title=f"{column} 直方图",
                    labels={column: column}
                )
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_box_plot_options(self, column_types: Dict):
        """
        显示箱线图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择Y轴(数值变量)
        y_column = st.selectbox(
            "选择Y轴(数值变量)",
            options=column_types["数值型"],
            key="box_y_column"
        )
        
        # 选择X轴(分类变量，可选)
        x_column = st.selectbox(
            "选择X轴(分类变量，可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"],
            key="box_x_column"
        )
        
        # 选择颜色变量(可选)
        color_column = st.selectbox(
            "选择颜色变量(可选)",
            options=["无"] + column_types["分类型"] + column_types["布尔型"],
            key="box_color_column"
        )
        
        # 生成图表按钮
        if st.button("生成箱线图", key="generate_box_plot"):
            # 准备数据
            df = self.data_processor.data
            
            # 创建图表参数
            box_params = {
                "y": y_column,
                "title": f"{y_column} 箱线图",
                "labels": {y_column: y_column}
            }
            
            # 添加X轴参数
            if x_column != "无":
                box_params["x"] = x_column
            
            # 添加颜色参数
            if color_column != "无":
                box_params["color"] = color_column
            
            # 创建图表
            fig = px.box(df, **box_params)
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_pie_chart_options(self, column_types: Dict):
        """
        显示饼图选项
        
        Args:
            column_types: 列类型字典
        """
        # 选择名称变量
        names_column = st.selectbox(
            "选择名称变量",
            options=column_types["分类型"] + column_types["布尔型"],
            key="pie_names_column"
        )
        
        # 选择值变量
        values_column = st.selectbox(
            "选择值变量",
            options=column_types["数值型"],
            key="pie_values_column"
        )
        
        # 生成图表按钮
        if st.button("生成饼图", key="generate_pie_chart"):
            # 准备数据
            df = self.data_processor.data
            
            # 对数据进行分组和聚合
            pie_data = df.groupby(names_column)[values_column].sum().reset_index()
            
            # 创建图表
            fig = px.pie(
                pie_data, 
                names=names_column, 
                values=values_column,
                title=f"{names_column} 饼图",
                labels={names_column: names_column, values_column: values_column}
            )
            
            # 显示图表
            st.plotly_chart(fig, use_container_width=True)
    
    def _display_correlation_analysis(self):
        """显示相关性分析选项"""
        # 生成相关性热图按钮
        if st.button("生成相关性热图", key="generate_correlation_heatmap"):
            # 获取相关性矩阵
            corr = self.data_processor.get_correlation_matrix()
            
            if corr is not None and not corr.empty:
                # 创建热图
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    aspect="auto",
                    title="相关性热图"
                )
                
                # 显示热图
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("无法生成相关性热图，请确保数据包含数值型列。")
    
    def _display_time_series_options(self, column_types: Dict):
        """
        显示时间序列选项
        
        Args:
            column_types: 列类型字典
        """
        # 检查是否有日期列
        date_columns = column_types["日期型"]
        
        # 如果没有日期列，尝试转换
        if not date_columns:
            st.info("未检测到日期列，请选择一个可以转换为日期的列。")
            
            # 选择可能的日期列
            possible_date_column = st.selectbox(
                "选择可能的日期列",
                options=column_types["分类型"],
                key="time_series_date_column"
            )
            
            # 选择值列
            value_column = st.selectbox(
                "选择值列",
                options=column_types["数值型"],
                key="time_series_value_column"
            )
            
            # 生成时间序列图按钮
            if st.button("生成时间序列图", key="generate_time_series"):
                # 尝试生成时间序列图
                html_content = self.data_processor.get_time_series_analysis(
                    possible_date_column,
                    value_column
                )
                
                if html_content:
                    # 显示时间序列图
                    st.components.v1.html(html_content, height=500)
                else:
                    st.error("无法生成时间序列图，请确保选择的列可以转换为日期。")
        else:
            # 选择日期列
            date_column = st.selectbox(
                "选择日期列",
                options=date_columns,
                key="time_series_date_column"
            )
            
            # 选择值列
            value_column = st.selectbox(
                "选择值列",
                options=column_types["数值型"],
                key="time_series_value_column"
            )
            
            # 生成时间序列图按钮
            if st.button("生成时间序列图", key="generate_time_series"):
                # 生成时间序列图
                html_content = self.data_processor.get_time_series_analysis(
                    date_column,
                    value_column
                )
                
                if html_content:
                    # 显示时间序列图
                    st.components.v1.html(html_content, height=500)
                else:
                    st.error("无法生成时间序列图，请检查数据。")
