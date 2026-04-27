from ninja import ModelSchema

from lobby.models import Lobby


class LobbySchema(ModelSchema):
    class Meta:
        model = Lobby
        fields = "__all__"