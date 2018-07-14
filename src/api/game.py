import datetime


class GameStatus:

    def __init__(self):
        self.users = {}
        self.actions = {}
        self.base_tick = datetime.datetime.now()
        self.turn = 1

    def on_tick(self):
        pass

    def check_tick(self):
        return False

    def wrap_user(self, guid, idx):
        val = self.users[guid]
        ret = {}
        ret['user%d-guid' % idx] = guid
        ret['user%d-hp' % idx] = val['hp']
        ret['user%d-mp' % idx] = val['mp']
        ret['user%d-nickname' % idx] = val['nick']
        return ret

    def get_my_act(self, guid):
        ret = {}
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
            'turn-remain-time': 1.2,
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
        self.users[guid] = user

        return self.get_game(guid)

    def ping(self, guid):
        return self.get_game(guid)

    def act(self, guid, target_guid, action):
        my_act = self.actions.get(guid, {})
        if target_guid:
            my_act['target_guid'] = target_guid
        if action:
            my_act['action'] = action
        self.actions[guid] = my_act

        return self.get_game(guid)

    def nick(self, guid, nick):
        return self.get_game(guid)
