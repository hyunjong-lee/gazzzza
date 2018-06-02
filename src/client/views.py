from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

import json
import random


Users = {}
Cards = {}
Targets = {}
HP = {}
# Create your views here.


def get_session(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    name = request.GET.get('name')
    return {
        'ip': ip,
        'name': name,
        'key': ip + name,
    }


def get_card(request):
    return request.GET.get('card')


def get_target(request):
    return request.GET.get('target')


def interpret_card(card):
    if card == 'r':
        return '방어'
    if card == 'g':
        return '펜'
    if card == 'b':
        return '칼'

    return '아직 안고름ㅋ'


def interpret_target(target):
    global Targets
    global Cards
    global HP
    if target in Users:
        return Users[target]['name']
    return '아직 안고름ㅋ'


def get_target_key(target):
    global Targets
    global Cards
    global HP
    if target in Users:
        return Users[target]['key']
    return ''


def demage(me, you):
    global Targets
    global Cards
    global HP
    if Cards[you] == 'r':
        return

    c = Cards[me]
    if c == 'g':
        HP[you] = HP[you] - 20
    if c == 'b':
        HP[you] = HP[you] - 10


def on_tick():
    global Targets
    global Cards
    global HP

    for me in Targets:
        you = Targets.get(me)
        if not you:
            continue
        if Cards[me] == 'r':
            continue
        if HP[me] < 0:
            continue

        # g 칼
        # b 펜
        if Targets[you] == me:
            if Cards[you] == 'r':
                continue
            elif Cards[me] == Cards[you]:
                demage(me, you)
            elif Cards[me] == 'b' and Cards[you] == 'g':
                demage(me, you)
        else:
            demage(me, you)
    Cards = {}
    Targets = {}


class AdminView(View):
    def get(self, request):
        template_name = 'admin.html'
        tick = request.GET.get('tick')
        if tick:
            on_tick()

        return render(request,
                      template_name,
                      {
                          'users': json.dumps(Users),
                          'targets': json.dumps(Targets),
                          'cards': json.dumps(Cards),
                          'hps': json.dumps(HP),
                      })


class ClientView(View):
    def get(self, request):
        template_name = 'client.html'
        s = get_session(request)
        Users[s['key']] = s
        Cards[s['key']] = get_card(request)
        Targets[s['key']] = get_target(request)
        targets = [k for k in Users.values()
                   if k['key'] != s['key'] and HP[k['key']] > 0]

        if s['key'] not in HP:
            HP[s['key']] = 100


        hps = {Users[k]['name']: HP[k] for k in HP}
        data = {
            'name': Users[s['key']]['name'],
            'key': Users[s['key']]['key'],
            'hp': HP[s['key']],
            'hps': hps,
            'card': interpret_card(Cards[s['key']]),
            'target': interpret_target(Targets[s['key']]),
            'target_key': get_target_key(Targets[s['key']]),
            'targets': targets,
        }
        return render(request, template_name, data)


class EnterView(View):
    def get(self, request):
        template_name = 'enter.html'
        return render(request, template_name, {})
