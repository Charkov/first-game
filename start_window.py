from window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import sqlite3
from sokoban import Game


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        for i in range(1, 15):
            exec(f'self.label_{i}.hide()')
        self.pushButton_1.clicked.connect(self.button_1)
        self.pushButton_2.clicked.connect(self.button_2)
        self.pushButton_3.clicked.connect(self.button_3)
        self.pushButton_4.clicked.connect(self.button_4)
        self.pushButton_5.clicked.connect(self.button_5)
        self.pushButton_16.clicked.connect(self.time_to_complete_the_level)

    def time_to_complete_the_level(self):
        if self.pushButton_16.text() == 'Время прохождения уровней':
            con = sqlite3.connect('records.sqlite')
            cur = con.cursor()
            for i in range(1, 15):
                exec(f'self.pushButton_{i}.hide()')
                exec(f'self.label_{i}.show()')
                time = cur.execute(f'''SELECT level_time FROM time WHERE id = "{i}"''').fetchone()[0]
                exec(f'self.label_{i}.setText("{i}: {time} сек")')
            self.radioButton.hide()
            self.radioButton_2.hide()
            con.commit()
            self.pushButton_16.setText('назад')
        else:
            for i in range(1, 15):
                exec(f'self.pushButton_{i}.show()')
                exec(f'self.label_{i}.hide()')
                self.pushButton_16.setText('Время прохождения уровней')
            self.radioButton.show()
            self.radioButton_2.show()

    def select(self):
        if self.radioButton.isChecked():
            d = open('decoration.txt', 'a')
            d.write('1')
            d.close()
        if self.radioButton_2.isChecked():
            d = open('decoration.txt', 'a')
            d.write('2')
            d.close()

    def start_game(self, num_level):
        self.select()
        f = open('level_number.txt', 'a')
        f.write(num_level)
        f.close()
        Game(self)

    def button_1(self):
        self.start_game('1')

    def button_2(self):
        self.start_game('2')

    def button_3(self):
        self.start_game('3')

    def button_4(self):
        self.start_game('4')

    def button_5(self):
        self.start_game('5')



pic = '''Window
{background-image:url(C:/Users/Vlad/PycharmProjects/pythonProject/data/i.png);
background-repeat: no-repeat;}'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(pic)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
