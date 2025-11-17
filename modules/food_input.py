from utils.file_utils import load_json, save_json


def load_food_data():
    """加载食物数据"""
    data = load_json('foods_data.json')
    return data if data is not None else []


def check_duplicate_food(foods_list, new_name):
    """检查新食物名称是否与现有列表重复（不区分大小写）"""
    existing_names = [food["name"].lower() for food in foods_list]
    return new_name.lower() in existing_names

def save_food_data(foods_data):
    """保存食物数据"""
    return save_json(foods_data, 'foods_data.json')

def update_food_data(foods_data, index, updated_data):
    """
    更新指定索引的食物数据
    """
    if 0 <= index < len(foods_data): #要修改的食物索引
        foods_data[index] = updated_data #更新后的食物数据字典
        save_food_data(foods_data) #所有食物数据列表
        return True
    return False


def delete_food_data(foods_data, index):
    """
    删除指定索引的食物数据

    参数:
        foods_data: 食物数据列表（包含所有食物信息的字典列表）
        index: 要删除的食物在列表中的索引

    返回:
        bool: 若索引有效且删除成功则返回True，否则返回False
    """
    # 校验索引合法性（确保在列表有效范围内）
    if 0 <= index < len(foods_data):
        # 移除指定索引的元素
        foods_data.pop(index)
        # 保存修改后的数据到文件
        save_food_data(foods_data)
        return True
    # 索引无效时返回False
    return False

def input_food_data():
    """
    食物信息录入函数：用于收集用户输入的食物名称及营养成分（碳水化合物、蛋白质、脂肪），
    并将新录入的数据与已有数据合并后保存。支持中途退出并保存已录入信息。
    """
    # 打印功能标题，提示用户进入食物信息录入模块
    print("\n=== 食物信息录入 ===")

    # 加载已保存的食物数据（假设load_food_data()是一个读取本地保存数据的函数）
    existing_data = load_food_data()

    # 初始化食物列表：如果已有数据则复制一份（避免直接修改原数据），否则创建空列表
    foods_list = existing_data.copy() if existing_data else []

    # 提示用户输入规则：按提示输入，输入'q'可退出
    print("请按提示输入食物信息，输入 'q' 可退出")

    # 循环录入食物信息（持续接收输入直到用户主动退出）
    while True:
        # 打印分隔线，区分不同食物的录入区域，提升可读性
        print("\n" + "-" * 30)

        # 接收用户输入的食物名称，并去除首尾空格
        foods_name = input("请输入食物名称(输入q退出): ").strip()

        # 判断用户是否输入'q'（不区分大小写），如果是则退出录入循环
        if foods_name.lower() == 'q':
            break

        # 校验食物名称是否为空：如果为空，提示重新输入并跳过本次循环剩余部分
        if not foods_name:
            print("食物名称不能为空，请重新输入")
            continue

        # 检查是否存在重复名称（不区分大小写，避免重复录入）
        # 提取现有食物名称并转为小写，用于比较
        if check_duplicate_food(foods_list, foods_name):
            print(f"警告：食物 '{foods_name}' 已存在，请使用不同名称或修改已有食物")
            continue  # 跳过当前食物录入，重新开始循环

        # 录入碳水化合物含量（每100g食物中的克数）
        # 使用循环确保用户输入有效的非负数字，直到输入正确或退出
        while True:
            foods_carb = input("请输入食物每100g碳水化合物含量(g): ").strip()

            # 如果用户输入'q'，则保存当前已录入的数据并退出函数
            if foods_carb.lower() == 'q':
                save_food_data(foods_list)  # 假设save_food_data()是保存数据的函数
                return

            # 尝试将输入转换为浮点数，验证输入有效性
            try:
                foods_carb = float(foods_carb)
                # 校验是否为非负数（营养成分含量不能为负）
                if foods_carb >= 0:
                    break  # 输入有效，跳出当前循环
                else:
                    print("含量不能为负数,请重新输入")
            except ValueError:
                # 如果转换失败（输入不是数字），提示用户输入有效数字
                print("请输入有效的数字")

        # 录入蛋白质含量（逻辑与碳水化合物一致）
        while True:
            foods_protein = input("请输入食物每100g蛋白质含量(g): ").strip()

            if foods_protein.lower() == 'q':
                save_food_data(foods_list)
                return

            try:
                foods_protein = float(foods_protein)
                if foods_protein >= 0:
                    break
                else:
                    print("含量不能为负数,请重新输入")
            except ValueError:
                print("请输入有效的数字")

        # 录入脂肪含量（逻辑与上述营养成分一致）
        while True:
            foods_fat = input("请输入食物每100g脂肪含量(g): ").strip()

            if foods_fat.lower() == 'q':
                save_food_data(foods_list)
                return

            try:
                foods_fat = float(foods_fat)
                if foods_fat >= 0:
                    break
                else:
                    print("含量不能为负数,请重新输入")
            except ValueError:
                print("请输入有效的数字")

        # 将当前录入的食物信息整理为字典（包含名称和三种营养成分）
        food_data = {
            "name": foods_name,  # 食物名称
            "carb_100g": foods_carb,  # 每100g碳水化合物含量
            "protein_100g": foods_protein,  # 每100g蛋白质含量
            "fat_100g": foods_fat  # 每100g脂肪含量
        }

        # 将当前食物信息添加到食物列表中
        foods_list.append(food_data)
        # 提示用户当前食物已成功录入
        print(f"'{foods_name}' 已成功录入!")

        # 询问用户是否继续录入其他食物
        continue_input = input("\n是否继续录入其他食物? (y/n): ").strip().lower()
        # 如果用户输入不是'y'（不区分大小写），则退出录入循环
        if continue_input != 'y':
            break

    # 当用户退出录入循环后，保存所有已录入（包括新增和原有）的食物数据
    save_food_data(foods_list)
    return foods_list