from ui.login_window_ui import Ui_MainWindow as LoginWindow
from ui.notes_ui import Ui_MainWindow as NotesMainWindow
from modules.encoder import encoder

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
import sqlite3
import sys
import ast
# Из информации о пользователе

is_login = False
# Переменная, отвечающая за войти/зарегистрироваться
process = "login"
current_user = None


class Authentication(QMainWindow, LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Авторизация')
        self.setFixedSize(600, 741)
        self.setWindowIcon(QIcon('images/main_icon.ico'))
        self.start.clicked.connect(self.ExecuteNotes)
        self.go_login.clicked.connect(self._login_form)
        self.go_reg.clicked.connect(self._registration_form)
        self.messagebox = QMessageBox(self)
        self.new_login.hide()
        self.password_1.hide()
        self.password_2.hide()

    def _login_form(self):
        global process
        if process != 'login':
            self.new_login.hide()
            self.password_1.hide()
            self.password_2.hide()
            self.login.show()
            self.password.show()
            process = 'login'

    def _login(self):
        with sqlite3.connect(database="database/database.sqlite3") as db:
            cursor = db.cursor()
            req = cursor.execute(
                f'SELECT * FROM USERDATA WHERE LOGIN = "{self.login.toPlainText()}"')
        try:
            name, password, data = [item for item in req][0]
            if self.login.toPlainText() == name and encoder(self.password.toPlainText()) == password:
                "TODO: Сделать логирование"
                global current_user
                current_user = name[:]
                start_notes()

            else:
                self.messagebox.setText(
                    'Проверьте правильность ввода логина или пароля.')
                self.messagebox.show()
        except Exception as e:
            self.messagebox.setText(
                'Возникла ошибка при попытке войти в систему. Скорее всего, данного аккаунта не существует. Детали: {}'.format(e))
            self.messagebox.show()

    def _registration_form(self):
        global process
        if process != 'registration':
            self.login.hide()
            self.password.hide()
            self.new_login.show()
            self.password_1.show()
            self.password_2.show()
            process = 'registration'

    def _registration(self):
        with sqlite3.connect(database="database/database.sqlite3") as db:
            cursor = db.cursor()
            req = cursor.execute(
                f'SELECT * FROM USERDATA WHERE LOGIN = "{self.new_login.toPlainText()}"')
            try:
                user_info = [item for item in req]
                # print(user_info, self.login.toPlainText(), self.password.toPlainText())
                if not user_info:
                    if len(self.new_login.toPlainText()) < 5:
                        self.messagebox.setText(
                            'Длина логина не может быть меньше 5 символов!')
                        self.messagebox.show()
                    elif len(self.password_1.toPlainText()) < 8:
                        self.messagebox.setText(
                            'Длина пароля меньше 8 символов!')
                        self.messagebox.show()
                    elif self.password_1.toPlainText() != self.password_2.toPlainText():
                        self.messagebox.setText('Пароли не совпадают!')
                        self.messagebox.show()
                    else:

                        self.data = {

                            "name": f"{self.new_login.toPlainText()}",
                            "2": {"title": "нет заголовка", "description": "нет описания", 'being': False},
                            "1": {"title": "нет заголовка", "description": "нет описания", 'being': False},
                            "3": {"title": "нет заголовка", "description": "нет описания", 'being': False},
                            "4": {"title": "нет заголовка", "description": "нет описания", 'being': False},
                            "5": {"title": "нет заголовка", "description": "нет описания", 'being': False},
                            "6": {"title": "нет заголовка", "description": "нет описания", 'being': False}

                        }

                        cursor.execute(
                            f'INSERT INTO USERDATA(LOGIN, PASSWORD, DATA) VALUES("{self.new_login.toPlainText()}", "{encoder(self.password_1.toPlainText())}", "{self.data}") ')
                        db.commit()
                        self.messagebox.setText(
                            'Аккаунт успешно создан! Войдите под своей учетнной записи. ')
                        self.messagebox.show()
                else:
                    self.messagebox.setText(
                        'Такой пользователь уже существует!')
                    self.messagebox.show()

            except Exception as e:
                self.messagebox.setText(e)
                self.messagebox.show()

    def ExecuteNotes(self):
        if process == 'login':
            self._login()
        elif process == 'registration':
            self._registration()


class Notes(QMainWindow, NotesMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.cb_1.clicked.connect(self.edit_menu)
        self.cb_2.clicked.connect(self.edit_menu)
        self.cb_3.clicked.connect(self.edit_menu)
        self.cb_4.clicked.connect(self.edit_menu)
        self.cb_5.clicked.connect(self.edit_menu)
        self.cb_6.clicked.connect(self.edit_menu)
        self.changebox.hide()
        self.save_new.clicked.connect(self.make_an_note)

    def _hide_mainboard(self):
        self.stack_1.hide()
        self.stack_2.hide()
        self.stack_3.hide()
        self.stack_4.hide()
        self.stack_5.hide()
        self.stack_6.hide()

    def _show_mainboard(self):
        self.stack_1.show()
        self.stack_2.show()
        self.stack_3.show()
        self.stack_4.show()
        self.stack_5.show()
        self.stack_6.show()
        self.repaint()

    def edit_menu(self):
        self.number = self.sender().objectName().split('_')[-1]
        self._hide_mainboard()
        self.label_mainwindow_name.setText('Меню редактирования')
        self.label_mainwindow_name.setFont(QFont('Comic Sans MS', 30))
        self.label_mainwindow_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.changebox.show()
        with sqlite3.connect(database="database/database.sqlite3") as db:
            cursor = db.cursor()
            req = cursor.execute(
                f'SELECT * FROM USERDATA WHERE LOGIN = "{current_user}"')

            data = [item for item in req][0][-1]
            data = ast.literal_eval(data)

        self.title.setPlainText(data[self.number]['title'])
        self.description.setPlainText(data[self.number]['description'])

    def make_an_note(self):
        global current_user
        """процесс сохранения новой информации и внесение её в БД"""
        print(self.number)
        self.changebox.hide()
        self._show_mainboard()
        self.label_mainwindow_name.setText('Memorandum')
        self.label_mainwindow_name.setFont(QFont('Comic Sans MS', 30))
        self.label_mainwindow_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        with sqlite3.connect(database="database/database.sqlite3") as db:
            cursor = db.cursor()
            req = cursor.execute(
                f'SELECT * FROM USERDATA WHERE LOGIN = "{current_user}"')

            data = [item for item in req][0][-1]
            data = ast.literal_eval(data)

            data[self.number]['title'] = self.title.toPlainText()
            data[self.number]['description'] = self.description.toPlainText()
            print(data)
            print(current_user)
            cursor.execute(
                f'UPDATE USERDATA SET DATA = "{data}" WHERE LOGIN = "{current_user}"')
            db.commit()
        self.init_user_interface()

    def init_user_interface(self):
        with sqlite3.connect(database="database/database.sqlite3") as db:
            cursor = db.cursor()
            req = cursor.execute(
                f'SELECT * FROM USERDATA WHERE LOGIN = "{current_user}"')

            data = [item for item in req][0][-1]
            data = ast.literal_eval(data)

        self.stack_1.setTitle(data['1']['title'])
        self.lt_1.setText(data['1']['description'])
        self.stack_2.setTitle(data['2']['title'])
        self.lt_2.setText(data['2']['description'])
        self.stack_3.setTitle(data['3']['title'])
        self.lt_3.setText(data['3']['description'])
        self.stack_4.setTitle(data['4']['title'])
        self.lt_4.setText(data['4']['description'])
        self.stack_5.setTitle(data['5']['title'])
        self.lt_5.setText(data['5']['description'])
        self.stack_6.setTitle(data['6']['title'])
        self.lt_6.setText(data['6']['description'])
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex1 = Authentication()
    ex2 = Notes()
    ex1.show()

    def start_notes():
        ex2.show()
        ex2.init_user_interface()
        ex1.close()

    app.exec()
