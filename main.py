import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.main_wnd import Ui_MainWnd
from mgr import *


class MainWnd(QMainWindow, Ui_MainWnd):
    def __init__(self, parent=None):
        super(MainWnd, self).__init__(parent)
        self.setupUi(self)
        width = self.centralLayout.contentsMargins().left()
        self.detailSplitter.setHandleWidth(width)
        self.fileSplitter.setHandleWidth(width)
        self.filterSplitter.setHandleWidth(width)
        self.fileView.setAlternatingRowColors(True)

        # setup detail view
        self._hide_details_icon = QIcon(':/icons/res/hide_details.png')
        self._show_details_icon = QIcon(':/icons/res/show_details.png')
        self._detailBtn = QPushButton(self)
        self._detailBtn.setFixedSize(QSize(width*2+5, 30+5))
        self._detailBtn.setIconSize(self._detailBtn.size())
        self._detailBtn.setStyleSheet('border:none')
        self._detailBtn.hide()
        self._detailBtn.clicked.connect(self.__toggleDetail)
        self._detailSplitterSizes = [0, 0]
        self.detailSplitter.splitterMoved.connect(lambda x, y: self.__setDetailBtn())
        self.installEventFilter(self)

        self.repo = Repo()
        self.explorer = Explorer(self.repo, self.cwdView, self.folderView, self)
        self.file_list = FileList(self.repo, self.fileView, self.fileSelector, self)

        # TODO: remove
        self.repo.reset(os.path.abspath(r'G:\Cloud\百度云同步盘\Readings'))

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

    def __setDetailBtn(self):
        lsize, rsize = self.detailSplitter.sizes()
        if lsize != 0 and rsize != 0:
            self._detailSplitterSizes = [lsize, rsize]

        if rsize == 0:
            self._detailBtn.setIcon(self._show_details_icon)
            pos = QPoint(self.fileSplitter.width() + self.detailSplitter.handleWidth()*2 - self._detailBtn.width(),
                         (self.fileSplitter.height() - self._detailBtn.height()) // 2)
            pos = self.fileSplitter.mapTo(self, pos)
        elif lsize == 0:
            self._detailBtn.setIcon(self._hide_details_icon)
            pos = QPoint(-self.detailSplitter.handleWidth()*2,
                         (self.detailView.height() - self._detailBtn.height()) // 2)
            pos = self.detailView.mapTo(self, pos)
        else:
            self._detailBtn.setIcon(self._hide_details_icon)
            pos = QPoint(-(self.detailSplitter.handleWidth() + self._detailBtn.width()) // 2,
                         (self.detailView.height() - self._detailBtn.height()) // 2)
            pos = self.detailView.mapTo(self, pos)
        self._detailBtn.move(pos)

    def __toggleDetail(self, clicked):
        lsize, rsize = self.detailSplitter.sizes()
        if rsize == 0:
            self.detailSplitter.setSizes(self._detailSplitterSizes)
        else:
            self.detailSplitter.setSizes([self._detailSplitterSizes[0] + self._detailSplitterSizes[1], 0])
        self.__setDetailBtn()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove:
            rect = self._detailBtn.frameGeometry()
            if rect.contains(event.pos()):
                self._detailBtn.show()
            else:
                self._detailBtn.hide()
        return super(MainWnd, self).eventFilter(obj, event)

    def showEvent(self, event):
        self.__setDetailBtn()
        super(MainWnd, self).showEvent(event)

    def resizeEvent(self, event):
        self.__setDetailBtn()
        super(MainWnd, self).resizeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = MainWnd()
    wnd.show()
    sys.exit(app.exec_())
