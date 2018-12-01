import os
import random
import re
import tempfile
import time

import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader
from pyperclip import copy
from qqbot import qqbotsched


def legal_text(value, n1=2, n2=5):
    # 这里规定了微语字节数的最大值
    bytes_length = 720

    if not callable(value):
        raise TypeError
    for i in range(n1, 0, -1):
        for j in range(n2, 0, -1):
            tmp_str = value(i, j)
            bs = tmp_str.encode("utf-8")
            if len(bs) < bytes_length:
                return tmp_str


def timer(value):
    if not isinstance(value, dict):
        raise TypeError
    # 这里先过滤掉未来的日期
    time_now = time.localtime(time.time())
    recent_items = [(k, v) for k, v in value.items() if time.strptime(k, r"%Y-%m-%d") <= time_now]
    # 然后对最近的日期活动项进行排序
    sorted_items = sorted(recent_items, key=lambda x: x[0])
    # 只返回最近一个键值对
    return sorted_items[-1]


env = Environment(
    loader=PackageLoader('baidu_wiki', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True
)
# 注册自定义过滤器
env.filters['legal_text'] = legal_text
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


@qqbotsched(hour='22', minute='30')
def sched_weiyu_task(bot):
    # 读取配置
    global_conf = bot.conf.pluginsConf["baidu_wiki"]
    def_conf = {
        'target': [],
        'template_encoding': 'utf-8',
        'exit_with_copy_the_message': False,
        'on_exit_show_the_message': False,
        # 随机发送时间间隔支持秒级随机数表示
        'send_interval': [],
        # 调试模式
        'debug': False,
    }
    conf = {**def_conf, **global_conf}
    is_debug = conf['debug']

    def debug(msg):
        if is_debug:
            print('=' * 72)
            print(msg)
            print('=' * 72)

    env.loader = PackageLoader('baidu_wiki', encoding=conf['template_encoding'])
    content = get_main_content('main.jinja2')

    def send_message(groupname, message):
        bl = bot.List('group', groupname)
        if bl:
            b = bl[0]
            bot.SendTo(b, message)

    send_interval = conf['send_interval']
    if isinstance(send_interval, (int, float)):
        send_interval = [send_interval]

    debug("发送间隔：" + ', '.join([str(i) for i in send_interval]))

    for tar in conf['target']:
        if send_interval:
            sec = random.choice(send_interval)
            debug(f"休息秒数：{sec}")
            time.sleep(sec)

        debug(f"发送对象：{tar} \n 发送内容：\n {content}")
        if not is_debug:
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
