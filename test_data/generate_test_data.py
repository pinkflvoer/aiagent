import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 创建销售数据示例
np.random.seed(42)

# 创建日期范围
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# 创建基础销售数据
base_sales = 1000 + np.random.normal(0, 100, len(date_range))

# 添加季节性
season_effect = 300 * np.sin(np.arange(len(date_range)) * (2 * np.pi / 365))
sales = base_sales + season_effect

# 添加周末效应
is_weekend = [(d.weekday() >= 5) for d in date_range]
weekend_boost = np.array([150 if w else 0 for w in is_weekend])
sales = sales + weekend_boost

# 添加促销效应
promo_dates = [
    datetime(2023, 2, 14),  # 情人节
    datetime(2023, 5, 1),   # 劳动节
    datetime(2023, 6, 18),  # 父亲节
    datetime(2023, 11, 11), # 双十一
    datetime(2023, 12, 12)  # 双十二
]

# 促销效应持续3天
promo_effect = np.zeros(len(date_range))
for promo_date in promo_dates:
    for i in range(3):
        promo_day = (promo_date + timedelta(days=i)).strftime('%Y-%m-%d')
        if promo_day in date_range.strftime('%Y-%m-%d').values:
            idx = np.where(date_range.strftime('%Y-%m-%d') == promo_day)[0][0]
            promo_effect[idx] = 500 - i * 100  # 促销效果逐渐减弱

sales = sales + promo_effect

# 创建区域和产品类别
regions = ['北区', '南区', '东区', '西区']
categories = ['电子产品', '服装', '食品', '家居用品']

# 创建完整数据集
data = []
for i, date in enumerate(date_range):
    for region in regions:
        for category in categories:
            # 区域和类别的基础差异
            region_factor = {'北区': 1.2, '南区': 0.9, '东区': 1.0, '西区': 1.1}[region]
            category_factor = {'电子产品': 1.5, '服装': 1.2, '食品': 0.8, '家居用品': 1.0}[category]
            
            # 计算最终销售额
            sale_amount = sales[i] * region_factor * category_factor
            
            # 添加随机波动
            sale_amount = sale_amount * np.random.uniform(0.9, 1.1)
            
            # 计算成本和利润
            cost = sale_amount * np.random.uniform(0.5, 0.7)
            profit = sale_amount - cost
            
            # 添加客户数量
            customer_count = int(sale_amount / np.random.uniform(50, 150))
            
            # 添加到数据集
            data.append({
                '日期': date,
                '区域': region,
                '产品类别': category,
                '销售额': round(sale_amount, 2),
                '成本': round(cost, 2),
                '利润': round(profit, 2),
                '客户数': customer_count,
                '是否促销': 1 if promo_effect[i] > 0 else 0,
                '是否周末': 1 if is_weekend[i] else 0
            })

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为CSV和Excel文件
df.to_csv('/home/ubuntu/data_analysis_agent/test_data/sales_data.csv', index=False)
df.to_excel('/home/ubuntu/data_analysis_agent/test_data/sales_data.xlsx', index=False)
