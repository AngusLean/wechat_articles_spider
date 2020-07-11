
from wechatarticles.WechartHelper import weChartHelper


if __name__ == "__main__":
    title = '测试'
    url = 'http://mp.weixin.qq.com/s?__biz=MzAwMTAwMzcxMg==&mid=2650864370&idx=1&sn=13f1e64ba248693982bf713139101cee&chksm=8114035db6638a4bda88e91c328ace7aa2ea936e8ded616aff8c1ff3ead0c243fc005b3579b0#rd'
    path = './pdf/'
    html = weChartHelper.refresh_wechart_cotent4_download(url, title, path)
    print(html)
