import sys
import os
import pandas as pd
import streamlit as st
from modules.food_input import load_food_data
from modules.insulin_calculation import (
    load_rsi_data,
    load_isf_data,
    calculate_insulin_dose
)

# 确保模块路径正确
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

st.set_page_config(
    page_title="胰岛素计算",
    page_icon="💉",
    layout="wide"
)

# 初始化session_state
if 'selected_food' not in st.session_state:
    st.session_state.selected_food = "未选择食物"
if 'calculation_result' not in st.session_state:
    st.session_state.calculation_result = None
if 'page_initialized' not in st.session_state:
    st.session_state.page_initialized = True

st.header("胰岛素剂量计算")

# 主要计算数据展示 - 使用callback强制更新
def update_metrics():
    """更新顶部metric显示"""
    # 重命名局部变量以避免隐藏外部作用域名称
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    # 初始化默认值
    display_insulin_dose = "0 U"
    isf_display = "ISF --"
    display_blood_sugar_rise = "0 mmol"
    rsi_display = "RSI --"
    total_carbs = "0 g"
    weight_display = "WGT --"

    # 加载校准数据 - 使用更具体的异常处理
    try:
        local_rsi_data = load_rsi_data()
        local_isf_data = load_isf_data()

        if local_isf_data:
            isf_display = f"ISF {local_isf_data['isf_value']:.2f}"
        if local_rsi_data:
            rsi_display = f"RSI {local_rsi_data['rsi_value']:.2f}"
    except (FileNotFoundError, KeyError, ValueError, TypeError) as error:
        # 重命名异常变量以避免隐藏外部作用域
        st.sidebar.warning(f"加载校准数据时遇到问题: {str(error)}")

    # 如果有计算结果，使用计算结果
    if st.session_state.calculation_result:
        result = st.session_state.calculation_result
        display_insulin_dose = f"{result['insulin_dose']:.1f} U"
        display_blood_sugar_rise = f"{result['blood_sugar_rise']:.1f} mmol"
        total_carbs = f"{result['total_carb']:.1f} g"
        weight_display = f"WGT {result['weight']:.1f}"

    # 显示metric
    metric_col1.metric("建议胰岛素剂量", display_insulin_dose, isf_display)
    metric_col2.metric("预计升糖指数", display_blood_sugar_rise, rsi_display)
    metric_col3.metric("碳水化合物总量", total_carbs, weight_display)

# 调用函数显示metric
update_metrics()

# 顶部三个并排元素区域
# 顶部三个并排元素区域 - 使用表单来实现计算后重置
with st.form("insulin_calculation_form", clear_on_submit=True):
    top_col1, top_col2, top_col3 = st.columns([3, 3, 4])

    with top_col1:
        st.text_input(
            "当前选择食物",
            value=st.session_state.selected_food,
            disabled=True,
            label_visibility="collapsed"
        )

    with top_col2:
        food_weight = st.number_input(
            "摄入重量(克)",
            min_value=0,
            step=1,
            format="%d",
            value=None,  # 明确设置为 None
            label_visibility="collapsed",
            placeholder="食物重量(单位：g)"
        )

    with top_col3:
        calculate_btn = st.form_submit_button("计算胰岛素剂量", use_container_width=True)

# 加载所有食物数据
all_foods = load_food_data()

# 搜索区域 - 重命名局部变量
search_col1, search_col2 = st.columns([6, 4])
with search_col2:
    search_query = st.text_input(
        "搜索食物",
        placeholder="输入食物名称（例如：米饭）",
        label_visibility="visible",
        key="food_search"
    )

matched_foods = []
if search_query.strip():
    if not all_foods:
        st.warning("未找到食物数据，请先录入食物信息")
    else:
        matched_foods = [
            food for food in all_foods
            if search_query.lower() in food["name"].lower()
        ]

with search_col1:
    if matched_foods:
        food_options = [food["name"] for food in matched_foods]
        selected_idx = food_options.index(
            st.session_state.selected_food) if st.session_state.selected_food in food_options else 0
        selected_food = st.selectbox(
            "选择食物",
            options=food_options,
            index=selected_idx,
            label_visibility="visible"
        )
        st.session_state.selected_food = selected_food
    else:
        selected_food = st.selectbox(
            "选择食物",
            options=["请先搜索食物"],
            disabled=True,
            label_visibility="visible"
        )

if matched_foods:
    st.dataframe(
        pd.DataFrame(matched_foods),
        column_config={
            "name": "食物名称",
            "carb_100g": "每100g碳水(g)",
            "protein_100g": "每100g蛋白质(g)",
            "fat_100g": "每100g脂肪(g)"
        },
        hide_index=True,
        use_container_width=True
    )
    st.info(f"找到 {len(matched_foods)} 种匹配的食物")
elif search_query.strip():
    st.warning(f"未找到包含「{search_query}」的食物，请检查名称是否正确或录入食物信息。")

# 计算胰岛素剂量的核心逻辑
if calculate_btn:
    if st.session_state.selected_food in ["未选择食物", "请先搜索食物"]:
        st.error("请先选择食物")
    elif food_weight <= 0:
        st.error("请输入有效的食物重量")
    else:
        try:
            # 重命名局部变量
            calc_rsi_data = load_rsi_data()
            calc_isf_data = load_isf_data()

            if not calc_rsi_data:
                st.error("未找到RSI校准数据，请先进行RSI校准")
            elif not calc_isf_data:
                st.error("未找到ISF校准数据，请先进行ISF校准")
            else:
                selected_food_detail = next(
                    (food for food in all_foods if food["name"] == st.session_state.selected_food),
                    None
                )

                if not selected_food_detail:
                    st.error("未找到选中食物的详细信息")
                else:
                    # 重命名局部变量
                    calc_total_carb, calc_blood_sugar_rise, calc_insulin_dose = calculate_insulin_dose(
                        food=selected_food_detail,
                        weight=food_weight,
                        rsi_value=calc_rsi_data["rsi_value"],
                        isf_value=calc_isf_data["isf_value"]
                    )

                    # 保存计算结果到session_state
                    st.session_state.calculation_result = {
                        "food": st.session_state.selected_food,
                        "weight": food_weight,
                        "total_carb": calc_total_carb,
                        "blood_sugar_rise": calc_blood_sugar_rise,
                        "insulin_dose": calc_insulin_dose
                    }

                    st.success("计算完成！")
                    with st.expander("查看计算结果", expanded=True):
                        st.write(f"食物名称: {st.session_state.selected_food}")
                        st.write(f"摄入重量: {food_weight} 克")
                        st.write(f"总碳水化合物含量: {calc_total_carb:.2f} 克")
                        st.write(f"预计血糖升高: {calc_blood_sugar_rise:.2f} mmol/L")
                        st.write(f"推荐胰岛素剂量: {calc_insulin_dose:.2f} 单位")

                    # 强制重新运行整个脚本以更新顶部的metric
                    st.rerun()

        except (FileNotFoundError, KeyError, ValueError, TypeError) as calc_error:
            # 重命名异常变量
            st.error(f"计算过程出错: {str(calc_error)}")