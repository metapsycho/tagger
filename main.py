import sys
import os
from PyQt5.QtWidgets import *
from ui.main_wnd import Ui_MainWnd
from mgr import *


class MainWnd(QMainWindow, Ui_MainWnd):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        self.setupUi(self)
        width = self.centralLayout.contentsMargins().left()
        self.centralArea.setHandleWidth(width)
        self.filterArea.setHandleWidth(width)
        self.fileView.setAlternatingRowColors(True)

        self.repo = Repo()
        self.explorer = Explorer(self.repo, self.cwdView, self.folderView, self)
        self.file_list = FileList(self.repo, self.fileView, self)

        # TODO: remove
        self.repo.reset(os.path.abspath('G:\Cloud\百度云同步盘\Readings'))

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
