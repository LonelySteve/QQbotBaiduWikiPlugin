import collections
import exceptions

import yaml

import logger


def _isfilelike(f):
    """ 
    Check if object 'f' is readable file-like  
    that it has callable attributes 'read' , 'write' and 'closer' 
    """
    try:
        if isinstance(
                getattr(f, "read"),
                collections.Callable) and isinstance(
                getattr(f, "write"),
                collections.Callable) and isinstance(
                getattr(f, "close"),
                collections.Callable):
            return True
    except AttributeError:
        pass
    return False

class QQbotPluginConfig(object):

    field = {**BaseConfig.field, **{
        "target": [],
        "template_encoding": "utf-8",
        "send_interval": [],
        "debug": False
    }}

    def __init__(self, bot, plugin_name):
        self.PluginConfig = bot.conf.pluginsConf[plugin_name]

        for k, v in self.PluginConfig.items():
            if k not in QQbotPluginConfig.field:
                logger.warn(f"{plugin_name}: {k} 配置选项不受支持！")
            setattr(self, k, property(fget=(lambda v: lambda self: v)(v)))

        for k, v in QQbotPluginConfig.field:
            if not hasattr(self, k):
                setattr(self, k, property(fget=(lambda v: lambda self: v)(v)))


class SelfConfig(QQbotPluginConfig):
    field = {**QQbotConfig.field, **{
        "_today_task_has_done": False,
    }}

    def __init__(self, fp, encoding='utf-8'):
        if isinstance(fp, str):
            fp = open(fp, "w+", encoding=encoding)
        if not _isfilelike(fp):
            raise ValueError("fp must be file-like object or file path str!")
        self.fp = fp
        # 对类的域进行一次浅拷贝到对象的域中
        self.field = dict(SelfConfig.field)

        def getter_producer(k, v):
            def get_val(self):
                return self.field.get(k, v)
            return get_val

        def setter_producer(k, v):
            if k not in SelfConfig.field:
                logger.warn(f"{k} 配置选项不受支持！")

            def set_val(self, value):
                if not isinstance(value, type(v)):
                    raise TypeError(f"{k} excepted " + str(type(v)))
                self.field[k] = v
            return set_val

        data = yaml.load(fp)

        for k, v in data.items():
            setattr(self, k, property(fget=getter_producer(k, v), fset=setter_producer(k, v)))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.save()

    def save(self):
        yaml.dump(self.field, self.fp)