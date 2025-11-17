# 导入必要的库和模块
import tkinter as tk  # 导入tkinter库，用于创建GUI界面
from tkinter import ttk, messagebox  # 导入ttk模块（主题控件）和messagebox模块（消息框）
from utils.file_utils import load_json  # 从自定义工具模块导入JSON文件加载函数
from modules.food_input import load_food_data, save_food_data  # 从食物输入模块导入数据加载和保存函数

# 导入重构后的计算函数
from modules.rsi_calibration import calculate_rsi, save_rsi_data  # 从RSI校准模块导入计算和保存函数
from modules.isf_calibration import calculate_isf, save_isf_data, load_rsi_data  # 从ISF校准模块导入相关函数
from modules.insulin_calculation import calculate_insulin_dose, load_isf_data  # 从胰岛素计算模块导入剂量计算和数据加载函数


class RsiCalibrationWindow:
    """RSI校准窗口类，用于计算和校准升糖系数"""

    def __init__(self, parent):
        """
        初始化RSI校准窗口

        参数:
            parent: 父窗口对象
        """
        # 创建顶级窗口
        self.window = tk.Toplevel(parent)
        self.window.title("RSI校准")  # 设置窗口标题
        self.window.geometry("450x350")  # 设置窗口大小
        self.window.transient(parent)  # 设置窗口为父窗口的临时窗口
        self.window.grab_set()  # 设置模态窗口，阻止与其他窗口交互

        # 调用界面设置方法
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面组件"""
        # 标题框架
        title_frame = ttk.Frame(self.window)  # 创建标题框架
        title_frame.pack(fill="x", pady=10)  # 填充X方向并设置垂直间距
        # 创建标题标签
        ttk.Label(title_frame, text="校准升糖系数(RSI)", font=("Arial", 14, "bold")).pack()

        # 输入框区域框架
        input_frame = ttk.LabelFrame(self.window, text="输入参数", padding=15)  # 创建带标签的框架
        input_frame.pack(fill="both", expand=True, padx=20, pady=10)  # 填充并扩展，设置内外边距

        # 食品重量输入组件
        ttk.Label(input_frame, text="食品重量(g):").grid(row=0, column=0, sticky="w", pady=8)  # 创建标签
        self.weight_entry = ttk.Entry(input_frame, width=15)  # 创建输入框
        self.weight_entry.grid(row=0, column=1, sticky="w", pady=8, padx=10)  # 网格布局

        # 碳水率输入组件
        ttk.Label(input_frame, text="碳水率(/100g):").grid(row=1, column=0, sticky="w", pady=8)
        self.carb_entry = ttk.Entry(input_frame, width=15)
        self.carb_entry.grid(row=1, column=1, sticky="w", pady=8, padx=10)

        # 升糖值输入组件
        ttk.Label(input_frame, text="升糖值(mmol/L):").grid(row=2, column=0, sticky="w", pady=8)
        self.bloodsugar_entry = ttk.Entry(input_frame, width=15)
        self.bloodsugar_entry.grid(row=2, column=1, sticky="w", pady=8, padx=10)

        # 按钮区域框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", pady=15)

        # 创建功能按钮
        ttk.Button(button_frame, text="计算并保存", command=self.calculate_rsi).pack(side="left", padx=10)
        ttk.Button(button_frame, text="清空", command=self.clear_entries).pack(side="left", padx=10)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side="left", padx=10)

        # 结果显示区域框架
        result_frame = ttk.LabelFrame(self.window, text="计算结果", padding=10)
        result_frame.pack(fill="x", padx=20, pady=10)

        # 创建结果显示标签
        self.result_label = ttk.Label(result_frame, text="请输入参数进行计算", font=("Arial", 12))
        self.result_label.pack()

    def clear_entries(self):
        """清空所有输入框和结果标签"""
        self.weight_entry.delete(0, tk.END)  # 清空重量输入框
        self.carb_entry.delete(0, tk.END)  # 清空碳水率输入框
        self.bloodsugar_entry.delete(0, tk.END)  # 清空升糖值输入框
        self.result_label.config(text="请输入参数进行计算")  # 重置结果标签文本

    def calculate_rsi(self):
        """计算RSI值并保存结果"""
        try:
            # 从输入框获取数据并转换为浮点数
            weight = float(self.weight_entry.get())
            carb_rate = float(self.carb_entry.get())
            blood_sugar = float(self.bloodsugar_entry.get())

            # 直接调用模块中的计算函数计算RSI和碳水含量
            rsi, carb_content = calculate_rsi(weight, carb_rate, blood_sugar)

            # 调用模块中的保存函数保存RSI数据
            if save_rsi_data(rsi, weight, carb_rate, blood_sugar, carb_content):
                # 保存成功，更新结果显示
                result_text = f"RSI值已校准为: {rsi}\n数据已保存成功!"
                self.result_label.config(text=result_text)
                messagebox.showinfo("成功", "RSI校准完成并已保存!")
            else:
                # 保存失败，显示错误信息
                messagebox.showerror("错误", "保存数据失败")

        except ValueError:
            # 输入格式错误处理
            messagebox.showerror("输入错误", "请输入有效的数字")
        except ZeroDivisionError:
            # 除零错误处理
            messagebox.showerror("计算错误", "碳水含量不能为零")


class IsfCalibrationWindow:
    """ISF校准窗口类，用于计算和校准胰岛素敏感系数"""

    def __init__(self, parent):
        """
        初始化ISF校准窗口

        参数:
            parent: 父窗口对象
        """
        self.window = tk.Toplevel(parent)
        self.window.title("ISF校准")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """设置用户界面组件"""
        # 标题框架
        title_frame = ttk.Frame(self.window)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="校准胰岛素敏感系数(ISF)", font=("Arial", 14, "bold")).pack()

        # 输入框区域框架
        input_frame = ttk.LabelFrame(self.window, text="输入参数", padding=15)
        input_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 一日碳水总量输入组件
        ttk.Label(input_frame, text="一日碳水总量(g):").grid(row=0, column=0, sticky="w", pady=8)
        self.carb_total_entry = ttk.Entry(input_frame, width=15)
        self.carb_total_entry.grid(row=0, column=1, sticky="w", pady=8, padx=10)

        # 一日胰岛素总量输入组件
        ttk.Label(input_frame, text="一日胰岛素总量(U):").grid(row=1, column=0, sticky="w", pady=8)
        self.insulin_total_entry = ttk.Entry(input_frame, width=15)
        self.insulin_total_entry.grid(row=1, column=1, sticky="w", pady=8, padx=10)

        # RSI值显示标签
        ttk.Label(input_frame, text="当前RSI值:").grid(row=2, column=0, sticky="w", pady=8)
        self.rsi_value_label = ttk.Label(input_frame, text="未加载")
        self.rsi_value_label.grid(row=2, column=1, sticky="w", pady=8, padx=10)

        # 加载RSI数据
        self.load_rsi_data()

        # 按钮区域框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", pady=15)

        # 创建功能按钮
        ttk.Button(button_frame, text="计算并保存", command=self.calculate_isf).pack(side="left", padx=10)
        ttk.Button(button_frame, text="清空", command=self.clear_entries).pack(side="left", padx=10)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side="left", padx=10)

        # 结果显示区域框架
        result_frame = ttk.LabelFrame(self.window, text="计算结果", padding=10)
        result_frame.pack(fill="x", padx=20, pady=10)

        # 创建文本结果显示组件（带滚动条）
        self.result_text = tk.Text(result_frame, height=6, width=50, font=("Arial", 12))
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)  # 关联滚动条
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 初始化结果显示文本
        self.result_text.insert("1.0", "请输入参数进行计算")
        self.result_text.config(state="disabled")  # 设置为只读模式

    def load_rsi_data(self):
        """加载并显示RSI数据"""
        rsi_data = load_rsi_data()  # 直接调用模块函数加载RSI数据
        if rsi_data:
            # 如果数据存在，显示RSI值
            rsi_value = rsi_data['rsi_value']
            self.rsi_value_label.config(text=f"{rsi_value}")
        else:
            # 如果数据不存在，显示提示信息
            self.rsi_value_label.config(text="未找到RSI数据")

    def clear_entries(self):
        """清空所有输入框和结果文本"""
        self.carb_total_entry.delete(0, tk.END)  # 清空碳水总量输入框
        self.insulin_total_entry.delete(0, tk.END)  # 清空胰岛素总量输入框
        self.result_text.config(state="normal")  # 设置为可编辑模式
        self.result_text.delete("1.0", tk.END)  # 清空结果文本
        self.result_text.insert("1.0", "请输入参数进行计算")  # 插入默认文本
        self.result_text.config(state="disabled")  # 重新设置为只读模式

    def calculate_isf(self):
        """计算ISF值并保存结果"""
        try:
            # 从输入框获取数据并转换为浮点数
            carb_total = float(self.carb_total_entry.get())
            insulin_total = float(self.insulin_total_entry.get())

            # 加载RSI数据
            rsi_data = load_rsi_data()  # 直接调用模块函数
            if not rsi_data:
                # 如果RSI数据不存在，显示错误信息
                messagebox.showerror("错误", "未找到RSI校准数据，请先进行RSI校准")
                return

            # 获取RSI值
            rsi_value = rsi_data['rsi_value']

            # 直接调用模块中的计算函数计算ISF值和总血糖升高值
            isf_value, blood_sugar_total = calculate_isf(carb_total, insulin_total, rsi_value)

            # 调用模块中的保存函数保存ISF数据
            if save_isf_data(isf_value, carb_total, insulin_total, blood_sugar_total):
                # 构建结果文本
                result_text = f"ISF校准完成!\n\n"
                result_text += f"一日碳水总量: {carb_total}g\n"
                result_text += f"一日胰岛素总量: {insulin_total}U\n"
                result_text += f"基于RSI值 {rsi_value}，预计总血糖升高值: {blood_sugar_total:.2f} mmol/L\n"
                result_text += f"胰岛素敏感系数(ISF): {isf_value:.2f} mmol/L/U\n\n"
                result_text += "数据已保存成功!"

                # 更新结果文本显示
                self.result_text.config(state="normal")
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", result_text)
                self.result_text.config(state="disabled")

                # 显示成功消息
                messagebox.showinfo("成功", "ISF校准完成并已保存!")
            else:
                # 保存失败，显示错误信息
                messagebox.showerror("错误", "保存数据失败")

        except ValueError:
            # 输入格式错误处理
            messagebox.showerror("输入错误", "请输入有效的数字")
        except ZeroDivisionError:
            # 除零错误处理
            messagebox.showerror("计算错误", "胰岛素总量不能为零")


class FoodInputWindow:
    """食物信息录入窗口类，用于管理食物数据库"""

    def __init__(self, parent):
        """
        初始化食物信息录入窗口

        参数:
            parent: 父窗口
        """
        self.window = tk.Toplevel(parent)
        self.window.title("食物信息录入")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()

        # 加载食物数据，如果为空则使用空列表
        self.foods_list = load_food_data() or []
        self.setup_ui()  # 设置界面
        self.refresh_food_list()  # 刷新食物列表显示

    def setup_ui(self):
        """设置用户界面"""
        # 标题框架
        title_frame = ttk.Frame(self.window)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="食物信息录入", font=("Arial", 14, "bold")).pack()

        # 新增食物输入区域框架
        input_frame = ttk.LabelFrame(self.window, text="新增食物", padding=15)
        input_frame.pack(fill="x", padx=20, pady=10)

        # 食物名称输入组件
        ttk.Label(input_frame, text="食物名称:").grid(row=0, column=0, sticky="w", pady=8)
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=8, padx=10)

        # 碳水率输入组件
        ttk.Label(input_frame, text="碳水率(/100g):").grid(row=1, column=0, sticky="w", pady=8)
        self.carb_entry = ttk.Entry(input_frame, width=20)
        self.carb_entry.grid(row=1, column=1, sticky="w", pady=8, padx=10)

        # 按钮区域框架
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        # 创建功能按钮
        ttk.Button(button_frame, text="添加食物", command=self.add_food).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_entries).pack(side="left", padx=5)

        # 食物列表显示区域框架
        list_frame = ttk.LabelFrame(self.window, text="已录入的食物", padding=10)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 创建树形视图（表格）显示食物列表
        columns = ("名称", "碳水率(/100g)")  # 定义列名
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)

        # 设置列标题和宽度
        for col in columns:
            self.tree.heading(col, text=col)  # 设置列标题
            self.tree.column(col, width=200)  # 设置列宽

        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)  # 关联滚动条

        # 布局树形视图和滚动条
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 列表操作按钮框架
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.pack(fill="x", pady=5)

        # 创建列表操作按钮
        ttk.Button(list_button_frame, text="删除选中", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(list_button_frame, text="刷新列表", command=self.refresh_food_list).pack(side="left", padx=5)

        # 关闭按钮框架
        close_frame = ttk.Frame(self.window)
        close_frame.pack(fill="x", pady=10)
        ttk.Button(close_frame, text="关闭", command=self.window.destroy).pack()

    def clear_entries(self):
        """清空输入框"""
        self.name_entry.delete(0, tk.END)  # 清空名称输入框
        self.carb_entry.delete(0, tk.END)  # 清空碳水率输入框

    def add_food(self):
        """添加新食物到列表"""
        # 获取并清理输入数据
        name = self.name_entry.get().strip()  # 获取并去除前后空格
        carb_str = self.carb_entry.get().strip()

        # 输入验证
        if not name:
            # 名称不能为空
            messagebox.showerror("输入错误", "食物名称不能为空")
            return

        try:
            # 验证碳水率格式
            carb_rate = float(carb_str)
            if carb_rate < 0:
                # 碳水率不能为负数
                messagebox.showerror("输入错误", "碳水率不能为负数")
                return
        except ValueError:
            # 碳水率格式错误
            messagebox.showerror("输入错误", "请输入有效的碳水率数字")
            return

        # 检查食物是否已存在
        for food in self.foods_list:
            if food['name'].lower() == name.lower():  # 不区分大小写比较
                # 食物已存在，询问是否覆盖
                if messagebox.askyesno("确认", f"食物 '{name}' 已存在，是否覆盖?"):
                    food['carb_100g'] = carb_rate  # 更新现有食物的碳水率
                    break
                else:
                    return  # 用户取消覆盖
        else:
            # 添加新食物（仅在循环正常结束时执行）
            food_data = {
                "name": name,
                "carb_100g": carb_rate
            }
            self.foods_list.append(food_data)

        # 保存数据
        if save_food_data(self.foods_list):
            # 保存成功，刷新界面
            self.refresh_food_list()  # 刷新列表显示
            self.clear_entries()  # 清空输入框
            messagebox.showinfo("成功", f"食物 '{name}' 已保存!")
        else:
            # 保存失败
            messagebox.showerror("错误", "保存食物数据失败")

    def refresh_food_list(self):
        """刷新食物列表显示"""
        # 清空当前列表
        self.tree.delete(*self.tree.get_children())
        # 重新加载数据
        self.foods_list = load_food_data() or []

        # 将每个食物添加到树形视图
        for food in self.foods_list:
            self.tree.insert("", "end", values=(food['name'], food['carb_100g']))

    def delete_selected(self):
        """删除选中的食物"""
        selected = self.tree.selection()  # 获取选中的项目
        if not selected:
            # 没有选中项目
            messagebox.showwarning("警告", "请先选择要删除的食物")
            return

        # 确认删除
        if messagebox.askyesno("确认", "确定要删除选中的食物吗?"):
            for item in selected:
                # 获取选中食物的名称
                food_name = self.tree.item(item)['values'][0]
                # 从列表中移除该食物
                self.foods_list = [food for food in self.foods_list if food['name'] != food_name]

            # 保存更新后的列表
            if save_food_data(self.foods_list):
                self.refresh_food_list()  # 刷新显示
                messagebox.showinfo("成功", "食物已删除")
            else:
                messagebox.showerror("错误", "删除食物失败")


class InsulinCalculationWindow:
    """胰岛素剂量计算窗口类，用于计算胰岛素注射剂量"""

    def __init__(self, parent):
        """
        初始化胰岛素剂量计算窗口

        参数:
            parent: 父窗口对象
        """
        self.window = tk.Toplevel(parent)
        self.window.title("胰岛素剂量计算")
        self.window.geometry("550x500")
        self.window.transient(parent)
        self.window.grab_set()

        # 加载食物数据
        self.foods_data = load_food_data() or []
        self.setup_ui()  # 设置界面

    def setup_ui(self):
        """设置用户界面组件"""
        # 标题框架
        title_frame = ttk.Frame(self.window)
        title_frame.pack(fill="x", pady=10)
        ttk.Label(title_frame, text="计算胰岛素注射剂量", font=("Arial", 14, "bold")).pack()

        # 食物选择区域框架
        selection_frame = ttk.LabelFrame(self.window, text="选择食物", padding=15)
        selection_frame.pack(fill="x", padx=20, pady=10)

        # 食物选择标签
        ttk.Label(selection_frame, text="选择食物:").grid(row=0, column=0, sticky="w", pady=8)

        # 食物下拉框
        self.food_var = tk.StringVar()  # 创建字符串变量
        # 获取食物名称列表，如果没有数据则显示提示
        food_names = [food['name'] for food in self.foods_data] if self.foods_data else ["无食物数据"]
        self.food_combo = ttk.Combobox(selection_frame, textvariable=self.food_var, values=food_names, state="readonly")
        self.food_combo.grid(row=0, column=1, sticky="w", pady=8, padx=10)

        # 如果有食物数据，默认选择第一个
        if food_names:
            self.food_combo.set(food_names[0])

        # 摄入重量输入组件
        ttk.Label(selection_frame, text="摄入重量(g):").grid(row=1, column=0, sticky="w", pady=8)
        self.weight_entry = ttk.Entry(selection_frame, width=15)
        self.weight_entry.grid(row=1, column=1, sticky="w", pady=8, padx=10)

        # 当前参数显示框架
        param_frame = ttk.LabelFrame(self.window, text="当前参数", padding=10)
        param_frame.pack(fill="x", padx=20, pady=10)

        # RSI值显示组件
        ttk.Label(param_frame, text="当前RSI值:").grid(row=0, column=0, sticky="w", pady=5)
        self.rsi_label = ttk.Label(param_frame, text="未加载")
        self.rsi_label.grid(row=0, column=1, sticky="w", pady=5, padx=10)

        # ISF值显示组件
        ttk.Label(param_frame, text="当前ISF值:").grid(row=1, column=0, sticky="w", pady=5)
        self.isf_label = ttk.Label(param_frame, text="未加载")
        self.isf_label.grid(row=1, column=1, sticky="w", pady=5, padx=10)

        # 加载参数数据
        self.load_parameters()

        # 按钮区域框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", pady=15)

        # 创建功能按钮
        ttk.Button(button_frame, text="计算剂量", command=self.calculate_insulin).pack(side="left", padx=10)
        ttk.Button(button_frame, text="清空", command=self.clear_calculation).pack(side="left", padx=10)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side="left", padx=10)

        # 计算结果区域框架
        result_frame = ttk.LabelFrame(self.window, text="计算结果", padding=10)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 创建文本结果显示组件（带滚动条）
        self.result_text = tk.Text(result_frame, height=8, width=50, font=("Arial", 12))
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)  # 关联滚动条
        self.result_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 初始化结果显示文本
        self.result_text.insert("1.0", "请选择食物并输入重量后点击计算")
        self.result_text.config(state="disabled")  # 设置为只读模式

    def load_parameters(self):
        """加载并显示RSI和ISF参数"""
        # 加载RSI数据
        rsi_data = load_rsi_data()  # 直接调用模块函数
        if rsi_data:
            # 如果数据存在，显示RSI值
            self.rsi_label.config(text=f"{rsi_data['rsi_value']}")
        else:
            # 如果数据不存在，显示提示信息
            self.rsi_label.config(text="未找到RSI数据")

        # 加载ISF数据
        isf_data = load_isf_data()  # 直接调用模块函数
        if isf_data:
            # 如果数据存在，显示ISF值
            self.isf_label.config(text=f"{isf_data['isf_value']} mmol/L/U")
        else:
            # 如果数据不存在，显示提示信息
            self.isf_label.config(text="未找到ISF数据")

    def clear_calculation(self):
        """清空计算结果和输入"""
        self.weight_entry.delete(0, tk.END)  # 清空重量输入框
        self.result_text.config(state="normal")  # 设置为可编辑模式
        self.result_text.delete("1.0", tk.END)  # 清空结果文本
        self.result_text.insert("1.0", "请选择食物并输入重量后点击计算")  # 插入默认文本
        self.result_text.config(state="disabled")  # 重新设置为只读模式

    def calculate_insulin(self):
        """计算胰岛素剂量"""
        # 获取选中的食物名称和输入重量
        selected_food_name = self.food_var.get()
        weight_str = self.weight_entry.get().strip()

        # 验证食物选择
        if not selected_food_name or selected_food_name == "无食物数据":
            messagebox.showerror("错误", "请先选择食物")
            return

        # 验证重量输入
        try:
            weight = float(weight_str)
            if weight <= 0:
                messagebox.showerror("输入错误", "重量必须大于0")
                return
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的重量数字")
            return

        # 查找选中的食物数据
        selected_food = None
        for food in self.foods_data:
            if food['name'] == selected_food_name:
                selected_food = food
                break

        # 验证食物数据是否存在
        if not selected_food:
            messagebox.showerror("错误", "未找到选中的食物数据")
            return

        # 检查RSI数据是否存在
        rsi_data = load_rsi_data()  # 直接调用模块函数
        if not rsi_data:
            messagebox.showerror("错误", "未找到RSI校准数据，请先进行RSI校准")
            return

        # 检查ISF数据是否存在
        isf_data = load_isf_data()  # 直接调用模块函数
        if not isf_data:
            messagebox.showerror("错误", "未找到ISF校准数据，请先进行ISF校准")
            return

        # 获取RSI和ISF值
        rsi_value = rsi_data['rsi_value']
        isf_value = isf_data['isf_value']

        # 直接调用模块中的计算函数计算胰岛素剂量
        total_carb, blood_sugar_rise, insulin_dose = calculate_insulin_dose(
            selected_food, weight, rsi_value, isf_value
        )

        # 构建结果显示文本
        result_text = f"食物: {selected_food['name']}\n"
        result_text += f"重量: {weight}g\n"
        result_text += f"碳水含量: {total_carb:.2f}g\n\n"
        result_text += f"预计血糖升高值: {blood_sugar_rise:.2f} mmol/L\n"
        result_text += f"胰岛素注射剂量: {insulin_dose:.2f} U\n\n"
        result_text += f"(基于RSI值: {rsi_value}, ISF值: {isf_value} mmol/L/U)"

        # 更新结果文本显示
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", result_text)
        self.result_text.config(state="disabled")