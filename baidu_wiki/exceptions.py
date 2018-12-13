class QQbotBaiduWikiPluginError(Exception):
    pass


class ConfigError(QQbotBaiduWikiPluginError):
    pass


class ConfigItemTypeError(ConfigError, TypeError):
    pass


class ConfigItemValueError(ConfigError, ValueError):
    pass


class ConfigFileError(ConfigError):
    pass


# class ConfigFileNotFoundError(ConfigFileError):
#     pass


class ConfigFileSyntaxError(ConfigError):
    pass


def funcname(parameter_list):
    pass
