"""
聊天界面组件
提供Streamlit聊天界面功能
"""
import streamlit as st
from typing import List, Dict, Any, Callable, Optional

class ChatInterface:
    """聊天界面类，用于管理Streamlit聊天界面"""
    
    def __init__(self):
        """初始化聊天界面"""
        # 初始化会话状态
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
    
    def display_chat_history(self):
        """显示聊天历史"""
        # 显示聊天消息
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                # 如果有HTML内容，显示它
                if "html_content" in message and message["html_content"]:
                    st.components.v1.html(message["html_content"], height=None, scrolling=True)
    
    def add_message(self, role: str, content: str, html_content: Optional[str] = None):
        """
        添加消息到聊天历史
        
        Args:
            role: 消息角色，"user"或"assistant"
            content: 消息内容
            html_content: 可选的HTML内容（如代码执行结果）
        """
        # 添加消息到会话状态
        message = {"role": role, "content": content}
        if html_content:
            message["html_content"] = html_content
            
        st.session_state.messages.append(message)
        
        # 添加到聊天历史记录
        st.session_state.chat_history.append(message)
    
    def get_user_input(self) -> Optional[str]:
        """
        获取用户输入
        
        Returns:
            str: 用户输入的消息，如果没有输入则返回None
        """
        # 获取用户输入
        if prompt := st.chat_input("请输入您的问题..."):
            # 添加用户消息
            self.add_message("user", prompt)
            return prompt
        return None
    
    def clear_chat_history(self):
        """清除聊天历史"""
        st.session_state.messages = []
        st.session_state.chat_history = []
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        获取聊天历史
        
        Returns:
            List[Dict[str, str]]: 聊天历史列表
        """
        return st.session_state.chat_history
    
    def display_thinking(self):
        """显示思考中状态"""
        with st.chat_message("assistant"):
            st.write("思考中...")
    
    def display_assistant_response(self, response: Dict[str, Any]):
        """
        显示助手响应
        
        Args:
            response: 响应字典，包含文本和可选的HTML内容
        """
        text = response.get("text", "")
        html_content = response.get("html_content", None)
        
        with st.chat_message("assistant"):
            st.markdown(text)
            if html_content:
                st.components.v1.html(html_content, height=None, scrolling=True)
        
        # 添加到历史记录
        self.add_message("assistant", text, html_content)
