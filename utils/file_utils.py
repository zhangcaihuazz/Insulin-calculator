import json
import os
import streamlit as st
from .path_utils import get_data_path


def save_json(data, filename):
    """保存数据到JSON文件（同时保存到本地和GitHub）"""
    try:
        # 1. 先保存到本地（作为缓存）
        filepath = get_data_path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # 2. 如果配置了GitHub，同步到GitHub
        if is_github_configured():
            from .github_storage import save_to_github
            success = save_to_github(data, filename)
            if success:
                print(f"数据已同步到GitHub: {filename}")
            else:
                print(f"GitHub同步失败，数据仅保存到本地: {filename}")
        else:
            print(f"数据保存到本地: {filepath}")

        return True
    except (IOError, OSError) as e:
        # 文件操作错误
        print(f'文件操作错误: {e}')
        return False
    except TypeError as e:  # 修改这里：JSON编码错误实际上会抛出TypeError
        # JSON编码错误
        print(f'JSON编码错误: {e}')
        return False
    except ImportError as e:
        # 模块导入错误
        print(f'导入github_storage模块失败: {e}')
        return False
    except Exception as e:
        # 保留一个通用的异常捕获作为最后防线
        print(f'保存文件时发生未知错误: {e}')
        return False


def load_json(filename):
    """从JSON文件加载数据（优先从本地加载，失败则从GitHub加载）"""
    try:
        # 1. 先尝试从本地加载
        filepath = get_data_path(filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)

        # 2. 本地文件不存在，尝试从GitHub加载
        if is_github_configured():
            from .github_storage import load_from_github
            data = load_from_github(filename)
            if data is not None:
                # 将从GitHub加载的数据保存到本地缓存
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"从GitHub加载并缓存: {filename}")
                return data

        return None
    except (IOError, OSError) as e:
        # 文件操作错误
        print(f'文件操作错误: {e}')
        return None
    except json.JSONDecodeError as e:  # 这个异常是存在的
        # JSON解码错误
        print(f'JSON解码错误: {e}')
        return None
    except ImportError as e:
        # 模块导入错误
        print(f'导入github_storage模块失败: {e}')
        return None
    except Exception as e:
        # 保留一个通用的异常捕获作为最后防线
        print(f'读取文件时发生未知错误: {e}')
        return None


def is_github_configured():
    """检查是否配置了GitHub"""
    try:
        return (
            "GITHUB_TOKEN" in st.secrets and
            "GITHUB_REPO" in st.secrets and
            st.secrets["GITHUB_TOKEN"] and
            st.secrets["GITHUB_REPO"]
        )
    except (AttributeError, KeyError, TypeError) as e:
        # st.secrets 可能不存在，或者格式不正确
        print(f"检查GitHub配置时出错: {e}")
        return False


def file_exists(filename):
    """检查文件是否存在（本地或GitHub）"""
    filepath = get_data_path(filename)
    if os.path.exists(filepath):
        return True

    if is_github_configured():
        try:
            from .github_storage import github_file_exists
            return github_file_exists(filename)
        except ImportError as e:
            print(f"导入github_storage模块失败: {e}")
            return False

    return False