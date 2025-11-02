import json


def load_json(filename):
    try:
        with open(filename, "r", encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Error: {filename} file not found')
        return {}
