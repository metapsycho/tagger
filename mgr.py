import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Repo:
    def __init__(self):
        self.__repo_root = ''
        self.__root = ''
        self.__dirs = []
        self.__files = []

    @property
    def repo_root(self):
        return self.__repo_root

    @property
    def root(self):
        return self.__root

    @property
    def dirs(self):
        return self.__dirs

    @property
    def files(self):
        return self.__files

    def reset(self, repo_root):
        self.__repo_root = repo_root
        self.__update(self.__repo_root)

    def enter(self, index):
        if len(self.__dirs) != 0:
            self.__update(os.path.join(self.__root, self.__dirs[index]))

    def __update(self, root):
        self.__root, self.__dirs, self.__files = next(os.walk(root))
        self.__root = os.path.abspath(self.__root)
        if self.__root != self.__repo_root:
            self.__dirs = ['..', ] + self.__dirs


class Explorer(QAbstractTableModel):
    def __init__(self, file_system, folder_view, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.fs = file_system
        folder_view.setModel(self)
        folder_view.doubleClicked.connect(self._update)

    def headerData(self, sec, orient, role=None):
        if role == Qt.DisplayRole and orient == Qt.Horizontal and sec == 0:
            return QVariant('name')
        return QVariant()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.fs.dirs) + 1

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        if index.row() == 0:
            return QVariant('..')
        return QVariant(self.fs.dirs[index.row() - 1])

    def _update(self, index):
        self.fs.root + self.fs.dirs[index.row()]
        self.fs.update()


class TagManager:
    def __init__(self):
        pass

    def index(self):
        pass


if __name__ == '__main__':
    repo = Repo()
    repo.init(os.path.abspath('.'))
    while True:
        print(repo.root)
        print(repo.dirs)
        print(repo.files)
        print('----------')
        idx = input('dir:')
        repo.enter(int(idx))


