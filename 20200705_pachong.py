import json
import time
from selenium import webdriver
import requests
import pandas as pd
from lxml import etree

# 打开excel
readex = pd.read_excel("data.xlsx", index=False)

# 获取坐标
# i 行数
def getdatalocal(i):
    data = readex.values[i, 1]
    return data


# 存入数据并写入
# i        行数
# ccdata   写入的内容
def savedata(i, ccdata):
    readex.loc[i, "address"] = ccdata
    readex.to_excel("data.xlsx", index=False)


# 请求获取地址，通过接口获取
# local 坐标
# return address
def getaddress(local):
    url = "https://restapi.amap.com/v3/geocode/regeo?key=8325164e247e15eea68b59e89200988b&s=rsv3&location=" + local + "&radius=2800&platform=JS&logversion=2.0&sdkversion=1.3&appname=https%3A%2F%2Flbs.amap.com%2Fconsole%2Fshow%2Fpicker&csid=AB88D5D4-3C9A-46BF-A27E-0397EEAC2509"
    res = requests.get(url)
    getres = json.loads(res.text)
    print(getres['regeocode']['formatted_address'])
    return getres['regeocode']['formatted_address']


# 停滞时间，可配置为0对电脑性能有要求，程序为阻塞型配置为0基本不会出错
def sleep():
    time.sleep(0)


# 通过html抓取获取地址，并输出保存
# num   执行行数
def getdata(num):
    # 定位label选择器，选择
    browser.find_element_by_xpath("//*[@id='myPageTop']/table/tbody/tr[1]/td[1]/label[2]").click()
    sleep()
    # 获取坐标
    lc = getdatalocal(num)
    # 输入坐标
    browser.find_element_by_id("txtSearch").send_keys(lc)
    sleep()
    # 定位搜索按钮，点击
    browser.find_element_by_class_name("btn-search").click()
    sleep()
    # 获取html存入内存
    a = browser.page_source
    # 解析html
    html = etree.HTML(a)
    datadic = html.xpath('//div[@class="amap-icon"]/@title')
    # 输出地址保存
    savedata(num, datadic[0])
    browser.find_element_by_id("txtSearch").clear()
    print("靓仔提醒：第", num, "次执行完成")


# 获取数据长度
# datalen = readex.shape[0]
# getdata(datalen)

# 主程序
# 提醒程序

# 设置字体为红色
print('\033[31m提示开始执行前请关闭excel和浏览器')
in_content = input("请输入回车开始执行：")

# j*10为执行次数，例如j=10执行100次，i为每几次开关一次浏览器
for j in range(10):
    try:
        # 打开浏览器，打开地址
        browser = webdriver.Chrome()
        browser.get("https://lbs.amap.com/console/show/picker")
        sleep()
        for i in range(10):
            try:
                getdata(j * 10 + i)
            except:
                print("出现错误：第", j * 10 + i, "次错误")
        # 关闭浏览器
        browser.quit()
    except:
        print("主循环错误：第", j * 10, "次之后10次循环出现错误")
