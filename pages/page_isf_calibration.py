import sys
import os
import streamlit as st  # 导入 Streamlit 库，用于构建 Web 应用

# 将 modules 文件夹添加到 Python 的模块搜索路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# 导入 rsi_calibration 模块中的函数
from modules.isf_calibration import calculate_isf, save_isf_data, load_rsi_data

# 加载RSI数据并检查
rsi_data = load_rsi_data()
if not rsi_data:
    st.error("未找到RSI校准数据，请先进行RSI校准")
    st.stop()  # 终止后续代码执行，避免使用未定义的rsi_value
else:
    rsi_value = rsi_data['rsi_value']

# 设置页面标题
st.header('ISF胰岛素敏感系数校准')  # 显示应用页面的标题

# 页面描述，解释页面的功能
st.write("""
    通过此页面，您可以输入一日碳水化合物总量和一日胰岛素注射总量，
    计算并保存您的 ISF (胰岛素敏感系数) 校准数据。
""")

# 输入框，获取用户的一日碳水总量
carb_total = st.number_input('请输入一日碳水化合物总量(单位:g)', min_value=0.0, step=0.1)
# 使用 number_input 创建一个数值输入框，最小值为 0.0，步长为 0.1，允许用户输入食物的重量。

# 输入框，获取用户的一日胰岛素总量
insulin_total = st.number_input('请输入一日胰岛素总量(单位:U)', min_value=0.0, max_value=100.0, step=0.1)
# 使用 number_input 创建一个数值输入框，用户输入食品的碳水化合物比率，最小值为 0，最大值为 100，步长为 0.1。

# 添加一个按钮，当用户点击时触发 ISF 计算和数据保存
if st.button('计算 ISF 并保存'):  # 注意按钮文字这里应该是"计算ISF"而不是"计算RSI"，建议同步修改
    if carb_total > 0 and insulin_total > 0:  # 胰岛素总量建议大于0（避免除以0）
        # 接收calculate_isf的返回值
        isf_value, blood_sugar_total = calculate_isf(carb_total, insulin_total, rsi_value)

        st.subheader('计算结果:')
        st.write(f'您的ISF值为: {isf_value}')

        # 保存数据
        result = save_isf_data(isf_value, carb_total, insulin_total, blood_sugar_total)
        if result:
            st.success('ISF数据已成功保存!')  # 提示文字同步改为ISF
        else:
            st.error('保存数据时出现问题，请重试!')
    else:
        st.warning('请确保碳水总量和胰岛素总量均大于0！')
