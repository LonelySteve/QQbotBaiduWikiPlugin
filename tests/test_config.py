import unittest

import baidu_wiki.config as config
from tests import util

qconf = util.FakeQConf({"baidu_wiki": config.QQbotPluginConfig.field})
qbot = util.FakeBotClass(qconf)


class TestConfig(unittest.TestCase):
    def test_instance(self):
        config.QQbotPluginConfig(qbot, "baidu_wiki")
        config.SelfConfig("tmp.log")

    def foo(self,obj, can_set_attr):
        self.assertEqual(obj.target, [])
        self.assertEqual(obj.template_encoding, "utf-8")

        obj.target.append("test 123")
         
        self.assertEqual(obj.target, ["test 123"])
        
        # 测试非法类型赋值
        ex = TypeError if can_set_attr else AttributeError
        with self.assertRaises(ex):
            obj.target = "123123"
        with self.assertRaises(ex):
            obj.template_encoding = 123456
        # 测试正常类型赋值
        if can_set_attr:
            obj.target = []
            obj.template_encoding = "gbk"

    def test_QQbotPluginConfig_attr(self):
        qqbot_conf = config.QQbotPluginConfig(qbot, "baidu_wiki")
        self.foo(qqbot_conf, False)

    def test_SelfConfig_attr(self):
        self_conf = config.SelfConfig("tmp.log")      
        self.foo(self_conf, True)


if __name__ == '__main__':
    unittest.main()
