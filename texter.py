class Texter:

    users = dict()

    def add_users(self, user_id, locale):
        self.users[user_id] = locale


texter = Texter()


def some_method(some_shit):
    return some_shit
