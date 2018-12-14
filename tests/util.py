class FakeQConf(object):
    def __init__(self, plugs_conf):
        self.pluginsConf = plugs_conf


class FakeBotClass(object):
    def __init__(self, fakeQConf):
        self.conf = fakeQConf
