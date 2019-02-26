import os
from PyQt5.QtCore import *


class Repo:
    def __init__(self):
        self.__repo_root = ''
        self.__root = ''
        self.__dirs = []
        self.__files = []
        self.__callbacks = []

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

    def addUpdateCallback(self, cb):
        self.__callbacks.append(cb)

    def __update(self, root):
        self.__root, self.__dirs, self.__files = next(os.walk(root))
        self.__root = os.path.abspath(self.__root)
        if self.__root != self.__repo_root:
            self.__dirs = ['..', ] + self.__dirs
        for cb in self.__callbacks:
            cb(self)


class Explorer(QAbstractListModel):
    def __init__(self, repo, cwd_view, folder_view, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.repo = repo
        self.repo.addUpdateCallback(self.__onRepoUpdated)
        self.cwd_view = cwd_view
        folder_view.setModel(self)
        folder_view.doubleClicked.connect(self.__update)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.repo.dirs)

    def data(self, index, role=None):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.repo.dirs[index.row()])
        return QVariant()

    def __update(self, index):
        self.repo.enter(index.row())

    def __onRepoUpdated(self, repo):
        self.cwd_view.setText(self.repo.root)
        self.cwd_view.setCursorPosition(0)
        self.cwd_view.repaint()

        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), 0))
        self.layoutChanged.emit()


class FileList(QAbstractTableModel):
    def __init__(self, repo, file_view, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.repo = repo
        file_view.setModel(self)


class TagManager:
    def __init__(self):
        pass

    def index(self):
        pass


if __name__ == '__main__':
    repo = Repo()
    repo.reset(os.path.abspath('.'))
    while True:
        print(repo.root)
        print(repo.dirs)
        print(repo.files)
        print('----------')
        idx = input('dir:')
        repo.enter(int(idx))


