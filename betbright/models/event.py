from betbright.application import app
from betbright.models.model import Model


class Event(Model):
    @property
    def collection(self):
        return app.mongo['event']
