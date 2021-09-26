# -*-coding:utf-8-*- 
# 作者：   29511
# 文件名:  demo01.py
# 日期时间：2021/9/26，17:12
"""
EasyDL 图像分类 调用模型公有云API Python3实现
"""
# 错误列表 https://ai.baidu.com/ai-doc/EASYDL/Sk38n3baq#%E9%94%99%E8%AF%AF%E7%A0%81
import json
import base64
import requests
from gooey import Gooey, GooeyParser

"""
  pip install requests, gooey
"""


@Gooey(encoding='utf-8', program_name="检测是否戴口罩-V1.0.0", language='chinese')
def select_image_file():
    parser = GooeyParser(description="检测是否戴口罩!")
    parser.add_argument("image_filepath", help="请选择要识别照片的文件路径：", widget="FileChooser")  # 文件选择框
    args = parser.parse_args()  # 接收界面传递的参数
    return args


if __name__ == '__main__':
    # 可选的请求参数
    # top_num: 返回的分类数量，不声明的话默认为 6 个
    PARAMS = {"top_num": 2}

    # 服务详情 中的 接口地址
    MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/check_mask_api"

    # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
    # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
    ACCESS_TOKEN = ""
    API_KEY = "eSqSWSGnpKR1xDgwHHhzqEfc"
    SECRET_KEY = "5d4R1HufR1keC59mRSI5oHEUPECHeDyq"

    # 调用函数，获取界面传递的参数
    args = select_image_file()
    # 解析传递回来的参数变量 目标图片的 本地文件路径，支持jpg/png/bmp格式
    image_filepath = args.image_filepath
    # 使用参数变量
    print("读取目标图片 '{}'".format(image_filepath))
    with open(image_filepath, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        base64_str = base64_data.decode('UTF8')
    # print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
    PARAMS["image"] = base64_str

    if not ACCESS_TOKEN:
        # print("2. ACCESS_TOKEN 为空，调用鉴权接口获取TOKEN")
        auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials" \
                   "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
        auth_resp = requests.get(auth_url)
        auth_resp_json = auth_resp.json()
        ACCESS_TOKEN = auth_resp_json["access_token"]
        # print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
    # else:
    # print("2. 使用已有 ACCESS_TOKEN")

    # print("3. 向模型接口 'MODEL_API_URL' 发送请求")
    request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
    response = requests.post(url=request_url, json=PARAMS)
    response_json = response.json()
    response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
    # print("结果:\n{}".format(response_str))

    try:
        name = response_json['results'][0]['name']
        score = float(response_json['results'][0]['score'])

        if name == 'image_mask':
            print("戴口罩的概率为%.3f" % score)
        else:
            print("未戴口罩的概率为%.3f" % score)
        print('-' * 100)
    except Exception as e:
        # 如果不存在results, 则为错误信息
        error_code = response_json['error_code']
        error_msg = response_json['error_msg']
        print("error_code----------", error_code)
        print("error_msg----------", error_msg)
