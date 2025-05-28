"""
代码执行工具模块
提供安全解析和执行Python代码的功能
"""
import re
import ast
import sys
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Union, Optional, Any
import traceback
import base64
from contextlib import redirect_stdout, redirect_stderr


class CodeExecutor:
    """代码执行器类，用于安全解析和执行Python代码"""

    def __init__(self, data_processor=None):
        """
        初始化代码执行器

        Args:
            data_processor: 数据处理器实例，用于提供数据访问
        """
        self.data_processor = data_processor
        self.allowed_modules = {
            'pandas', 'numpy', 'matplotlib', 'plotly',
            'math', 'statistics', 'datetime', 'collections',
            'sklearn', 'scipy'
        }
        self.forbidden_keywords = {
            'exec', 'eval', 'compile', '__import__', 'open',
            'file', 'os.', 'sys.', 'subprocess', 'import os',
            'import sys', 'import subprocess', 'shutil'
        }

    def extract_code_blocks(self, text: str) -> List[str]:
        """
        从文本中提取Python代码块

        Args:
            text: 包含代码块的文本

        Returns:
            List[str]: 提取的代码块列表
        """
        # 匹配```python 和 ``` 之间的代码块
        pattern = r'```python\s*(.*?)\s*```'
        code_blocks = re.findall(pattern, text, re.DOTALL)

        # 如果没有明确的python标记，尝试匹配任何代码块
        if not code_blocks:
            pattern = r'```\s*(.*?)\s*```'
            code_blocks = re.findall(pattern, text, re.DOTALL)

        return code_blocks

    def is_code_safe(self, code: str) -> bool:
        """
        检查代码是否安全

        Args:
            code: 要检查的代码

        Returns:
            bool: 代码是否安全
        """
        # 检查是否包含禁止的关键字
        for keyword in self.forbidden_keywords:
            if keyword in code:
                return False

        # 解析AST，检查导入和函数调用
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                # 检查导入语句
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for name in node.names:
                        module_name = name.name.split('.')[0]
                        if module_name not in self.allowed_modules:
                            return False

                # 检查函数调用
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['exec', 'eval', 'compile', '__import__']:
                            return False
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id in ['os', 'sys', 'subprocess', 'shutil']:
                                return False

            return True
        except SyntaxError:
            return False

    def prepare_execution_environment(self) -> Dict:
        """
        准备执行环境

        Returns:
            Dict: 执行环境变量字典
        """
        # 准备基本环境
        env = {
            'pd': pd,
            'np': np,
            'plt': plt,
            'px': px,
            'go': go,
        }

        # 设置matplotlib字体支持中文
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 如果有数据处理器，添加数据
        if self.data_processor is not None and hasattr(self.data_processor, 'data'):
            env['df'] = self.data_processor.data

        return env

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        执行代码并返回结果

        Args:
            code: 要执行的代码

        Returns:
            Dict: 包含执行结果的字典
        """
        if not self.is_code_safe(code):
            return {
                'success': False,
                'error': '代码包含不安全的操作，已被阻止执行。',
                'output': None,
                'figures': []
            }

        # 准备执行环境
        env = self.prepare_execution_environment()

        # 捕获标准输出和错误
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        # 存储生成的图表
        figures = []

        try:
            # 修改matplotlib后端，捕获图表
            plt.switch_backend('Agg')

            # 执行代码
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                # 添加图表捕获
                original_show = plt.show

                def custom_show():
                    fig = plt.gcf()
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png')
                    buf.seek(0)
                    img_str = base64.b64encode(buf.read()).decode('utf-8')
                    figures.append(f"data:image/png;base64,{img_str}")
                    plt.close(fig)

                plt.show = custom_show

                # 执行代码
                exec(code, env)

                # 恢复原始show函数
                plt.show = original_show

            # 获取输出
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

            # 检查是否有错误
            if stderr:
                return {
                    'success': False,
                    'error': stderr,
                    'output': stdout,
                    'figures': figures
                }

            # 检查是否有返回值或生成的变量
            results = {}
            for key, value in env.items():
                # 排除内置模块和函数
                if key not in ['pd', 'np', 'plt', 'px', 'go', 'df'] and not key.startswith('__'):
                    # 对于DataFrame和Series，转换为HTML
                    if isinstance(value, (pd.DataFrame, pd.Series)):
                        results[key] = value.to_html()
                    # 对于numpy数组，转换为列表
                    elif isinstance(value, np.ndarray):
                        results[key] = value.tolist()
                    # 对于其他可序列化的对象
                    elif isinstance(value, (int, float, str, bool, list, dict, tuple)):
                        results[key] = value

            return {
                'success': True,
                'output': stdout,
                'results': results,
                'figures': figures
            }

        except Exception as e:
            # 捕获执行过程中的异常
            error_msg = traceback.format_exc()
            return {
                'success': False,
                'error': error_msg,
                'output': stdout_buffer.getvalue(),
                'figures': figures
            }

    def process_response(self, response: str) -> Dict[str, Any]:
        """
        处理LLM响应，提取并执行代码块

        Args:
            response: LLM响应文本

        Returns:
            Dict: 处理结果
        """
        # 提取代码块
        code_blocks = self.extract_code_blocks(response)

        if not code_blocks:
            return {
                'original_response': response,
                'has_code': False,
                'execution_results': []
            }

        # 执行每个代码块
        execution_results = []
        for code in code_blocks:
            result = self.execute_code(code)
            result['code'] = code
            execution_results.append(result)

        return {
            'original_response': response,
            'has_code': True,
            'execution_results': execution_results
        }

    def format_results_as_html(self, processed_response: Dict[str, Any]) -> str:
        """
        将处理结果格式化为HTML，确保中文显示正常

        Args:
            processed_response: 处理结果字典

        Returns:
            str: HTML格式的结果
        """
        if not processed_response['has_code']:
            return ""

        html_parts = []
        html_parts.append("<div style='margin-top: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>")
        html_parts.append("<h3>代码执行结果</h3>")

        for i, result in enumerate(processed_response['execution_results']):
            html_parts.append(
                f"<div style='margin-top: 10px; padding: 10px; background-color: #f9f9f9; border-radius: 5px;'>")
            html_parts.append(f"<h4>代码块 {i + 1}</h4>")

            # 添加代码
            html_parts.append(
                "<pre style='background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto;'>")
            html_parts.append(f"<code>{result['code']}</code>")
            html_parts.append("</pre>")

            # 添加执行状态
            if result['success']:
                html_parts.append("<p style='color: green;'>✓ 执行成功</p>")
            # else:
            #     html_parts.append("<p style='color: red;'>✗ 执行失败</p>")
            # html_parts.append(f"<pre style='color: red; background-color: #fff0f0; padding: 10px; border-radius: 5px; overflow-x: auto;'>{result['error']}</pre>")

            # 添加输出
            if result.get('output'):
                html_parts.append("<h5>输出:</h5>")
                html_parts.append(
                    f"<pre style='background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto;'>{result['output']}</pre>")

            # 添加结果变量
            if result.get('results'):
                html_parts.append("<h5>结果变量:</h5>")
                for var_name, var_value in result['results'].items():
                    if isinstance(var_value, str) and var_value.startswith('<table'):
                        html_parts.append(f"<p><strong>{var_name}:</strong></p>")
                        html_parts.append(var_value)
                    else:
                        html_parts.append(f"<p><strong>{var_name}:</strong> {var_value}</p>")

            # 添加图表
            if result.get('figures'):
                html_parts.append("<h5>生成的图表:</h5>")
                for fig_data in result['figures']:
                    html_parts.append(f"<img src='{fig_data}' style='max-width: 100%; margin: 10px 0;'>")

            html_parts.append("</div>")

        html_parts.append("</div>")

        return "".join(html_parts)
