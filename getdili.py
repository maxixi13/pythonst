from selenium import webdriver
import time
from html.parser import HTMLParser
from lxml import etree

# 停滞时间，可配置为0对电脑性能有要求，程序为阻塞型配置为0基本不会出错
def sleep():
    time.sleep(1)

def getdata(local):
    # 打开浏览器，打开地址
    browser = webdriver.Chrome()
    browser.get("https://lbs.amap.com/console/show/picker")
    sleep()
    # 定位label选择器，选择
    browser.find_element_by_xpath("//*[@id='myPageTop']/table/tbody/tr[1]/td[1]/label[2]").click()
    sleep()
    # 输入坐标
    browser.find_element_by_id("txtSearch").send_keys(local)
    sleep()
    # 定位搜索按钮，点击
    browser.find_element_by_class_name("btn-search").click()
    sleep()
    # 获取html存入内存
    a = browser.page_source
    # 关闭浏览器
    browser.quit()
    # 解析html
    html = etree.HTML(a)
    datadic = html.xpath('//div[@class="amap-icon"]/@title')
    # 输出结果
    return datadic

# 循环获取输入坐标，输出地理位置
# "121.811074,31.141906" ==> ['上海市浦东新区祝桥镇S32申嘉湖高速上海浦东国际机场']
for i in range(10):
    print(getdata("121.811074,31.141906"))