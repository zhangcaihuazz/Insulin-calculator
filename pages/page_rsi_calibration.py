import sys
import os
import streamlit as st  # 导入 Streamlit 库，用于构建 Web 应用
from datetime import datetime  # 导入 datetime 库，用于处理时间戳

# 将 modules 文件夹添加到 Python 的模块搜索路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# 导入 rsi_calibration 模块中的函数
from modules.rsi_calibration import calculate_rsi, save_rsi_data  # 从你保存的模块中导入 calculate_rsi 和 save_rsi_data 函数

# 设置页面配置
st.set_page_config(
    page_title="基础信息录入",
    page_icon="RSI",
    layout="centered"

# 设置页面标题
st.header('RSI (升糖指数) 校准')  # 显示应用页面的标题

# 页面描述，解释页面的功能
st.write("""
    通过此页面，您可以输入食品的重量、碳水化合物含量比率和血糖升高值，
    计算并保存您的 RSI (升糖指数) 校准数据。
""")

# 输入框，获取用户的食物重量
weight = st.number_input('请输入食物的重量 (单位：克)', min_value=0.0, step=0.1)
# 使用 number_input 创建一个数值输入框，最小值为 0.0，步长为 0.1，允许用户输入食物的重量。

# 输入框，获取食品中碳水化合物的比率
carb_rate = st.number_input('请输入食品中碳水重量 (每100克的重量)', min_value=0.0, max_value=100.0, step=0.1)
# 使用 number_input 创建一个数值输入框，用户输入食品的碳水化合物比率，最小值为 0，最大值为 100，步长为 0.1。

# 输入框，获取血糖升高值
blood_sugar = st.number_input('请输入摄入食物后血糖升高值 (单位：mmol/L)', min_value=0.0, step=0.1)
# 使用 number_input 创建一个数值输入框，用户输入食物摄入后血糖升高的值，最小值为 0.0，步长为 0.1。

# 添加一个按钮，当用户点击时触发 RSI 计算和数据保存
if st.button('计算 RSI 并保存'):
    # 判断输入值是否合法，确保食物重量、碳水化合物比率和血糖升高值大于 0
    if weight > 0 and carb_rate > 0 and blood_sugar >= 0:
        # 调用 calculate_rsi 函数计算 RSI 和碳水化合物总含量
        rsi, carb_content = calculate_rsi(weight, carb_rate, blood_sugar)

        # 显示计算结果的标题
        st.subheader(f'计算结果:')

        # 显示计算得到的 RSI 值和碳水化合物总含量
        st.write(f'您的RSI值为: {rsi}')
        st.write(f'食品的碳水化合物总含量为: {carb_content} 克')

        # 调用 save_rsi_data 函数将计算数据保存为 JSON 文件
        result = save_rsi_data(rsi, weight, carb_rate, blood_sugar, carb_content)

        # 判断保存结果，如果保存成功，显示成功消息
        if result:
            st.success('RSI数据已成功保存!')  # 使用 success() 显示成功消息
        else:
            st.error('保存数据时出现问题，请重试!')  # 使用 error() 显示错误消息
    else:
        # 如果用户输入无效数据，显示警告消息
        st.warning('请确保所有输入值有效！')
