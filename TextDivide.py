import requests , urllib
import json

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?charset=UTF-8&grant_type=client_credentials&client_id=YQLDGliruieSX3enMdSCfG7u&client_secret=xfG4Sfk9hq4CVoG8iCFi76A2dP5tFx6c'

postdata = json.dumps({'Content-Type': 'application/json'})
r = requests.post(host, data=postdata)

token = json.loads(r.text)['access_token']
print(token)
# url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/depparser?access_token={}'.format(token)
# url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer_custom?access_token={}'.format(token)
# url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/dnnlm_cn?access_token={}'.format(token)
url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer_custom?access_token==24.76b7a4af183b2295c73b0a70b85c4619.2592000.1529647758.282335-11252294'
print(url)

postdata2 = json.dumps({'text': '"我要去星空错觉艺术馆', "mode": 1})

print(postdata2)
re = requests.post(url, data=postdata2)
if re.text:
    print(re.text)

'''
    1 先找到ATT 然后一直叠加，直到VOB       我要到昌平电子基地
    2 
'''


items = json.loads(re.text)['items']
location = ''
start = False

for item in items:
    if start | ('ATT' == item['deprel']):
        location += item['word']
        start = True


print(location)


import thulac


th = thulac.thulac()
print(th.cut("买一张到昌平电子基地的票"))
