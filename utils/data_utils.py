"""
数据处理工具模块
提供数据加载、预处理和基本分析功能
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import io
from typing import Dict, List, Tuple, Union, Optional

class DataProcessor:
    """数据处理类，用于处理CSV和Excel文件"""
    
    def __init__(self):
        self.data = None
        self.file_type = None
        self.file_name = None
        
    def load_data(self, uploaded_file) -> bool:
        """
        加载上传的数据文件
        
        Args:
            uploaded_file: Streamlit上传的文件对象
            
        Returns:
            bool: 是否成功加载数据
        """
        try:
            file_name = uploaded_file.name
            self.file_name = file_name
            
            if file_name.endswith('.csv'):
                self.data = pd.read_csv(uploaded_file)
                self.file_type = 'csv'
            elif file_name.endswith(('.xls', '.xlsx')):
                self.data = pd.read_excel(uploaded_file)
                self.file_type = 'excel'
            else:
                return False
                
            return True
        except Exception as e:
            print(f"加载数据时出错: {e}")
            return False
    
    def get_data_preview(self, rows: int = 5) -> pd.DataFrame:
        """
        获取数据预览
        
        Args:
            rows: 预览的行数
            
        Returns:
            pd.DataFrame: 数据预览
        """
        if self.data is not None:
            return self.data.head(rows)
        return None
    
    def get_data_info(self) -> Dict:
        """
        获取数据基本信息
        
        Returns:
            Dict: 包含数据基本信息的字典
        """
        if self.data is None:
            return {}
            
        info = {
            "行数": len(self.data),
            "列数": len(self.data.columns),
            "列名": list(self.data.columns),
            "数据类型": {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            "缺失值": self.data.isnull().sum().to_dict(),
            "文件类型": self.file_type,
            "文件名": self.file_name
        }
        return info
    
    def get_descriptive_stats(self) -> pd.DataFrame:
        """
        获取描述性统计信息
        
        Returns:
            pd.DataFrame: 描述性统计信息
        """
        if self.data is None:
            return None
            
        # 只对数值列进行描述性统计
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            return self.data[numeric_cols].describe()
        return pd.DataFrame()
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """
        获取相关性矩阵
        
        Returns:
            pd.DataFrame: 相关性矩阵
        """
        if self.data is None:
            return None
            
        # 只对数值列计算相关性
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            return self.data[numeric_cols].corr()
        return pd.DataFrame()
    
    def generate_correlation_heatmap(self) -> Optional[str]:
        """
        生成相关性热图
        
        Returns:
            str: 热图的HTML字符串
        """
        if self.data is None:
            return None
            
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            corr = self.data[numeric_cols].corr()
            fig = px.imshow(
                corr, 
                text_auto=True, 
                aspect="auto",
                title="相关性热图"
            )
            return fig.to_html()
        return None
    
    def generate_summary_plots(self, column: str) -> Optional[str]:
        """
        为指定列生成摘要图表
        
        Args:
            column: 列名
            
        Returns:
            str: 图表的HTML字符串
        """
        if self.data is None or column not in self.data.columns:
            return None
            
        # 检查数据类型并生成相应的图表
        if pd.api.types.is_numeric_dtype(self.data[column]):
            # 数值型数据生成直方图
            fig = px.histogram(
                self.data, 
                x=column,
                title=f"{column} 分布",
                labels={column: column},
                marginal="box"  # 添加箱线图
            )
            return fig.to_html()
        else:
            # 分类数据生成条形图
            value_counts = self.data[column].value_counts().reset_index()
            value_counts.columns = ['value', 'count']
            fig = px.bar(
                value_counts, 
                x='value', 
                y='count',
                title=f"{column} 分布",
                labels={'value': column, 'count': '计数'}
            )
            return fig.to_html()
    
    def detect_outliers(self, method: str = 'iqr') -> Dict:
        """
        检测异常值
        
        Args:
            method: 检测方法，'iqr'或'zscore'
            
        Returns:
            Dict: 包含异常值信息的字典
        """
        if self.data is None:
            return {}
            
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        outliers = {}
        
        for col in numeric_cols:
            if method == 'iqr':
                # IQR方法
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outlier_indices = self.data[(self.data[col] < lower_bound) | (self.data[col] > upper_bound)].index
                if len(outlier_indices) > 0:
                    outliers[col] = {
                        'count': len(outlier_indices),
                        'percentage': len(outlier_indices) / len(self.data) * 100,
                        'bounds': (lower_bound, upper_bound)
                    }
            elif method == 'zscore':
                # Z-score方法
                mean = self.data[col].mean()
                std = self.data[col].std()
                z_scores = abs((self.data[col] - mean) / std)
                outlier_indices = self.data[z_scores > 3].index  # Z-score > 3
                if len(outlier_indices) > 0:
                    outliers[col] = {
                        'count': len(outlier_indices),
                        'percentage': len(outlier_indices) / len(self.data) * 100,
                        'threshold': 3
                    }
                    
        return outliers
    
    def get_time_series_analysis(self, date_column: str, value_column: str) -> Optional[str]:
        """
        进行时间序列分析
        
        Args:
            date_column: 日期列名
            value_column: 值列名
            
        Returns:
            str: 时间序列图的HTML字符串
        """
        if self.data is None or date_column not in self.data.columns or value_column not in self.data.columns:
            return None
            
        try:
            # 确保日期列是日期类型
            self.data[date_column] = pd.to_datetime(self.data[date_column])
            
            # 按日期排序
            df_sorted = self.data.sort_values(by=date_column)
            
            # 创建时间序列图
            fig = px.line(
                df_sorted, 
                x=date_column, 
                y=value_column,
                title=f"{value_column} 随时间变化趋势",
                labels={date_column: "日期", value_column: value_column}
            )
            return fig.to_html()
        except Exception as e:
            print(f"时间序列分析出错: {e}")
            return None
    
    def get_column_types(self) -> Dict:
        """
        获取列的数据类型分类
        
        Returns:
            Dict: 按类型分类的列名
        """
        if self.data is None:
            return {}
            
        column_types = {
            "数值型": list(self.data.select_dtypes(include=['number']).columns),
            "分类型": list(self.data.select_dtypes(include=['object', 'category']).columns),
            "日期型": list(self.data.select_dtypes(include=['datetime']).columns),
            "布尔型": list(self.data.select_dtypes(include=['bool']).columns)
        }
        return column_types
