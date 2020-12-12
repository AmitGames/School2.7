from DumayCloud import client
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
mainwin = QtWidgets.QMainWindow()
client = client.Client()
client.login("itayd", "i")