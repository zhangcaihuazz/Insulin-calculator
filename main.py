# 导入操作系统接口模块，用于文件路径操作
import os
# 导入系统相关参数和函数模块，用于修改Python运行环境
import sys

# 添加模块路径到系统路径中，以便能够导入自定义模块
# 将当前文件所在目录下的'modules'文件夹路径添加到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
# 将当前文件所在目录下的'utils'文件夹路径添加到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# 从modules模块导入各个功能函数
# 从rsi_calibration模块导入calibrate_rsi函数，用于RSI值校准
from modules.rsi_calibration import calibrate_rsi
# 从isf_calibration模块导入calibrate_isf函数，用于ISF值校准
from modules.isf_calibration import calibrate_isf
# 从food_input模块导入input_food_data函数，用于食物信息录入
from modules.food_input import input_food_data
# 从insulin_calculation模块导入calculate_insulin函数，用于胰岛素剂量计算
from modules.insulin_calculation import calculate_insulin


def main():
    """
    主函数，程序入口点
    提供命令行菜单界面，用户可以选择不同的血糖控制功能
    """
    # 创建无限循环，直到用户选择退出
    while True:
        # 打印菜单标题和分隔线
        print("\n" + "=" * 50)  # 打印50个等号作为分隔线
        print("血糖控制程序主菜单")  # 打印程序标题
        print("=" * 50)  # 打印分隔线
        # 打印菜单选项
        print("1. 校准RSI值（升糖系数）")  # 选项1：RSI校准功能
        print("2. 校准ISF值（胰岛素敏感系数）")  # 选项2：ISF校准功能
        print("3. 录入食物信息")  # 选项3：食物信息录入功能
        print("4. 计算胰岛素注射剂量")  # 选项4：胰岛素剂量计算功能
        print("5. 退出程序")  # 选项5：退出程序
        print("=" * 50)  # 打印分隔线

        # 获取用户输入的选择，strip()用于去除首尾空白字符
        choice = input("请选择功能 (1-5): ").strip()

        # 根据用户选择执行相应的功能
        if choice == '1':
            # 如果选择1，调用RSI校准函数
            calibrate_rsi()
        elif choice == '2':
            # 如果选择2，调用ISF校准函数
            calibrate_isf()
        elif choice == '3':
            # 如果选择3，调用食物信息录入函数
            input_food_data()
        elif choice == '4':
            # 如果选择4，调用胰岛素剂量计算函数
            calculate_insulin()
        elif choice == '5':
            # 如果选择5，打印退出信息并跳出循环
            print("感谢使用血糖控制程序，再见！")
            break  # 跳出while循环，结束程序
        else:
            # 如果输入无效（不是1-5），提示用户重新输入
            print("无效选择，请输入1-5之间的数字")

        # 在每个功能执行完毕后暂停，等待用户按回车键继续
        # 这样可以让用户有时间查看上一个操作的输出结果
        input("\n按回车键继续...")


# Python程序的标准入口点检查
# 当该文件被直接运行时，__name__的值为"__main__"
# 当该文件被导入为模块时，__name__的值为模块名
if __name__ == "__main__":
    # 如果该文件是直接运行的（不是被导入的），则执行main()函数
    main()