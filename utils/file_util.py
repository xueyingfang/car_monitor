import json
from typing import List, Dict

def read_json_file(file_path: str) -> List[Dict]:
    """读取json数组文件，文件不存在返回空列表"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def write_json_file(file_path: str, data: List[Dict]):
    """写入json数组"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
