"""
胰岛素剂量计算模块
提供食物数据加载、ISF数据加载和胰岛素剂量计算功能
"""

from utils.file_utils import load_json
from modules.isf_calibration import load_rsi_data


def load_food_data():
    """
    加载食物数据从JSON文件

    返回:
        list: 包含食物信息的字典列表，如果文件不存在或读取失败则返回空列表
    """
    # 从foods_data.json文件加载食物数据
    data = load_json('foods_data.json')
    # 如果数据加载成功则返回数据，否则返回空列表
    return data if data is not None else []


def load_isf_data():
    """
    加载胰岛素敏感因子(ISF)数据从JSON文件

    返回:
        dict: 包含ISF值的字典，如果文件不存在则返回None
    """
    # 从isf_data.json文件加载ISF数据
    return load_json('isf_data.json')


def calculate_insulin_dose(food, weight, rsi_value, isf_value):
    """
    计算胰岛素注射剂量

    参数:
        food (dict): 食物信息字典，包含每100g碳水含量
        weight (float): 食物摄入重量(克)
        rsi_value (float): 碳水化合物敏感系数(RSI)
        isf_value (float): 胰岛素敏感因子(ISF)

    返回:
        tuple: 包含三个值的元组
            - total_carb (float): 总碳水含量(克)
            - estimated_blood_sugar_rise (float): 预计血糖升高值(mmol/L)
            - insulin_dose (float): 胰岛素注射剂量(单位)
    """
    # 获取食物每100g的碳水率
    carb_per_100g = food['carb_100g'] / 100
    # 计算实际摄入的总碳水含量 = 每100g碳水含量 × 摄入重量
    total_carb = carb_per_100g * weight

    # 计算预计血糖升高值 = 总碳水含量 × 碳水化合物敏感系数(RSI)
    estimated_blood_sugar_rise = total_carb * rsi_value

    # 计算胰岛素剂量 = 预计血糖升高值 / 胰岛素敏感因子(ISF)
    insulin_dose = estimated_blood_sugar_rise / isf_value

    return total_carb, estimated_blood_sugar_rise, insulin_dose


def calculate_insulin():
    """
    命令行界面的胰岛素计算主函数

    功能流程:
    1. 加载食物数据
    2. 用户输入食物名称和重量
    3. 加载RSI和ISF校准数据
    4. 计算胰岛素剂量
    5. 显示计算结果

    异常处理:
        - 处理食物数据加载失败情况
        - 处理食物未找到情况
        - 处理用户输入无效数字情况
        - 处理校准数据缺失情况
    """
    print("\n=== 计算胰岛素注射剂量 ===")

    # 加载食物数据
    foods_data = load_food_data()

    # 检查食物数据是否加载成功
    if not foods_data:
        print("没有找到食物数据，请先录入食物信息")
        return

    # 获取用户输入的食物名称
    food_name = input("请输入食物名称: ").strip()

    # 在食物数据中搜索匹配的食物
    selected_food = None
    for food in foods_data:
        # 不区分大小写比较食物名称
        if food['name'].lower() == food_name.lower():
            selected_food = food
            break

    # 如果未找到指定食物，提示用户并退出
    if not selected_food:
        print(f"未找到食物: {food_name}")
        return

    try:
        # 获取用户输入的食物重量并转换为浮点数
        weight = float(input(f"请输入摄入{selected_food['name']}的重量(克): ").strip())
    except ValueError:
        # 处理输入非数字的情况
        print("请输入有效的数字")
        return

    # 加载RSI(碳水化合物敏感系数)校准数据
    rsi_data = load_rsi_data()
    if rsi_data is None:
        print("未找到RSI校准数据,请先进行RSI校准")
        return

    # 加载ISF(胰岛素敏感因子)校准数据
    isf_data = load_isf_data()
    if isf_data is None:
        print("未找到ISF校准数据,请先进行ISF校准")
        return

    # 从校准数据中提取RSI和ISF值
    rsi_value = rsi_data['rsi_value']
    isf_value = isf_data['isf_value']

    # 调用计算函数获取结果
    total_carb, blood_sugar_rise, insulin_dose = calculate_insulin_dose(
        selected_food, weight, rsi_value, isf_value
    )

    # 格式化输出计算结果
    print(f"\n计算结果:")
    print(f"{weight}g {selected_food['name']}的碳水含量: {total_carb:.2f}g")
    print(f"预计血糖升高值: {blood_sugar_rise:.2f} mmol/L")
    print(f"胰岛素注射剂量: {insulin_dose:.2f} U")
    print(f"(基于RSI值: {rsi_value})")