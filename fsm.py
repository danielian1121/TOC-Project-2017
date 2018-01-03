from transitions.extensions import GraphMachine
import time

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def on_enter_user(self, update):
        update.message.reply_text("There are three functions to use\n1.[echo] it can repeat the word you type in\n2.[time] it can tell you what time it is\n3.[count] it can count backwards\nYou just type what function you want")
    def is_going_to_time(self, update):
        text = update.message.text
        return text.lower() == 'time'

    def is_going_to_notice(self, update):
        text = update.message.text
        return text.lower() == 'echo'

    def on_enter_notice(self, update):
        update.message.reply_text("You can type any word!")
        update.message.reply_text("If you want to finish, type [go back]")
        self.going_to_echo(update)

    def is_going_to_count(self, update):
        text = update.message.text
        return text.lower() == 'count'

    def is_going_to_user(self, update):
        text = update.message.text
        return text.lower() == 'go back'

    def is_going_to_start_count(self, update):
        text = update.message.text
        return text.isnumeric()

    def is_going_to_repeat(self, update):
        text = update.message.text
        return text != 'go back'

    def what_time(self,update):
        localtime = time.asctime( time.localtime(time.time()) )
        update.message.reply_text(localtime)

    def on_enter_time(self, update):
        self.what_time(update)
        self.go_back(update)

    def echo(self,update):
        text = update.message.text
        update.message.reply_text(text)

    def on_enter_repeat(self, update):
        self.echo(update)
        self.repeat_back(update)
        
    def start(self,update):
        second = int(update.message.text)
        while 1:
            time.sleep(1)
            if second==1:
                break
            else:
                second = second - 1
                update.message.reply_text(second)

    def on_enter_start_count(self, update):
        update.message.reply_text(update.message.text)
        self.start(update)
        self.go_back(update)

    def on_enter_count(self, update):
        update.message.reply_text("The seconds are?")

