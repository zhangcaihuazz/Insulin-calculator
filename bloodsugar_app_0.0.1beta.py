import streamlit as st  # 用于构建Web应用的Python框架
import streamlit.components.v1 as components
import sys  # 提供对Python解释器相关功能的访问
import os  # 提供与操作系统交互的功能

# 添加自定义模块路径到Python路径中
# 这样Python解释器能够找到我们自定义的模块文件
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))  # 添加modules文件夹路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))  # 添加utils文件夹路径

st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    """,
    unsafe_allow_html=True
)

# 设置Streamlit页面配置
st.set_page_config(
    page_title="血糖胰岛素控制程序",  # 浏览器标签页显示的标题
    page_icon="blood",  # 浏览器标签页显示的图标（血液emoji）
    layout="centered",  # 使用中心布局模式
)


def main():
    """
    主应用入口函数

    功能:
    - 显示应用标题
    - 调用状态显示函数展示当前系统状态
    """
    # 应用主标题
    st.header("水晶能量计算器 Beta 0.0.1")  # 显示带图标的标题

    # 显示当前系统状态
    show_current_status()


def show_current_status():
    """
    显示当前系统状态信息

    功能:
    - 从JSON文件加载RSI（胰岛素敏感系数）数据
    - 从JSON文件加载ISF（胰岛素敏感因子）数据
    - 从JSON文件加载食物数据库数据
    - 使用三列布局展示各项状态信息
    - 处理数据加载异常情况

    异常处理:
    - 捕获数据加载过程中的所有异常
    - 显示友好的错误信息给用户
    """

    try:
        # 从utils模块导入JSON文件加载功能
        from utils.file_utils import load_json

        # 创建子标题
        st.subheader("当前系统状态")

        # 创建三列布局，用于并排显示三个状态卡片
        col1, col2, col3 = st.columns(3)

        # 第一列：显示RSI（胰岛素敏感系数）状态
        with col1:
            # 从rsi_data.json文件加载RSI数据
            rsi_data = load_json('rsi_data.json')

            # 检查RSI数据是否成功加载
            if rsi_data:
                # 显示成功的状态信息和RSI值
                st.success(f"**RSI值**: {rsi_data['rsi_value']}")

                # 如果数据中包含时间戳，显示最后更新时间
                if 'timestamp' in rsi_data:
                    st.caption(f"最后更新: {rsi_data['timestamp']}")
            else:
                # 如果数据加载失败，显示错误状态
                st.error("**RSI值**: 未校准")
                st.caption("请先进行RSI校准")  # 提示用户需要执行校准操作

        # 第二列：显示ISF（胰岛素敏感因子）状态
        with col2:
            # 从isf_data.json文件加载ISF数据
            isf_data = load_json('isf_data.json')

            # 检查ISF数据是否成功加载
            if isf_data:
                # 显示成功的状态信息和ISF值（带单位）
                st.success(f"**ISF值**: {isf_data['isf_value']} mmol/L/U")

                # 如果数据中包含时间戳，显示最后更新时间
                if 'timestamp' in isf_data:
                    st.caption(f"最后更新: {isf_data['timestamp']}")
            else:
                # 如果数据加载失败，显示错误状态
                st.error("**ISF值**: 未校准")
                st.caption("请先进行ISF校准")  # 提示用户需要执行校准操作

        # 第三列：显示食物数据库状态
        with col3:
            # 从foods_data.json文件加载食物数据
            food_data = load_json('foods_data.json')

            # 检查食物数据是否成功加载
            if food_data:
                # 显示成功的状态信息和食物种类数量
                st.success(f"**食物数据**: {len(food_data)} 种")

                # 获取最近录入的3种食物
                recent_foods = food_data[-3:]
                # 格式化显示最近录入的食物列表
                food_list = "\n".join([f"• {food['name']}" for food in recent_foods])
                st.caption(f"最近录入:\n{food_list}")
            else:
                # 如果数据加载失败，显示警告状态
                st.warning("**食物数据**: 0 种")
                st.caption("请先录入食物信息")  # 提示用户需要录入食物信息

    except Exception as e:
        """
        异常处理块

        功能:
        - 捕获数据加载过程中可能出现的所有异常
        - 显示通用的错误信息
        - 提供详细的错误信息用于调试
        """
        # 显示通用错误信息
        st.error("数据加载错误")
        # 显示具体的错误信息（在生产环境中可能需要更友好的提示）
        st.info(f"错误详情: {str(e)}")


# Python程序的入口点
# 当直接运行此脚本时（而不是被导入为模块），执行main()函数
if __name__ == "__main__":
    main()
