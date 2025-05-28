# 数据分析智能体使用说明

## 项目概述

数据分析智能体是一个结合Streamlit、LangChain和OpenAI API的应用程序，可以帮助用户分析CSV和Excel数据文件，提供数据洞察和预测分析。应用通过聊天界面与用户交互，支持自然语言提问和分析请求。

## 功能特点

- **文件支持**：支持上传CSV和Excel文件
- **数据分析**：提供基本统计分析、相关性分析、异常检测等功能
- **预测分析**：支持趋势预测和预测分析
- **可视化**：提供多种图表类型，包括柱状图、折线图、散点图、直方图、箱线图、饼图等
- **聊天界面**：通过自然语言与智能体交互
- **OpenAI集成**：利用OpenAI API提供智能分析能力

## 使用方法

1. 访问应用链接：[数据分析智能体](https://8501-iqw6ge170176ln0bd7byt-518dece1.manusvm.computer)
2. 在侧边栏上传CSV或Excel文件
3. 输入OpenAI API密钥（需要您自己的API密钥）
4. 通过聊天界面提问或请求分析

## 示例问题

您可以向智能体提问如下类型的问题：

- 这个数据集的主要特点是什么？
- 帮我分析一下销售额与其他因素的关系
- 哪些因素对目标变量影响最大？
- 预测未来三个月的销售趋势
- 帮我检测数据中的异常值并分析原因

## 项目结构

```
data_analysis_agent/
├── app.py                      # 主应用入口
├── requirements.txt            # 依赖包列表
├── architecture.md             # 架构设计文档
├── todo.md                     # 开发任务清单
├── components/                 # 组件目录
│   ├── chat_interface.py       # 聊天界面组件
│   ├── file_processor.py       # 文件处理组件
│   └── visualizer.py           # 可视化组件
├── utils/                      # 工具函数
│   ├── data_utils.py           # 数据处理工具
│   └── openai_utils.py         # OpenAI API工具
└── test_data/                  # 测试数据
    ├── generate_test_data.py   # 测试数据生成脚本
    ├── sales_data.csv          # 示例CSV数据
    └── sales_data.xlsx         # 示例Excel数据
```

## 本地运行

如果您想在本地运行此应用：

1. 克隆项目代码
2. 安装依赖：`pip install -r requirements.txt`
3. 运行应用：`streamlit run app.py`

## 注意事项

- 应用需要OpenAI API密钥才能使用智能分析功能
- 大型文件可能需要较长处理时间
- 当前版本支持中文界面和分析
