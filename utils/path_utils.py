import os


def get_script_dir():
    """获取脚本所在目录"""
    return os.path.dirname(os.path.abspath(__file__))


def get_data_path(filename):
    """生成数据文件的完整路径"""
    script_dir = get_script_dir()
    # 数据文件存放在项目根目录的data文件夹中
    project_root = os.path.dirname(script_dir)  # 回到上一级目录（项目根目录）
    data_dir = os.path.join(project_root, 'data')

    # 如果data目录不存在，则创建
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    return os.path.join(data_dir, filename)