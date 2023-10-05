import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from numpy.fft import fft, fftfreq


def generate_harmonic_signal(freq, duration, samp_rate):  # генерация гармонического сигнала с заданной частотой
    x = np.linspace(0, duration, samp_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


def generate_digital_signal(freq, duration, samp_rate):  # генерация цифрового сигнала с заданной частотой
    x = np.linspace(0, duration, samp_rate * duration, endpoint=False)
    y = scipy.signal.square(2 * np.pi * freq * x)
    y = np.where(y < 0, 0, y)  # амплитуда такого сигнала должна быть положительной
    return x, y


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.move(650, 400)
        self.setFixedSize(650, 280)
        self.setWindowTitle('Аттестация 1: Спектры гармонических и цифровых сигналов')
        lbl = QLabel("Спектры гармонических и цифровых сигналов")
        lbl.setFont(QFont('Times', 16))
        lbl.setGeometry(40, -20, 650, 100)
        self.layout().addWidget(lbl)

        self.res_button = QPushButton('Показать сигнал', self)
        self.res_button.setGeometry(60, 100, 250, 50)
        self.res_button.setFont(QFont('Times', 16))
        self.res_button.clicked.connect(self.signal)

        self.spectrum_button = QPushButton('Спектрограмма', self)
        self.spectrum_button.setGeometry(330, 100, 250, 50)
        self.spectrum_button.setFont(QFont('Times', 16))
        self.spectrum_button.clicked.connect(self.spec)

        self.label = QLabel("Введите частоту сигнала:", self)
        self.label.setGeometry(255, 150, 200, 30)

        self.combo = QComboBox(self)
        self.combo.setGeometry(220, 180, 210, 30)
        self.combo.addItems(["1 Гц", "2 Гц", "4 Гц", "8 Гц"])
        self.combo.setFont(QFont("Times New Roman", 14))

        self.duration = 5
        self.curr_freq = 1
        self.samp_rate = 1000

    def change(self, freq):  # изменение частоты
        self.curr_freq = int(freq)

    def save(self):  # сохранение
        self.change(self.combo.currentText().split(" ")[0])

    def signal(self):
        self.show_signal(int(self.combo.currentText().split(" ")[0]))

    def show_signal(self, freq):  # показывает сигналы с заданной частотой
        self.save()
        _, signal = generate_harmonic_signal(freq, self.duration, self.samp_rate)  # генерируем гармонический сигнал, берем только сам сигнал
        time = np.linspace(0, self.duration, num=self.duration * self.samp_rate)  # время

        fig = plt.figure("Гармонический сигнал")  # отображаем сигнал
        fig.canvas.manager.window.move(100, 250)
        plt.plot(time, signal, label="Гармонический сигнал " + str(self.curr_freq) + " Гц")
        plt.legend()
        plt.xlabel('Время, сек')
        plt.ylabel('Амплитуда')
        plt.title('Гармонический сигнал')
        plt.xlim(0, 5)  # обрезал по осям, чтобы маштаб был адекватный
        plt.ylim(-2, 2)
        plt.grid(True)
        plt.show()

        _, signal = generate_digital_signal(freq, self.duration, self.samp_rate)  # генерируем цифровой сигнал
        time = np.linspace(0, self.duration, num=self.duration * self.samp_rate)

        fig1 = plt.figure("Цифровой сигнал")  # аналогично
        fig1.canvas.manager.window.move(750, 250)
        plt.plot(time, signal, label="Цифровой сигнал " + str(self.curr_freq) + " Гц")
        plt.legend()
        plt.xlabel('Время, сек')
        plt.ylabel('Амплитуда')
        plt.title('Цифровой сигнал')
        plt.xlim(0, 5)
        plt.ylim(-2, 2)
        plt.grid(True)
        plt.show()

    def spec(self):
        self.show_spectrum(int(self.combo.currentText().split(" ")[0]))

    def show_spectrum(self, freq):
        self.save()
        _, signal = generate_harmonic_signal(freq, self.duration, self.samp_rate)  # генерируем гармонический сигнал
        N = self.duration * self.samp_rate

        y = fft(signal)  # с помощью преобразований фурье находим его спектр
        x = fftfreq(N, 1 / self.samp_rate)

        fig = plt.figure("Гармонический сигнал")  # отображаем спектр
        fig.canvas.manager.window.move(100, 250)
        plt.plot(x, np.abs(y), label="Спектр гармонического сигнала " + str(self.curr_freq) + " Гц")
        plt.legend()
        plt.xlabel('Частота, Гц')
        plt.ylabel('Амплитуда')
        plt.title('Гармонический сигнал')
        plt.xlim(0, 10)
        plt.ylim(0, N / 1.8)
        plt.grid(True)
        plt.show()

        _, signal = generate_digital_signal(freq, self.duration, self.samp_rate)  # аналогично для цифрового сигнала
        N = self.duration * self.samp_rate

        y = fft(signal)
        x = fftfreq(N, 1 / self.samp_rate)

        fig1 = plt.figure("Цифровой сигнал")
        fig1.canvas.manager.window.move(750, 250)
        x = x[2:len(x)]
        y = y[2:len(y)]
        plt.plot(x, np.abs(y), label="Спектр цифрового сигнала " + str(self.curr_freq) + " Гц")
        plt.legend()
        plt.xlabel('Частота, Гц')
        plt.ylabel('Амплитуда')
        plt.title('Цифровой сигнал')
        plt.xlim(0, self.curr_freq * 15)
        plt.ylim(0, N / 2)
        plt.grid(True)
        plt.show()


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
