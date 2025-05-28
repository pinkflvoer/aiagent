"""
OpenAI API工具模块
提供与OpenAI API交互的功能
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from typing import Dict, List, Any, Optional
from utils.code_executor import CodeExecutor

class OpenAIUtils:
    """OpenAI API工具类，用于与OpenAI API交互"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化OpenAI工具类
        
        Args:
            api_key: OpenAI API密钥，如果为None则尝试从环境变量获取
        """
        self.api_key = api_key
        self.setup_llm()
        
    def setup_llm(self, model_name: str = "gpt-4o"):
        """
        设置LLM模型
        
        Args:
            model_name: 模型名称
        """
        try:
            # 使用流式输出回调
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            
            # 初始化ChatOpenAI
            self.llm = ChatOpenAI(
                base_url='https://twapi.openai-hk.com/v1',
                model_name=model_name,
                temperature=0,
                openai_api_key=self.api_key,
                streaming=True,
                callback_manager=callback_manager
            )
        except Exception as e:
            print(f"设置LLM时出错: {e}")
            self.llm = None
    
    def create_data_analysis_chain(self) -> LLMChain:
        """
        创建数据分析链
        
        Returns:
            LLMChain: 数据分析链
        """
        if self.llm is None:
            return None
            
        # 创建数据分析提示模板
        prompt = ChatPromptTemplate.from_template(
            """你是一个专业的数据分析师。请根据以下数据信息进行分析。
            
            数据信息:
            {data_info}
            
            用户问题:
            {question}
            
            请提供详细的分析结果，包括关键发现、趋势和洞察。如果需要进一步的数据或信息，请说明。
            
            重要：如果分析需要编写代码，请提供完整的Python代码，并使用```python和```包围代码块。
            代码应该使用pandas (pd)、numpy (np)、matplotlib (plt) 或 plotly (px, go) 等库。
            数据已经加载为DataFrame变量df，可以直接在代码中使用。
            请确保代码是完整的、可执行的，并包含必要的可视化。
            """
        )
        
        # 创建链
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def create_prediction_chain(self) -> LLMChain:
        """
        创建预测分析链
        
        Returns:
            LLMChain: 预测分析链
        """
        if self.llm is None:
            return None
            
        # 创建预测分析提示模板
        prompt = ChatPromptTemplate.from_template(
            """你是一个专业的数据科学家。请根据以下数据信息进行预测分析。
            
            数据信息:
            {data_info}
            
            统计摘要:
            {stats_summary}
            
            用户问题:
            {question}
            
            请提供详细的预测分析结果，包括可能的趋势、预测值和置信度。解释你的预测方法和依据。
            如果需要更多数据或特定模型，请说明。
            
            重要：请提供完整的Python代码来实现你的预测分析，并使用```python和```包围代码块。
            代码应该使用pandas (pd)、numpy (np)、matplotlib (plt)、plotly (px, go) 或 scikit-learn 等库。
            数据已经加载为DataFrame变量df，可以直接在代码中使用。
            请确保代码是完整的、可执行的，并包含必要的可视化和结果输出。
            """
        )
        
        # 创建链
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def analyze_data(self, data_info: Dict, question: str, data_processor=None) -> Dict:
        """
        分析数据
        
        Args:
            data_info: 数据信息
            question: 用户问题
            data_processor: 数据处理器实例
            
        Returns:
            Dict: 包含分析结果和代码执行结果的字典
        """
        if self.llm is None:
            return {"text": "无法连接到OpenAI API，请检查API密钥是否正确。", "html_content": None}
            
        try:
            # 创建数据分析链
            chain = self.create_data_analysis_chain()
            
            # 运行链
            result = chain.invoke({
                "data_info": str(data_info),
                "question": question
            })
            
            text_response = result["text"]
            
            # 创建代码执行器并处理响应
            code_executor = CodeExecutor(data_processor)
            processed_response = code_executor.process_response(text_response)
            
            # 格式化结果为HTML
            html_content = None
            if processed_response['has_code']:
                html_content = code_executor.format_results_as_html(processed_response)
            
            return {"text": text_response, "html_content": html_content}
        except Exception as e:
            return {"text": f"分析数据时出错: {e}", "html_content": None}
    
    def predict_data(self, data_info: Dict, stats_summary: Dict, question: str, data_processor=None) -> Dict:
        """
        预测分析
        
        Args:
            data_info: 数据信息
            stats_summary: 统计摘要
            question: 用户问题
            data_processor: 数据处理器实例
            
        Returns:
            Dict: 包含预测结果和代码执行结果的字典
        """
        if self.llm is None:
            return {"text": "无法连接到OpenAI API，请检查API密钥是否正确。", "html_content": None}
            
        try:
            # 创建预测分析链
            chain = self.create_prediction_chain()
            
            # 运行链
            result = chain.invoke({
                "data_info": str(data_info),
                "stats_summary": str(stats_summary),
                "question": question
            })
            
            text_response = result["text"]
            
            # 创建代码执行器并处理响应
            code_executor = CodeExecutor(data_processor)
            processed_response = code_executor.process_response(text_response)
            
            # 格式化结果为HTML
            html_content = None
            if processed_response['has_code']:
                html_content = code_executor.format_results_as_html(processed_response)
            
            return {"text": text_response, "html_content": html_content}
        except Exception as e:
            return {"text": f"预测分析时出错: {e}", "html_content": None}
