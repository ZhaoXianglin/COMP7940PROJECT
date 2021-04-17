from aip import AipImageClassify
import json
def calorie(image):
    """ 你的 APPID AK SK """
    APP_ID = '24002318'
    API_KEY = 'FToZ01XN7fUNwkGQrS48G5Xj'
    SECRET_KEY = '7HwVy0gikylVclUHYaMKQYdrFLuaLqib'

    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    """ 读取图片 """
    # def get_file_content(filePath):
    #     with open(filePath, 'rb') as fp:
    #         return fp.read()

   

    """ 调用菜品识别 """
    client.dishDetect(image)

    """ 如果有可选参数 """
    options = {}
    options["top_num"] = 3
    options["filter_threshold"] = "0.7"
    options["baike_num"] = 5

    """ 带参数调用菜品识别 """

    return client.dishDetect(image, options)

    