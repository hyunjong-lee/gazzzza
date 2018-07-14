from copy import deepcopy
import datetime


class GameStatus:

    def __init__(self):
        self.users = {}
        self.actions = {}
        self.base_tick = datetime.datetime.now()
        self.turn = 1
        self.mp_map = {'1': 40, '2': 10, '3': 5}
        self.demage_map = {'2': 10, '3': 5}

    def get_remain_time(self):
        diff = self.base_tick - datetime.datetime.now()
        rem_time = diff.total_seconds() + 5
        return rem_time

    def do_action(self):
        execute = {}
        actions = deepcopy(self.actions)
        for k in actions:
            act = actions.get(k, {})
            action = act.get('action')
            target = act.get('target_guid')
            if not action:
                continue

            # user check
            if k not in self.users:
                continue

            # action check
            if not action:
                continue

            # MP check
            status = self.users[k]
            req_mp = self.mp_map[action]
            if status['mp'] < req_mp:
                continue

            # target check
            if action in ['2', '3']:
                if not target:
                    continue
                if target not in self.users:
                    continue

            execute[k] = {
                'mp': self.mp_map[action],
                'action': action,
                'target': target,
            }

        print(execute)

        for k in execute:
            a = execute[k]['action']
            t = execute[k]['target']
            if a in ['1']:
                continue

            if a not in ['2', '3']:
                continue

            if a in ['2', '3']:
                if t in execute and execute[t]['action'] == '1':
                    continue
                if a == '2' and t in execute:
                    if execute[t]['action'] == '3':
                        continue

                self.users[t]['hp'] -= self.demage_map[a]
                if self.users[t]['hp'] < 0:
                    self.users[t]['death'] += 1
                    self.users[t]['hp'] = 100
                    self.users[t]['mp'] = 100

        for k in execute:
            a = execute[k]['action']
            self.users[k]['mp'] -= execute[k]['mp']

        for k in self.users:
            self.users[k]['mp'] += 3
            if self.users[k]['mp'] > 100:
                self.users[k]['mp'] = 100


    def on_tick(self):
        self.do_action()
        self.turn += 1
        self.base_tick = datetime.datetime.now()

    def check_tick(self):
        rem_time = self.get_remain_time()
        if rem_time <= 0:
            return True
        return False

    def wrap_user(self, guid, idx):
        val = self.users[guid]
        ret = {}
        ret['user%d-guid' % idx] = guid
        ret['user%d-hp' % idx] = val['hp']
        ret['user%d-mp' % idx] = val['mp']
        ret['user%d-death' % idx] = val['death']
        ret['user%d-nickname' % idx] = '%s' % val['nick']
        return ret

    def get_my_act(self, guid):
        ret = {}
        ret['guid'] = guid
        act = self.actions.get(guid, {})
        if 'action' in act:
            ret['selected-act'] = act['action']
        if 'target_guid' in act:
            ret['selected-target'] = act['target_guid']
        return ret

    def get_game(self, my_guid):
        if self.check_tick():
            self.on_tick()

        ret = {
            'turn': self.turn,
            'turn-remain-time': self.get_remain_time(),
        }
        ret.update(self.get_my_act(my_guid))

        for idx, guid in enumerate(self.users):
            user = self.wrap_user(guid, idx)
            ret.update(user)
        return ret

    def register(self, guid, nick):
        user = {'guid': guid,
                'nick': nick,
                }
        if guid not in self.users:
            user['hp'] = 100
            user['mp'] = 100
            user['death'] = 0
        self.users[guid] = user

        return self.get_game(guid)

    def ping(self, guid):
        return self.get_game(guid)

    def act(self, guid, target_guid, action):
        my_act = self.actions.get(guid, {})
        if target_guid:
            my_act['target_guid'] = target_guid
        if action:
            my_act['action'] = str(action)
        self.actions[guid] = my_act

        return self.get_game(guid)

    def nick(self, guid, nick):
        return self.get_game(guid)
