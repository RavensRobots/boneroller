class UserData(object):

    def __init__(self):
        self.locales = {}

    def save_locale(self, user_id, locale):
        self.locales[user_id] = locale

    def get_locale(self, user_id):
        if user_id in self.locales:
            return self.locales[user_id]
        else:
            return "EN"


user_data = UserData()
sl = user_data.save_locale
gl = user_data.get_locale
