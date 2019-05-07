import requests
import re
from lxml import etree
import csv
import time
import os
class tongcheng():
    def __init__(self, local_num):
        #构建user-agent，反反爬虫
        self.agent = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"," Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)","Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50","Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0","Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"]
        #控制user-agent选择
        self.agent_num = 0
        #初始化header
        self.headers = {
            "User-Agent": self.agent[self.agent_num]}
        #初始化种子网址
        self.url = "https://{}.58.com/job/pn{}"
        #初始化地区网址
        self.local = ["jn","lw","yt","qd","jining","wf","linyi","zb","ta","lc","weihai","zaozhuang","dz","rizhao","dy","heze","bz"]
        #划分各地区爬取数据数量
        self.count = (local_num/17)+1
        #控制代理池选择
        self.i = 0
        #控制表头写入
        self.flag = 0
        #代理字典
        self.proxies = {}
        #代理列表
        self.proxy_list = []
        #提取代理
        f = open("D:/Python代理/proxy.txt","r",encoding="utf-8")
        line = f.readline()
        while line :
            line = line.replace("\n","")
            line_list = line.split(":")
            self.proxy_list.append(line_list)
            line = f.readline()
        #判断是否生成表头
        if os.path.exists('d://write.csv') :
                self.flag = 1

    def run(self):#主逻辑
        pass
        for i in  range(1,len(self.local))  :
            pn = 1#页码
            count = 0#爬取本地区的数据数量
            while True :
                data_list = []
                if count > self.count :#判断在该地区是否爬取了足够的数据
                    break;
                # 1.获取招聘信息列表
                url_list = self.get_list(self.url.format(self.local[i],pn))
                print("正在提取详细信息")
                for url in url_list :
                    # 2.发送请求
                    html_str = self.parse_url(url=url)
                    # 3.提取数据放入列表
                    data_list.append(self.get_data(html_str))
                    count += 1
                # 4.保存至csv
                print("保存信息中")
                self.save_csv(data_list)
                # 5.翻页
                print("{}条信息保存成功，接下来进行反反爬虫设置".format(count))
                pn += 1
                time.sleep(2)#反反爬虫设置
            #6.切换下一个城市
            print("切换下一个城市，预计五秒后启动爬虫")
            time.sleep(5)
    def parse_url(self,url):#发送请求
        if self.i > (len(self.proxy_list)/3) :#判断代理是否用尽
            self.i = 0
        self.proxies[self.proxy_list[self.i][0]] ="{}:{}".format(self.proxy_list[self.i][1],self.proxy_list[self.i][2])#拼合代理
        self.headers = {"User-Agent": self.agent[self.agent_num]}#选择user-agent
        if self.agent_num < len(self.agent)-1 :#判断user-agent是否用尽
            self.agent_num += 1
        else:
            self.agent_num = 0
        self.i += 1
        try:
            response = requests.get(url,headers=self.headers,proxies=self.proxies)#获取元数据
        except:
            return  self.parse_url(url=url)#异常后递归获取
        return response.content.decode()
    def get_list(self,url):#构建URL列表
        html_str = self.parse_url(url=url)
        url_list = re.findall("__addition=\"0\"><a href=\"(.*?)\" urlparams=\'psid=", html_str, re.S)#正则筛选url
        print("url列表构建完成")
        return url_list
    def get_data(self,str):#获取有效数据
        data = []
        str = etree.HTML(str)#转换为可用xpath提取的html
        data.append("".join(str.xpath("//span[@class='pos_area_span pos_address']//text()")))#获取招聘地区
        data.append("".join(str.xpath("//div[@class ='baseInfo_link']//text()")))#获取公司名称
        data.append("".join(str.xpath("//div[@class='pos-area']/span[2]//text()")))#获取详细地址
        data.append("".join(str.xpath("//span[@class='pos_title']//text()")))#获取招聘岗位
        data.append("".join(str.xpath("//span[@class='pos_salary']//text()")))#获取薪资
        data.append("".join(str.xpath("//div[@class='pos_welfare']//text()")))#获取福利
        data.append("".join(str.xpath("//div[@class='pos_base_condition']//text()")))#获取岗位要求
        data.append("".join(str.xpath("//div[@class='des']//text()")))#获取详细需求
        data.append("".join(str.xpath("//div[@class='shiji']//text()")))#获取公司介绍
        data.append("".join(str.xpath("//span[@class='item_num join58_num']//text()")))#获取入驻58天数
        return data
    def save_csv(self,list):#保存到csv
        with open('58TongCheng.csv', 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if self.flag == 0 :#判断是否需要生成表头
                title = ["招聘地区","公司名称","详细地址","招聘岗位","薪资","福利","岗位要求","详细需求","公司介绍","入驻58天数"]
                csv_writer.writerow(title)
                self.flag = 1
            for info in list :
                try :
                    csv_writer.writerow(info)#写入数据
                except:
                    continue


if __name__ == '__main__':
    run = tongcheng(6000)#此处填入爬取数据数目，因为每页数据不同，会有5%~10%偏差
    run.run()#运行