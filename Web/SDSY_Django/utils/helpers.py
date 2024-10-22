import json

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def format_date(date_string):
    # 假设日期格式为 "YYYY-MM-DD"
    year, month, day = date_string.split('-')
    return f"{year}年{month}月{day}日"
