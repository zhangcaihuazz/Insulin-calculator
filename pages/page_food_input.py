import sys
import os
import pandas as pd
import streamlit as st

# 将 modules 文件夹添加到 Python 的模块搜索路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '../modules'))

# 从food_input.py导入所需函数
from modules.food_input import load_food_data, save_food_data, delete_food_data, check_duplicate_food

# 设置页面配置
st.set_page_config(
    page_title="食物信息录入",
    page_icon="🍎",
    layout="centered"
)

# 初始化session_state存储输入状态（放在这里）
if "food_input" not in st.session_state:
    st.session_state.food_input = {
        "name": "",
        "carb_100g": None,
        "protein_100g": None,
        "fat_100g": None
    }

# 初始化分页状态
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

# 页面标题
st.header("食物信息录入系统")

st.subheader("录入新食物")
with st.form("food_input_form", clear_on_submit=True):  # 添加这个参数
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        name = st.text_input(
            "食物名称",
            placeholder="例如：苹果",
            value=st.session_state.food_input["name"]
        )
    with col2:
        carb_100g = st.number_input(
            "每100g碳水 (g)",
            min_value=0.00,
            step=0.1,
            format="%.2f",
            value=st.session_state.food_input["carb_100g"],  # 现在会是 None
            placeholder="输入数值"  # 添加占位符文本
        )
    with col3:
        protein_100g = st.number_input(
            "每100g蛋白质 (g)",
            min_value=0.00,
            step=0.1,
            format="%.2f",
            value=st.session_state.food_input["protein_100g"],  # 修正：应该是protein_100g而不是carb_100g
            placeholder="输入数值"  # 添加占位符文本
        )
    with col4:
        fat_100g = st.number_input(
            "每100g脂肪 (g)",
            min_value=0.00,
            step=0.1,
            format="%.2f",
            value=st.session_state.food_input["fat_100g"],  # 修正：应该是fat_100g而不是carb_100g
            placeholder="输入数值"  # 添加占位符文本
        )

    submit = st.form_submit_button("保存食物信息", use_container_width=True)

    if submit:
        if not name:
            st.error("请输入食物名称")
        elif carb_100g is None or protein_100g is None or fat_100g is None:
            st.error("请填写所有营养成分数值")
        else:
            try:
                existing_data = load_food_data()
                foods_list = existing_data.copy() if existing_data else []

                if check_duplicate_food(foods_list, name):
                    st.error(f"警告：食物 '{name}' 已存在，请使用不同名称或修改已有食物")
                else:
                    new_food = {
                        "name": name,
                        "carb_100g": float(carb_100g),
                        "protein_100g": float(protein_100g),
                        "fat_100g": float(fat_100g)
                    }
                    foods_list.append(new_food)
                    save_food_data(foods_list)

                    st.success(f"食物 '{name}' 信息保存成功！")

                    # 重置session_state中的输入状态
                    st.session_state.food_input = {
                        "name": "",
                        "carb_100g": None,
                        "protein_100g": None,
                        "fat_100g": None
                    }

                    st.rerun()
            except Exception as e:
                st.error(f"保存失败: {str(e)}")


# 主区域：已录入食物列表（整合搜索功能）
st.subheader("已录入食物列表")

