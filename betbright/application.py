from sanic import Sanic

from betbright.config import settings


class Application(Sanic):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config.update(settings)

    def run(self, *args, **kwargs):
        self.config.app.update(kwargs)
        super().run(*args, **self.config.app)


app = Application()
