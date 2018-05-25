#encoding=utf-8
'''
使用Place API把从文本中提取出的地址转换为对应的经纬度坐标，再使用Geocoding API把经纬度坐标查询附件地铁站点。
'''

from xml.etree import ElementTree
import json
import urllib.request

search = urllib.parse.quote(u'八一广场'.encode('utf-8'))
region = urllib.parse.quote(u'南昌'.encode('utf-8'))
url = u"http://api.map.baidu.com/place/v2/search?query=%s&region=%s&city_limit=true&output=json&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T"%(search, region)
print(url)
req = urllib.request.urlopen(url)   # JSON格式的返回数据
res = req.read().decode("utf-8")    # 将其他编码的字符串解码成unicode
temp = json.loads(res)
print(temp)
address = temp['results'][0]['address']     # 地址
location = temp['results'][0]['location']   # 经纬度坐标
print(address, location)

lat = str(location['lat'])  # 纬度坐标
lng = str(location['lng'])  # 经度坐标
query = urllib.parse.quote(u'地铁站'.encode('utf-8'))
# url2 = u'http://api.map.baidu.com/geocoder/v2/?callback=renderReverse&location='+lat+','+lng+'&output=xml&pois=1&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T'
url2 = 'http://api.map.baidu.com/place/v2/search?query=%s&location=%s,%s&radius=10000&sort_name:distance|sort_rule:1&output=json&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T'%(query, lat, lng)
print(url2)
req2 = urllib.request.urlopen(url2)     # XML格式的返回数据
res2 = req2.read().decode("utf-8")  # 将其他编码的字符串解码成unicode

print(res2)
# root = ElementTree.fromstring(res2)     # 解析XML时直接将字符串转换为一个Element，解析树的根节点
# node_find = root.find('result/formatted_address')   # find()用于查找属于某个tag的第一个element，这里查找结构化地址
# print(node_find.text)   # 输出结构化的地址

# url3= 'http://api.map.baidu.com/routematrix/v2/driving?output=json&origins=22.775956,113.618675&destinations=22.758707,113.579597&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T';
'''
"name": "八一馆",
"location": {
    "lat": 28.681604,
    "lng": 115.898264
}

"name":"庐山南大道",
"location":{
    "lat":28.706792,
    "lng":115.871905
}

'''
url3 = 'http://api.map.baidu.com/direction/v2/transit?origin=28.681604,115.898264&destination=28.706792,115.871905&tactics_incity=5&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T'
data = urllib.request.urlopen(url3)

print(data.read().decode("utf-8"))


url4 = 'http://api.map.baidu.com/place/v2/search?query=%s&location=%s,%s&radius=100&sort_name:distance|sort_rule:1&output=json&ak=CNQ3tzhnuupZY1v41lkBv8vGvMWNvc4T'%(query, '28.680994393721', "115.89237007919")
print(url4)
req4 = urllib.request.urlopen(url4)     # XML格式的返回数据
res4 = req4.read().decode("utf-8")  # 将其他编码的字符串解码成unicode

print(res4)

