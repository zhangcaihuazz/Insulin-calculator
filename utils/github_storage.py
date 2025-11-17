import requests
import base64
import json
import streamlit as st
from utils.file_utils import save_json, load_json, file_exists


def get_github_file_path(filename):
    """生成GitHub文件路径"""
    return f"data/{filename}"


def github_file_exists(filename):
    """检查GitHub上文件是否存在"""
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        branch = st.secrets.get("GITHUB_BRANCH", "main")

        url = f"https://api.github.com/repos/{repo}/contents/{get_github_file_path(filename)}?ref={branch}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)
        return response.status_code == 200
    except Exception:
        return False


def load_from_github(filename):
    """从GitHub加载数据"""
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        branch = st.secrets.get("GITHUB_BRANCH", "main")

        url = f"https://api.github.com/repos/{repo}/contents/{get_github_file_path(filename)}?ref={branch}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()["content"]
            # GitHub API返回的是base64编码的内容
            decoded_content = base64.b64decode(content).decode('utf-8')
            return json.loads(decoded_content)
        else:
            return None
    except Exception as e:
        st.error(f"从GitHub加载数据失败: {str(e)}")
        return None


def save_to_github(data, filename, commit_message="Update data"):
    """保存数据到GitHub"""
    try:
        token = st.secrets["GITHUB_TOKEN"]
        repo = st.secrets["GITHUB_REPO"]
        branch = st.secrets.get("GITHUB_BRANCH", "main")

        # 检查文件是否存在以获取sha（用于更新）
        file_sha = None
        if github_file_exists(filename):
            url = f"https://api.github.com/repos/{repo}/contents/{get_github_file_path(filename)}?ref={branch}"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                file_sha = response.json()["sha"]

        # 准备文件内容
        content = json.dumps(data, ensure_ascii=False, indent=2)
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        # 创建或更新文件
        url = f"https://api.github.com/repos/{repo}/contents/{get_github_file_path(filename)}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch
        }
        if file_sha:
            payload["sha"] = file_sha

        response = requests.put(url, headers=headers, json=payload)
        return response.status_code in [200, 201]
    except Exception as e:
        st.error(f"保存到GitHub失败: {str(e)}")
        return False