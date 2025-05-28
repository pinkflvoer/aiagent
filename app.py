"""
数据分析智能体主应用
集成所有组件，提供完整的数据分析体验
"""
import streamlit as st
import os
from components.chat_interface import ChatInterface
from components.file_processor import FileProcessor
from components.visualizer import Visualizer
from utils.openai_utils import OpenAIUtils
from utils.data_utils import DataProcessor

# 设置页面配置
st.set_page_config(
    page_title="数据分析智能体",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("📊 数据分析智能体")
st.markdown("上传CSV或Excel文件，通过聊天界面进行数据分析和预测分析。")

# 初始化会话状态
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None

if "data_processor" not in st.session_state:
    st.session_state.data_processor = DataProcessor()

# 创建侧边栏
with st.sidebar:
    st.header("设置")
    
    # OpenAI API密钥输入
    api_key = st.text_input(
        "OpenAI API密钥",
        type="password",
        placeholder="输入您的OpenAI API密钥",
        help="需要OpenAI API密钥才能使用智能分析功能"
    )
    
    if api_key:
        st.session_state.openai_api_key = api_key
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.divider()
    
    # 文件上传部分
    st.subheader("数据上传")
    file_processor = FileProcessor()
    
    # 显示文件上传组件
    if file_processor.display_file_uploader():
        st.success(f"成功加载文件: {st.session_state.file_name}")
    
    # 重置数据按钮
    if st.button("重置数据", key="reset_data"):
        file_processor.reset_data()
        st.rerun()
    
    st.divider()
    
    # 关于部分
    st.subheader("关于")
    st.markdown("""
    **数据分析智能体**是一个结合Streamlit、LangChain和OpenAI API的应用，
    可以帮助您分析CSV和Excel数据，提供数据洞察和预测分析。
    
    使用方法：
    1. 上传CSV或Excel文件
    2. 输入OpenAI API密钥
    3. 通过聊天界面提问
    
    新功能：智能体现在不仅能提供分析建议，还能自动执行代码并展示结果！
    """)

# 主界面
if file_processor.is_data_loaded():
    # 获取数据处理器
    data_processor = file_processor.get_data_processor()
    
    # 创建选项卡
    tab1, tab2 = st.tabs(["数据分析", "数据可视化"])
    
    # 数据分析选项卡
    with tab1:
        # 显示数据预览和信息
        col1, col2 = st.columns([2, 1])
        
        with col1:
            file_processor.display_data_preview()
        
        with col2:
            file_processor.display_data_info()
        
        # 显示描述性统计信息
        file_processor.display_descriptive_stats()
        
        st.divider()
        
        # 创建聊天界面
        st.subheader("与数据分析智能体对话")
        
        if not st.session_state.openai_api_key:
            st.warning("请在侧边栏输入OpenAI API密钥以启用智能分析功能。")
        else:
            # 初始化OpenAI工具
            openai_utils = OpenAIUtils(st.session_state.openai_api_key)
            
            # 初始化聊天界面
            chat_interface = ChatInterface()
            
            # 显示聊天历史
            chat_interface.display_chat_history()
            
            # 获取用户输入
            user_input = chat_interface.get_user_input()
            
            # 处理用户输入
            if user_input:
                # 获取数据信息
                data_info = data_processor.get_data_info()
                stats_summary = data_processor.get_descriptive_stats().to_dict()
                
                # 判断是否是预测分析问题
                if "预测" in user_input or "趋势" in user_input or "forecast" in user_input.lower() or "predict" in user_input.lower():
                    # 预测分析
                    with st.spinner("正在进行预测分析..."):
                        response = openai_utils.predict_data(data_info, stats_summary, user_input, data_processor)
                else:
                    # 普通数据分析
                    with st.spinner("正在分析数据..."):
                        response = openai_utils.analyze_data(data_info, user_input, data_processor)
                
                # 显示助手响应
                chat_interface.display_assistant_response(response)
    
    # 数据可视化选项卡
    with tab2:
        # 创建可视化器
        visualizer = Visualizer(data_processor)
        
        # 显示可视化选项
        visualizer.display_visualization_options()
else:
    # 未加载数据时显示欢迎信息
    st.info("👈 请在侧边栏上传CSV或Excel文件以开始分析。")
    
    # 示例提示
    st.subheader("您可以提问的示例：")
    st.markdown("""
    - 这个数据集的主要特点是什么？
    - 帮我分析一下销售额与其他因素的关系
    - 哪些因素对目标变量影响最大？
    - 预测未来三个月的销售趋势
    - 帮我检测数据中的异常值并分析原因
    - 绘制销售数据的时间序列图并分析趋势
    - 计算各产品类别的销售占比并可视化
    """)
