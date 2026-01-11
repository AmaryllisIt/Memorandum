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
        except Exception:
            self.messagebox.setText(
                'Возникла ошибка при попытке войти в систему. Скорее всего, данного аккаунта не существует')
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
                            "2": {"title": "-", "description": "", 'being': False},
                            "1": {"title": "-", "description": "", 'being': False},
                            "3": {"title": "-", "description": "", 'being': False},
                            "4": {"title": "-", "description": "", 'being': False},
                            "5": {"title": "-", "description": "", 'being': False},
                            "6": {"title": "-", "description": "", 'being': False}

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
        self.setWindowIcon(QIcon("images/main_icon.ico"))
        self.cb_1.clicked.connect(self.edit_menu)
        self.cb_2.clicked.connect(self.edit_menu)
        self.cb_3.clicked.connect(self.edit_menu)
        self.cb_4.clicked.connect(self.edit_menu)
        self.cb_5.clicked.connect(self.edit_menu)
        self.cb_6.clicked.connect(self.edit_menu)
        self.changebox.hide()
        self.save_new.clicked.connect(self.make_a_note)
        self.just_back.clicked.connect(self.backEvent)
        self.db_1.clicked.connect(self.deleteEvent)
        self.db_2.clicked.connect(self.deleteEvent)
        self.db_3.clicked.connect(self.deleteEvent)
        self.db_4.clicked.connect(self.deleteEvent)
        self.db_5.clicked.connect(self.deleteEvent)
        self.db_6.clicked.connect(self.deleteEvent)
        self.menuAbout_us.triggered.connect(self.about)
        self.info_label = QMessageBox(self)

    def about(self):
        self.info_label.setText("Приложение \"Memorandum\"\nСтатус разработки: alpha\n\n\n\nДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ НЕ ПРЕДНАЗНАЧЕНО ДЛЯ МАССОВОГО РАСПРОСТРАНЕНИЯ И ЗАЩИЩЕНО АВТОРСКИМ ПРАВОМ. \n\nNavio, Sarugakuza, AmaryllisIt, \n2026")
        self.info_label.show()
        self.info_label.setWindowTitle('О приложении')

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

    def make_a_note(self):
        global current_user
        """процесс сохранения новой информации и внесение её в БД"""
        # print(self.number)
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
            data[self.number]['being'] = True
            # print(data)
            # print(current_user)
            try:
                cursor.execute(
                    f'UPDATE USERDATA SET DATA = "{data}" WHERE LOGIN = "{current_user}"')
            except sqlite3.OperationalError as e:
                self.info_label.setText("В данной версии программы недопустимо использование одинарных и двойных кавычек и других специальных символов.")
                self.info_label.setWindowTitle('Ошибка!')
                self.info_label.show()

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
        if not data['1']['being']:
            self.cb_1.setText('Создать')
            self.db_1.setEnabled(False)
        else:
            self.cb_1.setText('Редактировать')
            self.db_1.setEnabled(True)
        self.stack_2.setTitle(data['2']['title'])
        self.lt_2.setText(data['2']['description'])
        if not data['2']['being']:
            self.cb_2.setText('Создать')
            self.db_2.setEnabled(False)
        else:
            self.cb_2.setText('Редактировать')
            self.db_2.setEnabled(True)
        self.stack_3.setTitle(data['3']['title'])
        self.lt_3.setText(data['3']['description'])
        if not data['3']['being']:
            self.cb_3.setText('Создать')
            self.db_3.setEnabled(False)
        else:
            self.cb_3.setText('Редактировать')
            self.db_3.setEnabled(True)
        self.stack_4.setTitle(data['4']['title'])
        self.lt_4.setText(data['4']['description'])
        if not data['4']['being']:
            self.cb_4.setText('Создать')
            self.db_4.setEnabled(False)
        else:
            self.cb_4.setText('Редактировать')
            self.db_4.setEnabled(True)
        self.stack_5.setTitle(data['5']['title'])
        self.lt_5.setText(data['5']['description'])
        if not data['5']['being']:
            self.cb_5.setText('Создать')
            self.db_5.setEnabled(False)
        else:
            self.cb_5.setText('Редактировать')
            self.db_5.setEnabled(True)
        self.stack_6.setTitle(data['6']['title'])
        self.lt_6.setText(data['6']['description'])
        if not data['6']['being']:
            self.cb_6.setText('Создать')
            self.db_6.setEnabled(False)
        else:
            self.cb_6.setText('Редактировать')
            self.db_6.setEnabled(True)
        self.repaint()

    def backEvent(self):
        self.title.setPlainText('')
        self.description.setPlainText('')
        self._show_mainboard()
        self.init_user_interface()
        self.changebox.hide()
        self.label_mainwindow_name.setText('Memorandum')
        self.label_mainwindow_name.setFont(QFont('Comic Sans MS', 30))
        self.label_mainwindow_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    def deleteEvent(self):
        confirmation = QMessageBox.question(
            self, "Удалить", "Вы точно хотите удалить заметку?")
        if confirmation == 16384:
            self.number = self.sender().objectName().split('_')[-1]
            with sqlite3.connect(database="database/database.sqlite3") as db:
                cursor = db.cursor()
                req = cursor.execute(
                    f'SELECT * FROM USERDATA WHERE LOGIN = "{current_user}"')

                data = [item for item in req][0][-1]
                data = ast.literal_eval(data)

                data[self.number]['title'] = '-'
                data[self.number]['description'] = ''
                data[self.number]['being'] = False

                cursor.execute(
                    f'UPDATE USERDATA SET DATA = "{data}" WHERE LOGIN = "{current_user}"')

                db.commit()

            self.init_user_interface()
        else:
            pass


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
