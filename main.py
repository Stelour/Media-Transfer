from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QListWidget, QMessageBox
from PyQt6.QtCore import QDate
import sys
import os
import cx_Oracle
import hashlib
import shutil
import logging


logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('main.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# logger.debug(f'\n')
# logger.info(f'\n')
# logger.error(f'\n')
# logger.warning(f'\n')


dsn = cx_Oracle.makedsn(host='///', port='///', service_name='///')

try:
    logger.debug(f'Коннект базы')
    connection = cx_Oracle.connect(user='///', password='///', dsn=dsn)
    print("База данных доступна")
    logger.info(f'База доступна')
    connection.close()
except cx_Oracle.Error as error:
    logger.info(f'База не доступна')
    print("Ошибка:", error)

Department = 1
Section = 2
Group = 0
Information_type_id_for_video = 60
Information_type_id_for_audoi = 50

def get_oks():
    logger.debug(f'Вызов функции, которая выдает все айди\n')
    connection = cx_Oracle.connect(user='///', password='///', dsn=dsn)
    cursor = connection.cursor()

    oks = cursor.var(cx_Oracle.CURSOR)
    cursor.callproc("TABLES.Pack_Commutation_v3.get_OK_All", [oks])
    result_oks = oks.getvalue()

    sp_all_oks = []
    for row in result_oks:
        row = list(row[:3])
        sp_all_oks.append(row)

    cursor.close()
    connection.close()
    
    return sp_all_oks


def print_oks(self):
    logger.debug(f'Вызов функции, которая выводит все айди\n')
    sp_all_oks = get_oks()
    for row in sp_all_oks:
        row = list(row)
        if row[-1] == "None":
            self.listWidget.addItem(f"{row[0]} - {row[1]}")
        else:
            self.listWidget.addItem(f"{row[0]} - {row[1]} ({row[2]})")


def db_select(ok_id):
    logger.debug(f'Вызов функции, которая получает данные с бд\n')
    connection = cx_Oracle.connect(user='///', password='///', dsn=dsn)
    cursor = connection.cursor()

    cursor.execute("SELECT OK_ID, Begin_date, file_folder, file_name FROM TABLES.AUDIO_FRAGMENTS WHERE OK_ID = :ok_id", {'ok_id': ok_id})

    tables = cursor.fetchall() # < 0 - id ; 1 - date ; 2 - directory ; 3 - name  >

    cursor.close()
    connection.close()

    return tables


def db_update(ok_id, new_folder, file_name):
    logger.debug(f'Вызов функции, которая обновляет данные в бд\n')
    connection = cx_Oracle.connect(user='///', password='///', dsn=dsn)
    cursor = connection.cursor()

    cursor.execute("UPDATE TABLES.AUDIO_FRAGMENTS SET file_folder = :new_folder WHERE OK_ID = :ok_id AND file_name = :file_name", {'new_folder': new_folder, 'ok_id': ok_id, 'file_name': file_name})
    
    connection.commit()

    cursor.close()
    connection.close()


current_files = 0
all_files = 0
error_files = 0
class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(401, 360)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 261, 31))
        self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 111, 31))
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 30, 101, 31))
        self.pushButton.setObjectName("pushButton")

        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 110, 181, 192))
        self.listWidget.setObjectName("listWidget")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 111, 16))
        self.label_2.setObjectName("label_2")

        self.checkBox = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(20, 310, 171, 21))
        self.checkBox.setObjectName("checkBox")

        self.dateEdit = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(210, 110, 81, 22))
        self.dateEdit.setObjectName("dateEdit")

        self.listWidget_2 = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(210, 140, 181, 161))
        self.listWidget_2.setObjectName("listWidget_2")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 310, 81, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 310, 81, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 90, 111, 16))
        self.label_4.setObjectName("label_4")

        self.dateEdit_2 = QtWidgets.QDateEdit(parent=self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(310, 110, 81, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")

        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(300, 110, 16, 16))
        self.label_3.setObjectName("label_3")
        self.statusBar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_3.clicked.connect(self.refresh_directory)
        self.listWidget_2.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.checkBox.stateChanged.connect(self.checking_directory_all)
        self.pushButton.clicked.connect(self.select_directory)
        self.pushButton_2.clicked.connect(self.start_button)
        self.listWidget.itemClicked.connect(self.on_item_clicked)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit_2.setCalendarPopup(True)

        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit_2.setDate(QDate.currentDate())

        print_oks(self)

        logger.debug(f'Запуск программы\n')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "SohoTransfer"))
        self.label.setText(_translate("MainWindow", "Путь:"))
        self.pushButton.setText(_translate("MainWindow", "Обзор"))
        self.label_2.setText(_translate("MainWindow", "Выбор ID:"))
        self.checkBox.setText(_translate("MainWindow", "Отправлять все фрагменты"))
        self.pushButton_2.setText(_translate("MainWindow", "Начать"))
        self.pushButton_3.setText(_translate("MainWindow", "Обновить"))
        self.label_4.setText(_translate("MainWindow", "Выбор даты:"))
        self.label_3.setText(_translate("MainWindow", "-"))


    def checking_directory_all(self):
        logger.debug(f'Нажатие на чекбокс\n')
        if self.checkBox.isChecked():
            self.listWidget_2.setSelectionMode(QListWidget.SelectionMode.NoSelection)
            self.dateEdit.setEnabled(False)
            self.dateEdit_2.setEnabled(False)
            self.listWidget_2.clear()
            self.listWidget.clearSelection()
            self.listWidget_2.clearSelection()
            
        else:
            self.listWidget_2.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            self.dateEdit.setEnabled(True)
            self.dateEdit_2.setEnabled(True)
            self.listWidget.clearSelection()
            self.listWidget_2.clearSelection()
            self.listWidget_2.clear()

    def on_item_clicked(self):
        logger.debug(f'Нажатие на элемент в списке айди\n')
        date1 = self.dateEdit.date()
        date2 = self.dateEdit_2.date()

        if self.dateEdit_2.date() < self.dateEdit.date() and not (self.checkBox.isChecked()):
            logger.warning(f'Ошибка, начальная дата больше конечной\n')
            QMessageBox.warning(self, "Ошибка", "Начальная дата не может быть больше конечной даты.")
            self.listWidget.clearSelection()
            self.listWidget_2.clearSelection()
            self.listWidget_2.clear()
            return
        
        days_in_range = []
        current_date = date1
        while current_date <= date2:
            days_in_range.append(current_date.toString('yyyy-MM-dd'))
            current_date = current_date.addDays(1)

        selected = self.listWidget.selectedItems()
        if len(selected) != 0:
            ok_id = selected[0].text()
            ok_id = ok_id[:ok_id.find(' ')]
            self.listWidget_2.clear()
            sp_select = db_select(ok_id)

            if not self.checkBox.isChecked():
                logger.debug(f'Обновление файлов с выключенным чекбоксом\n')
                try:
                    for i in sp_select:
                        ok = i[0]

                        if str(ok) != str(ok_id):
                            continue
                        
                        date = i[1]
                        date = date.strftime("%Y-%m-%d")
                        # file_directory = i[2]
                        file_name = i[3]

                        for j in days_in_range:
                            if j == date:
                                self.listWidget_2.addItem(file_name)
                                break
                except:    
                    logger.error(f'Ошибка в обновление файлов\n')
            
            elif self.checkBox.isChecked():
                logger.debug(f'Обновление файлов с выключенным чекбоксом\n')
                try:
                    for i in sp_select:
                        # ok = i[0]
                        date = i[1]
                        date = date.strftime("%Y-%m-%d")
                        # file_directory = i[2]
                        file_name = i[3]

                        self.listWidget_2.addItem(file_name)
                except:
                    logger.error(f'Ошибка в обновление файлов\n')

    def select_directory(self):
        try:
            logger.debug(f'Нажатие на кнопку Обзор\n')
            directory = QFileDialog.getExistingDirectory()
            self.lineEdit.setText(directory)
        except:
            logger.error(f'Ошибка в нажатие кнопки Обзор\n')
    
    def refresh_directory(self):
        try:
            logger.debug(f'Обновление списков\n')
            self.listWidget.clear()
            self.listWidget_2.clear()
            print_oks(self)
            self.listWidget.clearSelection()
            self.listWidget_2.clearSelection()
        except:
            logger.error(f'Ошибка в обновлении списков\n')
    
    def start_button(self):
        global current_files, all_files, error_files
        logger.debug(f'Нажатие на кнопку Начать\n')

        directory = self.lineEdit.text()

        if len(directory) == 0 or not os.path.isdir(directory):
            logger.warning(f'"Ошибка Данной директории не существует."\n')
            QMessageBox.warning(self, "Ошибка", "Данной директории не существует.")
            return
        
        if directory[-1] == '/' or directory[-1] == '\\':
            directory = directory[:-1]

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText('Вы действительно хотите перенести файлы?')
        msg_box.setWindowTitle('Подтверждение')
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        button_choice = msg_box.exec()

        if button_choice == QMessageBox.StandardButton.Yes and len(self.listWidget.selectedItems()) > 0:
            logger.debug(f'Пользователь нажал на Yes, и он хочет начать')
            date1 = self.dateEdit.date()
            date2 = self.dateEdit_2.date()

            days_in_range = []
            current_date = date1
            while current_date <= date2:
                days_in_range.append(current_date.toString('yyyy-MM-dd'))
                current_date = current_date.addDays(1)
            
            sp_selected = []
            for i in range(len(self.listWidget_2.selectedItems())):
                selected = self.listWidget_2.selectedItems()
                sp_selected.append(selected[i].text())

            selected = self.listWidget.selectedItems()
            ok_id = selected[0].text()
            ok_id = ok_id[:ok_id.find(' ')]
            sp_select = db_select(ok_id)
            if not self.checkBox.isChecked() and len(self.listWidget_2.selectedItems()) > 0:
                all_files += len(sp_selected)
                logger.debug(f'Передача файлов с выключенным чекбоксом')

                try:
                    for k in sp_selected:
                        for i in sp_select:
                            # ok = i[0]
                            date = i[1].strftime("%Y-%m-%d")
                            file_directory = i[2]
                            file_name = i[3]

                            for j in days_in_range:
                                if j == date and k == file_name:
                                    try:
                                        shutil.copy2(file_directory + '/' + file_name, directory + '/' + file_name)

                                        if os.path.isfile(directory + '/' + file_name):
                                            with open(file_directory + '/' + file_name, 'rb') as file_to_check1:
                                                data1 = file_to_check1.read()
                                                hash1 = hashlib.md5(data1).hexdigest()

                                            with open(directory + '/' + file_name, 'rb') as file_to_check2:
                                                data2 = file_to_check2.read()
                                                hash2 = hashlib.md5(data2).hexdigest()

                                            if hash1 == hash2:
                                                os.remove(file_directory + '/' + file_name)

                                                directory1 = directory + '/'
                                                db_update(ok_id, directory1, file_name)

                                                current_files += 1
                                                self.statusBar.showMessage(f"{current_files}/{all_files}")
                                                logger.debug(f'Передача файла {file_name} в {directory} прошла успешно')
                                    except:
                                        logger.error(f'Передача файла {file_name} в {directory} не удалась, ошибка в копирование/проверке файла. Возможно файла в каталоге не существует, либо пользователь поменял дату и дата оказалась кривая.')
                except:
                    error_files += 1
                    logger.error(f'Передача файла {file_name} в {directory} не удалась')
            
            elif self.checkBox.isChecked():
                all_files += self.listWidget_2.count()
                logger.debug(f'Передача файлов с включенным чекбоксом')

                try:
                    for i in sp_select:
                        # ok = i[0]
                        date = i[1].strftime("%Y-%m-%d")
                        file_directory = i[2]
                        file_name = i[3]

                        try:
                            shutil.copy2(file_directory + '/' + file_name, directory + '/' + file_name)

                            if os.path.isfile(directory + '/' + file_name):
                                with open(file_directory + '/' + file_name, 'rb') as file_to_check1:
                                    data1 = file_to_check1.read()
                                    hash1 = hashlib.md5(data1).hexdigest()

                                with open(directory + '/' + file_name, 'rb') as file_to_check2:
                                    data2 = file_to_check2.read()
                                    hash2 = hashlib.md5(data2).hexdigest()

                                if hash1 == hash2:
                                    os.remove(file_directory + '/' + file_name)

                                    directory1 = directory + '/'
                                    db_update(ok_id, directory1, file_name)

                                    current_files += 1
                                    self.statusBar.showMessage(f"Передано - {current_files}/{all_files}")
                                    logger.debug(f'Передача файла {file_name} в {directory} прошла успешно')
                        except:
                            logger.error(f'Передача файла {file_name} в {directory} не удалась, ошибка в копирование/проверке файла. Возможно файла в каталоге не существует.')
                except:
                    logger.error(f'Передача файла {file_name} в {directory} не удалась')
                    error_files += 1

            self.listWidget_2.clearSelection()
            self.listWidget.clearSelection()
            self.listWidget_2.clear()
            
            if all_files > 0:
                self.statusBar.showMessage(f"Передано - {current_files}/{all_files}; Ошибок - {error_files}; Передача завершена!")
                logger.debug(f"Передано - {current_files}/{all_files}; Ошибок - {error_files}; Передача завершена!")

        else:
            self.listWidget_2.clearSelection()
            self.listWidget.clearSelection()
            self.listWidget_2.clear()
            return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()