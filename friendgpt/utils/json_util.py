import json
import os
from typing import Optional, Dict


def text_to_json(text: str) -> Optional[Dict]:
    try:
        start = text.find('{')
        end = text.rfind('}') + 1

        json_str = text[start:end]

        return json.loads(json_str)
    except Exception as e:
        print(f"text_to_json Exception: {e}")
        return None


def dict_from_json(
        env_or_file: str,
        file_location: str = "config",
) -> Optional[Dict]:
    """Translate environmental variables or json in files into a dictionary.

    :param env_or_file: Name of the environmental variable or file.
    :param file_location: Relative path of the file, The default value is extensions.

    :return: The dictionary after conversion.
    """

    json_str = os.environ.get(env_or_file)
    if json_str:
        return json.loads(json_str)
    else:
        # 基于引用 dict_from_json 函数的文件的绝对路径
        config_list_path = os.path.abspath(os.path.join(os.getcwd(), file_location + "/" + env_or_file))
        # 基于 world_os 包的绝对路径
        # config_list_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir + "/" + file_location + "/" + env_or_file))
        try:
            with open(config_list_path) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return None
