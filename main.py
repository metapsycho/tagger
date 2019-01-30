import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.main_wnd import Ui_MainWnd


class MainWnd(QMainWindow, Ui_MainWnd):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        self.setupUi(self)

    def setRoot(self):
        ret = QFileDialog.getExistingDirectory(
            parent=self,
            caption='set root',
            directory='.')
        print('setRoot', ret)

    def loadTags(self):
        ret = QFileDialog.getOpenFileName(
            parent=self,
            caption='load tags',
            directory='.',
            filter='*.*')
        print('loadTags', ret)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = MainWnd()
    wnd.show()
    sys.exit(app.exec_())
