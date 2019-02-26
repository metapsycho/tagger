import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui.main_wnd import Ui_MainWnd
from mgr import *


class MainWnd(QMainWindow, Ui_MainWnd):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        self.setupUi(self)
        width = self.centralLayout.contentsMargins().left()
        self.hsplitter.setHandleWidth(width)
        self.vsplitter.setHandleWidth(width)

        self.repo = Repo()
        self.explorer = Explorer(self.repo, self.cwdView, self.folderView, self)

        # TODO: remove
        self.repo.reset(os.path.abspath('.'))

    def setRepo(self):
        ret = QFileDialog.getExistingDirectory(
            parent=self,
            caption='set repository',
            directory='.')
        self.repo.reset(os.path.abspath(ret))

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
