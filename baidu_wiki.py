import requests
import re
from bs4 import BeautifulSoup
import time
from qqbot.utf8logger import WARN, ERROR
from jinja2 import Environment, PackageLoader
from pyperclip import copy
import tempfile
import os


def limited_items(value, length=255):
    tmp = []
    cur_len = 0
    for item in value:
        v = item
        try:
            _, v = item
        except:
            pass
        cur_len += len(v)
        if cur_len > length:
            return tmp
        tmp.append(item)
    return tmp


def timer(value):
    if not isinstance(value, dict):
        raise TypeError

    sorted_items = sorted(value.items(), key=lambda x: time.strptime(x[0], r"%Y-%m-%d"))
    # 只返回最近一个键值对
    return sorted_items[-1]


env = Environment(
    loader=PackageLoader('baidu_wiki', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True
)
# 注册自定义过滤器
env.filters['limited_items'] = limited_items
env.filters['timer'] = timer


def get_weather_forecast(city_code=101200801):
    r = requests.get(f'http://wthrcdn.etouch.cn/weather_mini?citykey={city_code}')
    tmp = r.json()
    if tmp['status'] != 1000:
        raise ValueError('weather api response error!')
    return tmp['data']


def get_today_history(time_: str = None):
    if time_:
        if not isinstance(time_, str):
            raise TypeError("The month must be an str type!")
        time_ = time.strptime(time_, r"%Y-%m-%d")
    else:
        time_ = time.localtime(time.time())
    r = requests.get(f"http://baike.baidu.com/cms/home/eventsOnHistory/{time_.tm_mon:02d}.json",
                     headers={"user-agent": ''})
    today = r.json()[f"{time_.tm_mon:02d}"][f"{time_.tm_mon:02d}{time_.tm_mday:02d}"]
    # 虽然说取近3年的数据，不过有很小的概率“今天”根本没有这3年的数据，或有BUG ？
    return [(item['year'], re.sub(r"<[^>]+>", "", str(item['title'])).strip('\n')) for item in today]


def get_hot_search():
    """
    爬取当前热搜词条\n
    返回List:[(title,content),(title,content),(title,content)...]
    """
    r = requests.get('https://baike.baidu.com/', headers={"user-agent": ''})
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    today_content_show = soup.find('dl', class_='today content show')
    content = today_content_show.find_all('div', class_='content_cnt')

    def reval(c):
        k, v = [item for item in c.parent.text.split('\n') if item]
        return (k, v)

    return [reval(c) for c in content]


def get_main_content(template_name):
    template = env.get_template(template_name)
    content = template.render(get_hot_search=get_hot_search,
                              get_today_history=get_today_history,
                              get_weather_forecast=get_weather_forecast)
    return content


# 本插件被加载时被调用，提供 List/SendTo/GroupXXX/Stop/Restart 等接口，详见文档第五节
# 提醒：如果本插件设置为启动时自动加载，则本函数将延迟到登录完成后被调用
# bot ： QQBot 对象
def onPlug(bot):
    # 读取配置
    global_conf = bot.conf.pluginsConf["baidu_wiki"]
    try:
        # 对配置项名称进行效验
        if not all(['target' in global_conf, 'templates_path' in global_conf]):
            raise KeyError
    except:
        WARN("BaiduWiki 无效的配置文件！")
    def_conf = {
        'target': [],
        'exit_with_copy_the_message': True,
        'on_exit_show_the_message': True,
    }
    conf = {**def_conf, **global_conf}

    content = get_main_content('main.txt')

    def send_message(groupname, message):
        bl = bot.List('group', groupname)
        if bl:
            b = bl[0]
            bot.SendTo(b, message)

    for tar in conf['target']:
        send_message(tar, content)

    if conf['exit_with_copy_the_message']:
        copy(content)

    if conf['on_exit_show_the_message']:
        tmp = tempfile.TemporaryFile('w', encoding='utf-8', delete=False)
        tmp.write(content)
        tmp.close()
        os.system(f"notepad {tmp.name}")


if __name__ == '__main__':
    print(get_main_content('main.txt'))
