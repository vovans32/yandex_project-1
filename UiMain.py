from Message import Message
from save_dialog import save_dialog
from send_message_server import send_message_server

import sys
from random import choice
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSizePolicy
from PyQt5.QtWidgets import QPushButton, QScrollBar, QLabel, QLineEdit
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self, users_handles, users_names, dialogs, number_of_users, handle, token):
        super().__init__()

        self.handle = handle
        self.token = token
        self.number_of_users = number_of_users
        self.names_of_users = dict()
        self.names_of_users = users_names
        self.handles_of_users = [*users_handles]
        self.users_btn = dict()
        self.users_showed = 0
        self.user_now = None
        self.dialogs = dialogs
        self.messages_number = 0
        self.initUI()

        self.start()

    def initUI(self):
        uic.loadUi('C:/Program Files (x86)/Messenger/main_window.ui', self)
        self.message_send_button.clicked.connect(self.send_message)
        self.message_vbar = self.messangesScrollArea.verticalScrollBar()
        self.senders_vbar = self.sendersScrollArea.verticalScrollBar()

        self.restyle(0)

    def restyle(self, style):
        # self.setStyleSheet('''
        #  background-color: #323232;''')
        # self.setStyleSheet('''background-color: #A9B7C6;''')
        self.setStyleSheet('''background-color: rgb(210, 230, 255)''')
        self.message_send_button.setStyleSheet('''
         background-color: #BED6FF;
         border-style: outset;
         border-width: 2px;
         border-radius: 10px;
         min-width: 10em;
         padding: 6px;''')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.send_message()
        if event.key() == Qt.Key_Return:
            self.send_message()

    def clear_users(self):
        while self.senders.count():
            child = self.senders.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def clear_messages(self):
        while self.messages.count():
            child = self.messages.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def scroll_message_bar(self, n):
        for _ in range(n):
            QApplication.processEvents()
        self.message_vbar.setSliderPosition(self.message_vbar.maximum())
        # self.message_vbar.setValue(self.message_vbar.maximum())
        # self.message_vbar.setSliderDown(True)

    def scroll_senders_bar(self):
        QApplication.processEvents()
        self.senders_vbar.setSliderPosition(0)

    def generate_message(self, sender):
        text = ''.join([choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(10)])
        return Message(text, sender, 1572499975)

    def generate_dialog(self, user):
        if user not in self.dialogs:
            self.dialogs[user] = [self.generate_message(
                sender=choice([self.names_of_users[self.handle], self.names_of_users[user]]))
                for _ in range(10)]

    def send_message(self):
        if not self.user_now:
            return
        message = Message(self.messange_input.text(), self.names_of_users[self.handle])
        self.add_message(message)
        if self.dialogs:
            self.dialogs[self.user_now].append(message)
        else:
            self.dialogs[self.user_now] = [message]

        # save_dialog(self.user_now, self.dialogs[self.user_now])

        send_message_server(self.handle, self.token, self.user_now, message.text)

        self.messange_input.clear()

        self.sort_users()

    def add_message(self, text):
        if text.sender == self.names_of_users[self.handle]:
            self.messages.addWidget(text.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignRight)

        else:
            self.messages.addWidget(text.text_to_show(), self.messages_number, 0,
                                    alignment=Qt.AlignLeft)
        self.messages_number += 1

        self.scroll_message_bar(2)

    def show_new_user(self, user):
        btn = QPushButton(self.names_of_users[user])
        btn.clicked.connect(self.open_new_dialog)

        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn.setMinimumHeight(150)
        btn.setStyleSheet('background-color: #BED6FF; font-size: 35px')
        # self.senders.addWidget(btn, self.users_showed, 0, alignment=Qt.AlignVCenter)
        self.senders.addWidget(btn)
        self.users_btn[btn] = user

        self.users_showed += 1

        self.generate_dialog(user)

    def open_new_dialog(self):
        self.clear_messages()

        sender = self.users_btn[self.sender()]
        self.user_now = sender
        for message in self.dialogs[sender]:
            self.add_message(message)

        self.scroll_message_bar(0)

        # self.messange_input.setCursorPosition(0)

        save_dialog(sender, self.dialogs[sender])

    def sort_users(self):
        self.clear_users()
        self.handles_of_users.sort(key=lambda l: float(-self.dialogs[l][-1].int_time))
        self.start()
        self.scroll_senders_bar()

    def start(self):
        for i in range(self.number_of_users):
            self.show_new_user(self.handles_of_users[i])


def main(users_handles, users_names, dialogs, number_of_users, handle, token):
    try:
        app = QApplication(sys.argv)
        ex = MyWidget(users_handles, users_names, dialogs, number_of_users, handle, token)
        ex.show()
        sys.exit(app.exec_())
    finally:
        open('C:/Program Files (x86)/Messenger/data', 'w')

