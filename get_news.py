import json
import os
import requests
from datetime import datetime, timedelta
import csdn
"""
我关注的 up 主
稚晖君、快乐治愈小分队、林亦LYi、不高兴就喝水、差评君、硬件茶谈、电丸科技AK、大狸子切切里、ElenaLin_青青、啥都会一点的研究生、小蝶今天吃饱了、NLP从入门到放弃、锦堂生活空间
"""
up_list = [20259914, 1666689045, 4401694, 412704776, 19319172, 14871346, 477782158, 471303350, 5128788, 46880349,
           38060523, 383038901]

# 所有的 up 视频 时间:html卡片

video_list = {

}

# 获取截止现在到7天前的视频
today = datetime.now().replace(hour=23, minute=0, second=0)
before = today - timedelta(days=7)

html_top = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日推荐</title>

    <style type="text/css">
        * {
            padding: 0;
            margin: 0;
        }
        
        body {
            background: rgb(255, 255, 255);
        }
        
        #face_card {
            width: 100%;
            height: 80px;
            text-align: left;
        }
        
        #face {
            width: 50px;
            height: 50px;
            border-radius: 40px;
        }
        
        #nick_name,
        #date {
            margin-left: 30px;
            line-height: 40px;
            overflow: hidden;
            display: inline-block;
        }
        
        #left_box {
            text-align: center;
            margin-left: 50px;
            display: inline-block;
            width: 43%;
        }
        
        #right_box {
            text-align: center;
            margin-right: 50px;
            float: right;
            width: 43%;
        }
        
        .div1 {
            width:100%;
            text-align: center;
            background: rgb(241, 241, 241);
            justify-content: center;
            align-items: center;
            padding: 30px;
            margin: 30px 2% 30px 0px;
            /* 正方形图标圆角半径20px */
            border-radius: 20px;
            /* 第一个值是外阴影X&Y轴方向偏移18px，模糊度半径是30px，阴影颜色为0.2透明度的黑色 */
            /* 第二个值是外阴影X&Y轴方向偏移-18px，模糊度半径是30px，阴影颜色为白色 */
            box-shadow: 18px 18px 30px rgba(0, 0, 0, 0.2), -18px -18px 30px rgba(255, 255, 255, 1);
            /* tricks: 利用transition给常态于按压态两者状态互相变换过程增加缓动动画 */
            transition: all 0.2s ease-in-out;
            display: inline-block;
        }
    </style>

</head>

<body>
"""

html_bottom = """
</body>
</html>
"""


def get_single_up_info(uid):
    url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&offset_dynamic_id=0&need_top=0"
    r = requests.get(url).json()
    html_cards = ""
    for card in r['data']['cards']:
        # 发布时间
        timestamp = card['desc']['timestamp']
        time = datetime.fromtimestamp(timestamp)
        if  before < time < today:
            name = card['desc']['user_profile']['info'].get('uname')
            # 个人信息
            uid = card['desc']['user_profile']['info']['uid']
            face = card['desc']['user_profile']['info']['face']
            name = card['desc']['user_profile']['info'].get('uname')
            type = card['desc']['type']
            # print(type)
            # 获取视频
            if type == 8:
                bvid = card['desc']['bvid']
                video_url = "https://www.bilibili.com/video/" + str(bvid)
                # print(video_url)
                title = json.loads(card['card'])['title']
                # 封面图
                pic = json.loads(card['card'])['pic']
                # print(pic)
                # 视频简介
                desc = json.loads(card['card'])['desc']
                # print(desc)
                # 类型
                tname = json.loads(card['card'])['tname']
                # print(tname)
            # 获取文章
            elif type == 64:
                rid_str = card['desc']['rid_str']
                article_url = "https://www.bilibili.com/read/cv" + str(rid_str)
                # print(article_url)
            # 获取说说
            elif type == 2:
                talk_id = card['desc']['dynamic_id_str']
                talk_url = "https://t.bilibili.com/" + str(talk_id)
                # print(talk_url)
            # 获取多媒体说说
            elif type == 1:
                dynamic_id = card['desc']['dynamic_id']
                dynamic_url = "https://t.bilibili.com/" + str(dynamic_id)
                # print(dynamic_url)
            if type == 8:
                # 生成视频卡片
                html_card = """
                <div class="div1">
                    <div id="face_card">
                        <img id="face" src="{}">
                        <h2 id="nick_name">{}</h2>
                        <h2 id="date" style="color: gray;">{}</h2>
                    </div>
                    <h2>{}</h2>
                    <a href="{}"><img style="width: 450px;height: 300px;margin:20px 0px -10px 0px;border-radius:20px;" src="{}"></a>
                    <p style="margin: 30px;text-align:left;">{}
                    </p>
                </div>
                """.format(face, name, time, title, video_url, pic, desc)
                html_cards += html_card
                video_list.update({timestamp: html_card})



def write_date_to_html(filename, content):
    if not os.path.exists(filename):
        file = open(filename, mode="x", encoding="utf-8")
    file = open(filename, 'w', encoding="utf-8")
    file.write(content)


def generate_html_page(video_list,article_list):
    # 生成哔哩哔哩动态 left_box html 代码
    html_cards_head = '''
    <div id="left_box">
        <h1 style="margin-top: 30px;">bilibili关注up主</h1>
    '''
    html_cards = ""
    html_cards_foot = '''
    </div>
    '''
    for (k, v) in video_list.items():
        html_cards += v
    left_html_cards = html_cards_head + html_cards + html_cards_foot
    right_cards = ''
    # 生成 CSDN 热榜排行 right_box html 代码
    for i in article_list:
        face = i.avatarUrl
        name = i.nickName
        time = i.period
        title = i.articleTitle
        video_url = i.articleDetailUrl
        pic = i.picList[0]
        desc = ''
        right_html_card = """
            <div class="div1">
                <div id="face_card">
                    <img id="face" src="{}">
                    <h2 id="nick_name">{}</h2>
                    <h2 id="date" style="color: gray;">{}</h2>
                </div>
                <h2>{}</h2>
                <a href="{}"><img style="width: 450px;height: 300px;margin:20px 0px -10px 0px;border-radius:20px;" src="{}"></a>
                <p style="margin: 30px;text-align:left;">{}
                </p>
            </div>
            """.format(face, name, time, title, video_url, pic, desc)
        right_cards += right_html_card
    right_html_cards = html_cards_head.replace('left_box', 'right_box').replace('bilibili关注up主', 'CSDN热榜排行')+right_cards+html_cards_foot
    return html_top + left_html_cards +right_html_cards+ html_bottom
# 获取 bilibili1 关注的up主
def get_bilibili_news():
    global video_list
    for i in up_list:
        get_single_up_info(i)
    video_list = sorted(video_list.items(), key=lambda x: x[0], reverse=True)
    print("bilibili动态获取成功!")

# 获取 csdn 热榜
def get_csdn_hot_rank():
    print("CSDN热榜获取成功!")
    return csdn.getMyFocusArticle(csdn.my_favorite_type.split('\n')[1:-1],csdn.get_rank_article_list(),False)

if __name__ == "__main__":
    filename = "index.html"
    get_bilibili_news()
    # 自动生成 html
    content = generate_html_page(dict(video_list),get_csdn_hot_rank())
    write_date_to_html(filename, content)
    print("网页生成成功")
