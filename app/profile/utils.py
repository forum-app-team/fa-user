import re

def camel_to_snake(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

def snake_to_camel(name: str) -> str:
    parts = name.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def normalize_keys(data: dict, to: str) -> dict:
    if to == "camel":
        return {snake_to_camel(k): v for k, v in data.items()}
    elif to == "snake":
        return {camel_to_snake(k): v for k, v in data.items()}
    else:
        valid_options = ["camel", "snake"]
        raise ValueError(f"Unsupported option: {to}. Must be one of {valid_options}")
    

