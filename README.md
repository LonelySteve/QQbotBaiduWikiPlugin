# QQbotBaiduWikiPlugin
> 这是一个基于qqbot开发的插件，用于发送长江大学百度百科俱乐部的微语

## 如何开始

这是一个基于[qqbot](https://github.com/pandolia/qqbot)开发的插件，因此，在开始正式使用前，请按照该项目的说明配置好相应的环境。

本项目在windows 10 1803上的Python3.6.6环境中成功运行：

* [Python 3.6+](https://www.python.org/)

你需要安装的所有依赖项（以下依赖项均可使用pip进行快捷安装）：

* [qqbot](https://github.com/pandolia/qqbot)
* [Jinja2](http://jinja.pocoo.org/)
* [requests](http://www.python-requests.org/en/master/)
* [bs4](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)
* [pyperclip](https://github.com/asweigart/pyperclip)

### 对qqbot进行配置

本插件的配置由qqbot提供，插件首次运行时，必须进行配置。

以下是qqbot配置文件的关键部分：

```
# 该文件通常的路径为：
# C:\Users\[User Name]\.qqbot-tmp\v2.3.conf
# 如果没有该文件或目录，请尝试先运行一次qqbot
{

    # QQBot 的配置文件
    # 使用 qqbot -u somebody 启动程序时，依次加载：
    #     根配置 -> 默认配置 -> 用户 somebody 的配置 -> 命令行参数配置
    # 使用 qqbot 启动程序时，依次加载：
    #     根配置 -> 默认配置 -> 命令行参数配置
    
    # 用户 somebody 的配置 （特别指出的是，由于一般人机器上并不会有somebody这样的用户名，因此在该配置下，做出的任何配置，可能都不会对qqbot产生影响！）
    "somebody" : {
        
        # QQBot-term （HTTP-API） 服务器端口号（该服务器监听 IP 为 127.0.0.1 ）
        # 设置为 0 则不会开启本服务器（此时 qq 命令和 HTTP-API 接口都无法使用）。
        "termServerPort" : 8188,
        
        # 二维码 http 服务器 ip，请设置为公网 ip 或空字符串
        "httpServerIP" : "",
        
        # 二维码 http 服务器端口号
        "httpServerPort" : 8189,
        
        # 自动登录的 QQ 号
        "qq" : "3497303033",
        
        # 接收二维码图片的邮箱账号
        "mailAccount" : "3497303033@qq.com",
        
        # 该邮箱的 IMAP/SMTP 服务授权码
        "mailAuthCode" : "feregfgftrasdsew",
        
        # 是否以文本模式显示二维码
        "cmdQrcode" : False,
    
        # 显示/关闭调试信息
        "debug" : False,

        # QQBot 掉线后自动重启
        "restartOnOffline" : False,
        
        # 在后台运行 qqbot ( daemon 模式)
        "daemon": False,
        
        # 完成全部联系人列表获取之后才启动 QQBot 
        "startAfterFetch" : False,
        
        # 插件目录
        "pluginPath" : ".",
        
        # 启动时需加载的插件
        "plugins" : [],
        
        # 插件的配置（由用户自定义）
        "pluginsConf" : {}
    
    },
    
    # 可以在 默认配置 中配置所有用户都通用的设置
    # 这是对机器上所有用户都生效的设置项，请优先设置此配置！
    # 可配置项和上面的somebody中的一致
    "默认配置" : {
        "qq" : "123456789",
        "pluginPath" : "",
        "plugins" : [
            'qqbot.plugins.sampleslots',
            'qqbot.plugins.schedrestart',
            # 建议填入本插件名，让qqbot在启动时自动加载本插件
            "baidu_wiki"  
        ],
	    "pluginsConf" : {
	        'qqbot.plugins.schedrestart': '8:00',
            # **在此处配置本插件**
            "baidu_wiki":{
                # 【必须】这里可以选择群发目标（目前只支持QQ群）
                "target": ["1群名"，"2群名"],
                # 模板编码，默认为utf-8
                'template_encoding': 'utf-8',
                # 在插件退出时，将构建内容复制到剪切板中。默认为开启状态
                "exit_with_copy_the_message":True,
                # 在插件退出时，将构建内容输出至临时文件中，并用记事本打开呈现。默认为开启状态
                'on_exit_show_the_message': True,
                # 消息发送间隔时间，默认为空，即不使用间隔时间，另：间隔时间将随机选取
                'send_interval':[3,4,5],
                # 是否开启调试模式，在调试模式下，消息将不会真正发出
                'debug':False,
            }
	    }
    }
}

```

### 将本插件连同模板复制到qqbot插件目录下

目前有两种方式下载本插件的源码压缩包：

* 直接在页面中通过点击绿色的**Clone or download**按钮来**Download Zip**
* 通过[releases](https://github.com/LonelySteve/QQbotBaiduWikiPlugin/releases)下载zip or tar.gz

**qqbot插件目录通常为 C:\\Users\\[User Name]\\.qqbot-tmp\\plugins**

将压缩包进行解压，其中你必须复制到qqbot插件目录的文件或文件夹：

* baidu_wiki.py
* templates

### 一切就绪，使用qqbot即可正常工作

## 关于Jinja2

>Jinja2是python的一种模板语言，以Django的模板语言为原本，和Django的模板语言有很多相似之处，同时Jinja本身也是一种系统的、完整的Python模板语言。

关于Jinja2的语法及注意事项请参考[官方文档](http://jinja.pocoo.org/docs/2.10/)

依托于Jinja2强大的功能，结合本模板提供的过滤器和相关函数，用户可以轻而易举地定义自己期望的百度百科微语。

### 本插件提供的过滤器与函数

以下是本插件提供的自定义过滤器：

|过滤器|描述|
|:-------|:--|
|legal_text(value, n1=2, n2=5)|通过对指定函数或其它可调用对象（value）中传入循环变量，控制其生成的字符串字节数不多于720，并返回该字符串，失败将返回 None|
|timer|传入一个字典，该字典的键值表示日期，例如："2018-07-12"，将返回日期最近（注意不是**最新**）的键值对|

_在v0.0.1版本中timer将返回最新的日期的键值对，而不是最近的日期，此问题在v0.0.2版本中得到修复_

以下是本插件提供给模板使用的函数：

|函数|返回值示例|描述|
|:--|:--|:--|
|get_hot_search()|[(title,content),(title,content),(title,content)...]|获取百度百科当前热搜词条（不完全，但已经够用了）|
|get_today_history(time_: str = None)|[(year,title),(year,title),(year,title)...]|获取历史上的今天上的事件，可以指定字符串表示的日期，例如："2018-07-12"|
|get_weather_forecast(city_code=101200801)|见下|获取天气预报，默认城市为荆州|

其中get_weather_forecast函数的返回值格式较为复杂，以下是示例：

```

{
    "data": {
        "yesterday": {
            "date": "19日星期三",
            "high": "高温 33℃",
            "fx": "南风",
            "low": "低温 22℃",
            "fl": "<![CDATA[3-4级]]>",
            "type": "多云"
        },
        "city": "荆州",
        "forecast": [
            {
                "date": "20日星期四",
                "high": "高温 26℃",
                "fengli": "<![CDATA[3-4级]]>",
                "low": "低温 20℃",
                "fengxiang": "北风",
                "type": "小雨"
            },
            {
                "date": "21日星期五",
                "high": "高温 23℃",
                "fengli": "<![CDATA[3-4级]]>",
                "low": "低温 19℃",
                "fengxiang": "西北风",
                "type": "小雨"
            },
            {
                "date": "22日星期六",
                "high": "高温 27℃",
                "fengli": "<![CDATA[<3级]]>",
                "low": "低温 17℃",
                "fengxiang": "东北风",
                "type": "多云"
            },
            {
                "date": "23日星期天",
                "high": "高温 27℃",
                "fengli": "<![CDATA[<3级]]>",
                "low": "低温 18℃",
                "fengxiang": "东北风",
                "type": "多云"
            },
            {
                "date": "24日星期一",
                "high": "高温 26℃",
                "fengli": "<![CDATA[<3级]]>",
                "low": "低温 17℃",
                "fengxiang": "北风",
                "type": "阴"
            }
        ],
        "ganmao": "各项气象条件适宜，无明显降温过程，发生感冒机率较低。",
        "wendu": "23"
    },
    "status": 1000,
    "desc": "OK"
}

```

### 关于模板

模板所在路径暂时不可改变，即 **.\templates\\*.jinja2**

_如果出现编码问题，请尝试修改qqbot的配置文件中本插件的模板编码设置项_

## 版本变更

### v0.0.3

* 新增：随机发送消息时间间隔设置
* 新增：Debug 模式
* 修正：解耦 main.txt 模板，新的模板文件扩展名修改为 .jinja2

### v0.0.2

* 新增：现在可以设置模板的编码了
* 修正：无法确保生成的微语的字节数不超标的问题
* 修正：timer过滤器返回的不是最近的键值对的问题

### v0.0.1

* 基本架构搭建完成
