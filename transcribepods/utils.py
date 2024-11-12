import json 
import os
import tiktoken

data_folder_path = os.path.abspath(os.path.join(__file__, "./../../data"))

def save_to_json(data, 
                    info = "data"):
    if not isinstance(data, dict):
        data = {f"{info}": list(set(data))}
    with open(f'{data_folder_path}/{info}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename):
    with open(f'{data_folder_path}/{filename}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def count_tokens(text, model="gpt-4o-mini"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
