from . import config


class Controller():

    def __init__(self, trigger: str):
        self.config = config


    def test(self):
        print(self.config.PARAMS)

    def hi(self):
        print('hi')
