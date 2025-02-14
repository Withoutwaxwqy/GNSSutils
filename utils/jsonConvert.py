import json
import numpy as np

def read_json_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_dict_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def sceneChinese2English(scene_word):
    """
    sceneChinese words to English words
        * scene_word: str
    return: str
    """
    if "高架" in scene_word:
        scene = "elevated"
    elif "隧道" in scene_word:
        scene = "tunnel"
    elif "下穿" in scene_word:
        scene = "underPass"
    elif "林荫" in scene_word or "荫道" in scene_word:
        scene = "forest"
    elif "高架上" in scene_word:
        scene = "elevated"
    elif "高架下" in scene_word:
        scene = "underElevated"
    elif "开阔" in scene_word:
        scene = "openSky"
    elif "车库" in scene_word:
        scene = "garage"
    elif "隧道" in scene_word:
        scene = "tunnel"
    elif "城市道路" in scene_word:
        scene = "cityRoad"
    elif "多径" in scene_word:
        scene = "multiPath"
    elif "城市峡谷" in scene_word:
        scene = "urbanCanyon"
    elif "高楼" in scene_word:
        scene = "highBuilding"
    elif "路" in scene_word:
        scene = "cityRoad"
    else:
        scene = "openSky"
    return scene
 

def sliceTime(time_list, bottom, top):
    """
    slice time list
        * timelist: list[int]
        * bottom: int
        * top: int
    return: time and index
    """
    time_list_array = np.array(time_list)
    bottom_index = np.where(time_list_array >= bottom)[0][0]
    top_index = np.where(time_list_array <= top)[0][-1]
    l = [i for i in range(bottom_index, top_index)]
    return time_list_array[bottom_index:top_index], l