import os
import sys
import bs4
import json
import requests
import urllib.request

class NetEase_Cloud_Music():
    def __init__(self,url):
        self.music_id = url.split("=")[-1]
        self.music_name = ""
        self.path = os.path.split(os.path.realpath(__file__))[0]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        print("准备开始下载......")
    
    
    # 获取歌名
    def get_music_name(self):
        print("开始搜索歌名......")

        # 请求头
        headers = {'user-agent':self.user_agent,
                   'referer':"https://music.163.com/"
            }
        
        # 歌名链接
        music_name_url = "https://music.163.com/song?id=" + self.music_id
        
        # 下载整个网页并提取歌曲名
        response = requests.get(url=music_name_url,headers=headers)
        html = bs4.BeautifulSoup(response.text,'html.parser')       # 指定 html 解析器
        name_html_text = html.find_all("title")                     # 定位
        
        for each in name_html_text:
            self.music_name = each.text.split("-")[0].strip(" ")

        print("歌名搜索完成......")

    # 下载音乐
    def music_load(self):
        print("正在下载音频......")

        # 歌曲链接
        music_url = "http://music.163.com/song/media/outer/url?id={0}.mp3".format(self.music_id)

        response = urllib.request.urlopen(music_url)
        music_res = response.read()

        # 歌曲路径，及名字
        music_file_name = self.path + "\\" + self.music_name + ".mp3"
        
        with open(music_file_name,"wb") as f:
            f.write(music_res)
        
        print("音频下载完成......\n即将下载歌词......")
    
    # 下载歌词
    def get_music_Lyric(self):
        print("正在下载歌词......")

        # 请求头
        Lyric_url = "http://music.163.com/api/song/lyric?id={0}&lv=1&kv=1&tv=-1".format(self.music_id)
        referer = "https://music.163.com/song?id={0}".format(self.music_id)
        # 传入请求头参数
        request_headers = { 'user-agent':self.user_agent,
                            'referer':referer
            }
             
        # 下载整个网页
        Lyric_html = requests.get(url=Lyric_url,headers=request_headers)
        
        # 转换 Python 数据类型
        Lyric_data = json.loads(Lyric_html.text)
        
        # 定位歌词位置
        music_Lyric = Lyric_data["lrc"]["lyric"] 

        # 歌词保存位置，及文件名
        Lyric_File_Name = self.path + "\\" + self.music_name + ".lrc" 
        
        with open(Lyric_File_Name,"w") as f:
            f.write(music_Lyric)
        
        print("歌词下载完成......\n程序运行结束......")


if __name__ == "__main__":
    user_input_url = input("请输入音乐链接：")
 
    CloudMusic = NetEase_Cloud_Music(user_input_url)
    CloudMusic.get_music_name()
    CloudMusic.music_load()
    CloudMusic.get_music_Lyric()