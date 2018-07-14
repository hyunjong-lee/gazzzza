import uuid

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from api.game import GameStatus


game = GameStatus()


class HeaderParser:
    @staticmethod
    def get_header(request, field):
        value = request.META.get(field)
        return value

    @staticmethod
    def register(request):
        nick = get_header(request, 'Nickname')
        guid = uuid.uuid4()


class RegisterView(View):
    def get(self, request):
        nick, guid = HeaderParser.register(request)
        header = {'Guid': guid}
        response = game.register(guid, nick)

        return JsonResponse(response, header=header)


class PingView(View):
    def get(self, request):
        return JsonResponse({})


class ActView(View):
    def get(self, request):
        return JsonResponse({})


class NickView(View):
    def get(self, request):
        return JsonResponse({})
