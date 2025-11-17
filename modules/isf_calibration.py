import datetime
from utils.file_utils import load_json, save_json


def load_rsi_data():
    """加载RSI数据"""
    # 从'rsi_data.json'文件中加载并返回RSI（相对强度指标）数据
    # RSI数据可能包含之前计算得到的rsi_value值
    return load_json('rsi_data.json')


def calculate_isf(carb_total, insulin_total, rsi_value):
    """
    计算ISF（胰岛素敏感系数）值

    参数:
        carb_total: 总碳水化合物摄入量（单位：克）
        insulin_total: 总胰岛素用量（单位：单位U）
        rsi_value: RSI值（相对强度指标值）

    返回:
        tuple: (计算得到的ISF值, 估算的总血糖升高值)
    """
    # 根据公式：总碳水化合物 × RSI值 = 估算的总血糖升高值
    blood_sugar_total = carb_total * rsi_value

    # ISF计算公式：估算的总血糖升高值 ÷ 总胰岛素用量
    # 表示每单位胰岛素能降低多少mmol/L的血糖
    isf_value = blood_sugar_total / insulin_total

    # 返回四舍五入到小数点后2位的ISF值和估算的总血糖升高值
    return round(isf_value, 2), blood_sugar_total


def save_isf_data(isf_value, carb_total, insulin_total, blood_sugar_total):
    """
    保存ISF数据到JSON文件

    参数:
        isf_value: 计算得到的胰岛素敏感系数
        carb_total: 总碳水化合物摄入量
        insulin_total: 总胰岛素用量
        blood_sugar_total: 估算的总血糖升高值

    返回:
        save_json函数的返回值，通常是保存操作的结果状态
    """
    # 构建包含ISF计算数据的字典
    isf_data = {
        'isf_value': isf_value,  # ISF计算结果值
        'calculation_info': {  # 计算过程中的相关信息
            'carb_total_g': carb_total,  # 碳水化合物总量（克）
            'insulin_total_U': insulin_total,  # 胰岛素总量（单位）
            'estimated_blood_sugar_rise_mmol': round(blood_sugar_total, 2)  # 估算血糖升高值（mmol/L）
        },
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 当前时间戳
        'note': '胰岛素敏感系数 (ISF) 计算数据'  # 数据说明备注
    }

    # 将ISF数据保存到'isf_data.json'文件
    return save_json(isf_data, 'isf_data.json')


def calibrate_isf():
    """
    命令行界面的ISF校准功能

    通过用户输入的碳水化合物总量和胰岛素总量，结合RSI值计算ISF
    并显示计算结果，最后保存计算数据
    """
    print("\n=== 校准胰岛素敏感系数(ISF) ===")

    # 获取用户输入的碳水化合物总量（单位：克）
    calibrate_carbtotal = float(input('请输入一日碳水总量(单位:g):'))

    # 获取用户输入的胰岛素总量（单位：单位U）
    calibrate_isulintotal = float(input('请输入一日胰岛素总量(单位:U):'))

    # 加载RSI数据
    rsi_data = load_rsi_data()

    # 检查RSI数据是否存在
    if rsi_data is None:
        print("未找到RSI校准数据,请先进行RSI校准")
        return  # 如果RSI数据不存在，终止函数执行

    # 从RSI数据中提取rsi_value
    rsi_value = rsi_data['rsi_value']

    # 计算ISF值和估算的总血糖升高值
    isf_value, blood_sugar_total = calculate_isf(calibrate_carbtotal, calibrate_isulintotal, rsi_value)

    # 显示计算结果
    print(f"\n计算结果:")
    print(f"一日碳水总量: {calibrate_carbtotal}g")
    print(f"一日胰岛素总量: {calibrate_isulintotal}U")
    print(f"基于RSI值 {rsi_value}，预计总血糖值: {blood_sugar_total:.2f} mmol/L")
    print(f"胰岛素敏感系数(ISF): {isf_value:.2f} mmol/L/U")

    # 保存ISF计算数据到文件
    save_isf_data(isf_value, calibrate_carbtotal, calibrate_isulintotal, blood_sugar_total)