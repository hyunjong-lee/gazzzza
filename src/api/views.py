import uuid

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from api.game import GameStatus


game = GameStatus()


class HeaderParser:
    @staticmethod
    def get_header(request, field):
        value = request.META.get('HTTP_' + field)
        return value


class RegisterView(View):
    def get(self, request):
        nick = HeaderParser.get_header(request, 'NICKNAME')
        print(nick)
        '''
        if nick:
            nick = nick.encode('iso-8859-1').decode('utf-8')
        print(nick)
        '''
        guid = str(uuid.uuid4())
        ret = game.register(guid, nick)

        response = JsonResponse(ret)
        response['Guid'] = guid
        return response


class PingView(View):
    def get(self, request):
        nick = HeaderParser.get_header(request, 'NICKNAME')
        guid = HeaderParser.get_header(request, 'GUID')
        if guid not in game.users:
            game.register(guid, nick)
        ret = game.ping(guid)
        return JsonResponse(ret)


class ActView(View):
    def get(self, request):
        guid = HeaderParser.get_header(request, 'GUID')
        target_guid = HeaderParser.get_header(request, 'TARGETGUID')
        action = HeaderParser.get_header(request, 'ACTION')
        ret = game.act(guid, target_guid, action)
        return JsonResponse(ret)


class NickView(View):
    def get(self, request):
        return JsonResponse({})
