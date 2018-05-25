from aip import AipSpeech
import os
""" 你的 APPID AK SK """
APP_ID = '11220380'
API_KEY = 'FMalerGcUNGzHxFlAYyQ3EQQ'
SECRET_KEY = '0p3ow1RASkLcs3MFCWwxV8Kb4HUaaqhi'


client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


path = 'C:\\Users\\built\\Desktop\\sound'

print('请输入文件名')
name = input()

print(path+'\\'+name)
# 识别本地文件
if os.path.exists(path+'\\'+name):
    ret = client.asr(get_file_content(path+'\\'+name), 'wav')
    print(ret)



