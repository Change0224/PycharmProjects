from urllib import request

with request.urlopen('http://www.baidu.com') as f:
    print("f的类型",type(f))
    print("Status:",f.status,f.reason)
    data = f.read()  #读取网页内容
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', data.decode('utf-8'))