try:
    # 加载所有食物数据
    foods = load_food_data()

    if foods:
        search_query = st.text_input(
            "搜索食物名称",
            placeholder="输入关键词搜索...",
            key="food_search",
            label_visibility="collapsed"
        )

        # 根据搜索词过滤数据（无搜索时显示全部）
        if search_query:
            filtered_foods = [
                food for food in foods
                if search_query.lower() in food["name"].lower()
            ]
        else:
            filtered_foods = foods  # 无搜索时显示全部

        # 分页设置
        items_per_page = 10
        total_items = len(filtered_foods)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

        # 确保当前页面在有效范围内
        if st.session_state.current_page > total_pages:
            st.session_state.current_page = 1

        # 分页控件
        if total_pages > 1:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("上一页",
                             disabled=st.session_state.current_page == 1,
                             use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
            with col2:
                # 使用动态key确保选择框状态正确同步
                selected_page = st.selectbox(
                    "选择页码",
                    options=list(range(1, total_pages + 1)),
                    index=st.session_state.current_page - 1,
                    key=f"page_select_{total_pages}_{st.session_state.current_page}",  # 动态key
                    label_visibility="collapsed"
                )

                # 如果用户选择了不同的页码，立即更新
            if selected_page != st.session_state.current_page:
                st.session_state.current_page = selected_page
                st.rerun()
            with col3:
                if st.button("下一页",
                             disabled=st.session_state.current_page == total_pages,
                             use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()

        # 计算当前页的数据范围
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        current_page_foods = filtered_foods[start_idx:end_idx]

        # 显示当前页的食物列表
        df = pd.DataFrame(current_page_foods)
        df.index = range(start_idx + 1, end_idx + 1)  # 序号从当前页开始计算
        df.index.name = "序号"

        st.dataframe(
            df,
            column_config={
                "name": "食物名称",
                "carb_100g": st.column_config.NumberColumn("每100g碳水化合物 (g)"),
                "protein_100g": st.column_config.NumberColumn("每100g蛋白质 (g)"),
                "fat_100g": st.column_config.NumberColumn("每100g脂肪 (g)")
            },
            use_container_width=True
        )

        # 显示分页信息和统计信息
        if total_pages > 1:
            st.caption(f"第 {st.session_state.current_page}/{total_pages} 页，显示第 {start_idx + 1}-{end_idx} 条记录")

        # 显示统计信息（区分搜索状态）
        if search_query:
            st.info(f"搜索到 {len(filtered_foods)} 种食物（共 {len(foods)} 种）")
        else:
            st.info(f"当前共录入 {len(foods)} 种食物")
    else:
        st.info("暂无食物数据，请在上方录入食物信息")
        # 无数据时也显示搜索框（但提示无数据）
        st.text_input(
            "搜索食物名称",
            placeholder="输入关键词搜索...",
            disabled=True,
            label_visibility="collapsed"
        )

except Exception as e:
    st.error(f"加载食物数据失败: {str(e)}")

# 初始化foods为None，确保全局可见
foods = None

try:
    # 加载所有食物数据
    foods = load_food_data()  # 覆盖初始值
    # ... 后续使用foods的代码
except Exception as e:
    st.error(f"加载食物数据失败: {str(e)}")

# 编辑功能：带快速搜索的食物编辑（搜索框与选择框并排）
if foods:
    st.subheader("编辑食物信息")

    # 使用列布局实现搜索框与选择框并排
    select_col, search_col = st.columns([3, 1])  # 左侧选择框占比更大，右侧搜索框占比小

    with search_col:
        # 带搜索图标的输入框
        edit_search = st.text_input(
            "搜索要修改的食物",  # 搜索图标
            placeholder="搜索要修改的食物...",
            label_visibility="collapsed"  # 隐藏标签，只显示图标和输入框
        )

    # 根据搜索词过滤可编辑的食物列表
    if edit_search:
        filtered_edit_foods = [
            food for food in foods
            if edit_search.lower() in food["name"].lower()
        ]
    else:
        filtered_edit_foods = foods  # 无搜索时显示全部

    # 显示过滤结果数量（放在选择框上方）
    if edit_search:
        st.caption(f"找到 {len(filtered_edit_foods)} 个匹配的食物")

    with select_col:
        # 只在有过滤结果时显示选择框
        if filtered_edit_foods:
            edit_food_name = st.selectbox(
                "选择要修改的食物",  # 标签文本保留但不显示
                options=[food["name"] for food in filtered_edit_foods],
                index=None,
                placeholder="选择需要修改的食物...",
                label_visibility="collapsed"  # 隐藏选择框标签
            )
        else:
            edit_food_name = None
            st.selectbox(
                "选择要修改的食物",  # 标签文本保留但不显示
                options=[],
                index=None,
                placeholder="无匹配食物...",
                disabled=True,
                label_visibility="collapsed"
            )

    if edit_food_name:
        # 找到选中的食物数据
        edit_food = next(food for food in foods if food["name"] == edit_food_name)
        edit_index = foods.index(edit_food)

        with st.form(f"edit_form_{edit_index}"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                # 禁止修改食物名称：设置disabled=True，并添加提示
                st.text_input(
                    "食物名称",  # 提示用户名称不可修改
                    value=edit_food["name"],
                    disabled=True  # 核心：禁用输入框，阻止修改
                )
                # 隐藏的输入框：用于在提交时传递原始名称（不显示给用户）
                updated_name = st.session_state["original_name"] = edit_food["name"]
            with col2:
                updated_carb = st.number_input(
                    "每100g碳水 (g)",
                    min_value=0.00,
                    step=0.1,
                    format="%.2f",
                    value=edit_food["carb_100g"]
                )
            with col3:
                updated_protein = st.number_input(
                    "每100g蛋白质 (g)",
                    min_value=0.00,
                    step=0.1,
                    format="%.2f",
                    value=edit_food["protein_100g"]
                )
            with col4:
                updated_fat = st.number_input(
                    "每100g脂肪 (g)",
                    min_value=0.00,
                    step=0.1,
                    format="%.2f",
                    value=edit_food["fat_100g"]
                )

            col_submit, col_delete = st.columns(2)
            with col_submit:
                submit_edit = st.form_submit_button("保存修改", use_container_width=True)
            with col_delete:
                delete_btn = st.form_submit_button("删除", use_container_width=True, type="secondary",
                                                   help="删除此食物")

            if submit_edit:
                if not updated_name:
                    st.error("食物名称不能为空")
                else:
                    try:
                        # 更新食物数据
                        foods[edit_index] = {
                            "name": updated_name,
                            "carb_100g": float(updated_carb),
                            "protein_100g": float(updated_protein),
                            "fat_100g": float(updated_fat)
                        }
                        save_food_data(foods)
                        st.success(f"食物 '{updated_name}' 信息更新成功！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"更新失败: {str(e)}")

            if delete_btn:
                # 显示删除确认
                if st.checkbox(f"确认删除 '{edit_food_name}'？此操作不可恢复！", key="delete_confirm"):
                    try:
                        # 调用delete_food_data函数执行删除
                        delete_success = delete_food_data(foods, edit_index)
                        if delete_success:
                            st.success(f"食物 '{edit_food_name}' 已成功删除！")
                            st.rerun()
                        else:
                            st.error(f"删除失败：无效的食物索引")
                    except Exception as e:
                        st.error(f"删除失败: {str(e)}")

    elif edit_search and not filtered_edit_foods:
        # 无匹配结果时显示提示
        st.info(f"没有找到包含 '{edit_search}' 的食物，请尝试其他关键词")
