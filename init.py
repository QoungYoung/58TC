import requests
import re
import time
class get_proxy():
    def __init__(self):
        self.headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        self.url = "https://www.kuaidaili.com/free/inha/{}/"

    def parse_url(self,url):#获取数据
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_data(self,html_str):#获取IP，端口号，协议类型
        ip_list = re.findall(r"data-title=\"IP\">(.*?)</td>",html_str,re.S)
        port_list = re.findall(r"data-title=\"PORT\">(.*?)</td>",html_str,re.S)
        type_list = re.findall(r"data-title=\"类型\">(.*?)</td>",html_str,re.S)
        print(ip_list)
        return ip_list,port_list,type_list

    def save_porxy(self,ip_list,port_list,type_list):#将字符串整合为字典并保存
        with open("proxy.txt","w",encoding="utf-8") as f :
            for i in range(len(ip_list)):
                print("正在保存"+ip_list[i])
                f.write(type_list[i]+":"+ip_list[i]+":"+port_list[i]+"\n")
        f.close()

    def run(self):
        # 0.初始化页码
        for i in range(1,15):
            # 1.获取数据
            html_str = self.parse_url(self.url.format(i))
            # 2.提取数据
            ip_list,port_list,type_list = self.get_data(html_str)
            # 3.整合并保存数据
            self.save_porxy(ip_list=ip_list,port_list=port_list,type_list=type_list)
            time.sleep(1)


if __name__ == '__main__':
    p =get_proxy()
    p.run()