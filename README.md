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
                # 【必须】模板路径（未实现）
                "templates_path":[]
                # 在插件退出时，将构建内容复制到剪切板中。默认为开启状态
                "exit_with_copy_the_message":True,
                # 在插件退出时，将构建内容输出至临时文件中，并用记事本打开呈现。默认为开启状态
                'on_exit_show_the_message': True,
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

待填坑。。。