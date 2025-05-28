"""
文件处理组件
提供文件上传和处理功能
"""
import streamlit as st
import pandas as pd
from utils.data_utils import DataProcessor
from typing import Optional, Tuple

class FileProcessor:
    """文件处理类，用于处理上传的文件"""
    
    def __init__(self):
        """初始化文件处理器"""
        # 初始化数据处理器
        self.data_processor = DataProcessor()
        
        # 初始化会话状态
        if "data_loaded" not in st.session_state:
            st.session_state.data_loaded = False
        
        if "file_name" not in st.session_state:
            st.session_state.file_name = None
    
    def display_file_uploader(self) -> bool:
        """
        显示文件上传组件
        
        Returns:
            bool: 是否成功上传并处理文件
        """
        # 创建文件上传组件
        uploaded_file = st.file_uploader(
            "上传CSV或Excel文件",
            type=["csv", "xlsx", "xls"],
            help="支持CSV和Excel文件格式"
        )
        
        # 如果有文件上传
        if uploaded_file is not None:
            # 加载数据
            if self.data_processor.load_data(uploaded_file):
                st.session_state.data_loaded = True
                st.session_state.file_name = uploaded_file.name
                return True
            else:
                st.error("文件加载失败，请确保文件格式正确。")
                return False
        
        return False
    
    def display_data_preview(self):
        """显示数据预览"""
        if st.session_state.data_loaded:
            # 获取数据预览
            preview = self.data_processor.get_data_preview()
            if preview is not None:
                st.subheader("数据预览")
                st.dataframe(preview, use_container_width=True)
    
    def display_data_info(self):
        """显示数据信息"""
        if st.session_state.data_loaded:
            # 获取数据信息
            info = self.data_processor.get_data_info()
            if info:
                st.subheader("数据信息")
                
                # 显示基本信息
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**行数:** {info['行数']}")
                    st.write(f"**列数:** {info['列数']}")
                    st.write(f"**文件类型:** {info['文件类型']}")
                
                with col2:
                    st.write(f"**文件名:** {info['文件名']}")
                    
                # 显示列名
                with st.expander("列名"):
                    st.write(", ".join(info['列名']))
                
                # 显示数据类型
                with st.expander("数据类型"):
                    for col, dtype in info['数据类型'].items():
                        st.write(f"**{col}:** {dtype}")
                
                # 显示缺失值
                with st.expander("缺失值"):
                    for col, count in info['缺失值'].items():
                        if count > 0:
                            st.write(f"**{col}:** {count} ({count/info['行数']*100:.2f}%)")
    
    def display_descriptive_stats(self):
        """显示描述性统计信息"""
        if st.session_state.data_loaded:
            # 获取描述性统计信息
            stats = self.data_processor.get_descriptive_stats()
            if stats is not None and not stats.empty:
                with st.expander("描述性统计"):
                    st.dataframe(stats, use_container_width=True)
    
    def get_data_processor(self) -> DataProcessor:
        """
        获取数据处理器
        
        Returns:
            DataProcessor: 数据处理器实例
        """
        return self.data_processor
    
    def is_data_loaded(self) -> bool:
        """
        检查数据是否已加载
        
        Returns:
            bool: 数据是否已加载
        """
        return st.session_state.data_loaded
    
    def reset_data(self):
        """重置数据"""
        st.session_state.data_loaded = False
        st.session_state.file_name = None
        self.data_processor = DataProcessor()
