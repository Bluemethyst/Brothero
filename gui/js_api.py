from convert import translate_csv


class BrotheroJSApi():
    def log(self, message):
        print(message)

    def convert(self, text):
        return translate_csv(text)
