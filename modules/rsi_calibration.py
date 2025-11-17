import datetime
from utils.file_utils import save_json


def calculate_rsi(weight, carb_rate, blood_sugar):
    """
    计算升糖指数(RSI)值

    参数:
        weight (float): 食物重量，单位：克(g)
        carb_rate (float): 碳水化合物的含量比率，单位：每100克中的百分比(%)
        blood_sugar (float): 血糖升高值，单位：毫摩尔/升(mmol/L)

    返回:
        tuple: 包含两个元素的元组
            - rsi (float): 计算得到的RSI值，保留2位小数
            - carb_content (float): 计算得到的碳水化合物总含量

    计算公式:
        carb_content = weight * (carb_rate / 100)  # 将百分比转换为实际碳水化合物含量
        rsi = blood_sugar / carb_content  # RSI = 血糖升高值 / 碳水化合物含量
    """
    # 计算碳水化合物总含量：重量 × ( 碳水量 / 100 )
    carb_content = weight * (carb_rate / 100)

    # 计算RSI值：血糖升高值 / 碳水化合物含量
    rsi = blood_sugar / carb_content

    # 返回保留2位小数的RSI值和碳水化合物含量
    return round(rsi, 2), carb_content


def save_rsi_data(rsi, weight, carb_rate, blood_sugar, carb_content):
    """
    将RSI计算数据保存为JSON格式文件

    参数:
        rsi (float): 计算得到的RSI值
        weight (float): 食物重量，单位：克(g)
        carb_rate (float): 碳水化合物的含量比率
        blood_sugar (float): 血糖升高值
        carb_content (float): 碳水化合物总含量

    返回:
        object: save_json函数的返回值，通常是保存操作的结果

    数据结构说明:
        rsi_data字典包含以下字段：
        - rsi_value: RSI数值
        - calculation_info: 计算相关的详细信息
            - weight_g: 食物重量(克)
            - carb_rate_per_100g: 每100克碳水比率(%)
            - carb_content_g: 碳水化合物总含量(克)，保留2位小数
            - blood_sugar_rise_mmol: 血糖升高值(mmol)
        - timestamp: 数据保存的时间戳，格式：年-月-日 时:分:秒
        - note: 数据说明备注
    """
    # 构建RSI数据字典
    rsi_data = {
        'rsi_value': rsi,  # RSI数值
        'calculation_info': {  # 计算相关信息
            'weight_g': weight,  # 食物重量
            'carb_rate_per_100g': carb_rate,  # 碳水比率
            'carb_content_g': round(carb_content, 2),  # 碳水化合物含量，保留2位小数
            'blood_sugar_rise_mmol': blood_sugar  # 血糖升高值
        },
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 当前时间戳
        'note': 'RSI (升糖指数) 计算数据'  # 数据说明
    }

    # 调用文件工具函数保存数据到JSON文件
    return save_json(rsi_data, 'rsi_data.json')


def calibrate_rsi():
    """
    通过命令行界面进行RSI校准的交互函数

    功能流程:
        1. 显示校准标题
        2. 通过命令行输入获取校准参数：
           - 食物重量
           - 碳水比率
           - 血糖升高值
        3. 调用calculate_rsi函数计算RSI值
        4. 显示校准结果
        5. 调用save_rsi_data函数保存校准数据

    用户交互:
        - 提示用户输入各项参数
        - 显示计算得到的RSI值

    注意:
        此函数设计为在命令行环境中运行，依赖于用户的标准输入
    """
    # 显示校准界面标题
    print("\n=== 校准升糖系数(RSI) ===")

    # 获取用户输入的校准参数
    calibrate_weight = float(input('请输入校准升糖系数食品的重量(单位:g):'))  # 食物重量
    calibrate_carbrate = float(input('请输入食品中碳水量(每100g):'))  # 碳水比率
    calibrate_bloodsugar = float(input('请输入摄入食物后升糖值(单位:mmol):'))  # 血糖升高值

    # 计算RSI值和碳水化合物含量(通过calculate_rsi函数元祖解包)
    rsi, carb_content = calculate_rsi(calibrate_weight, calibrate_carbrate, calibrate_bloodsugar)

    # 显示校准结果
    print('您的RSI值已校准为:' + str(rsi))

    # 保存RSI校准数据到文件
    save_rsi_data(rsi, calibrate_weight, calibrate_carbrate, calibrate_bloodsugar, carb_content)