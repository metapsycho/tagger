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


class FileList(QAbstractListModel):
    def __init__(self, repo, file_view, file_selector, parent=None):
        QAbstractListModel.__init__(self, parent)
        self.repo = repo
        self.repo.addUpdateCallback(self.__onRepoUpdate)

        file_view.setModel(self)
        file_view.selectionModel().selectionChanged.connect(self.__onFilesSelected)

        self.file_selector = file_selector
        self.file_selector.setChecked(False)
        self.file_selector.stateChanged.connect(self.__onFileSelectorChecked)

        self.checked_indices = set()
        self.selections = set()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.repo.files)

    def data(self, index, role=None):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            return QVariant(self.repo.files[index.row()])
        elif role == Qt.CheckStateRole:
            if index.row() in self.checked_indices:
                return Qt.Checked
            return Qt.Unchecked
        return QVariant()

    def setData(self, index, value, role=None):
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole:
            if value == Qt.Checked:
                self.checked_indices.add(index.row())
            else:
                self.checked_indices.discard(index.row())
        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlags()
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable

    def __onRepoUpdate(self, repo):
        self.checked_indices.clear()

        self.layoutAboutToBeChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(), 0))
        self.layoutChanged.emit()

    def __onFilesSelected(self, selected, deselected):
        for idx in selected.indexes():
            self.selections.add(idx.row())
        for idx in deselected.indexes():
            self.selections.discard(idx.row())

        cnt = 0
        for s in self.selections:
            if s in self.checked_indices:
                cnt += 1
        self.file_selector.blockSignals(True)
        self.file_selector.setChecked(cnt > len(self.selections) // 2)
        self.file_selector.blockSignals(False)

    def __onFileSelectorChecked(self, state):
        if state == Qt.Checked:
            for s in self.selections:
                self.checked_indices.add(s)
                self.dataChanged.emit(self.createIndex(s, 0),
                                      self.createIndex(s, 0))
        elif state == Qt.Unchecked:
            for s in self.selections:
                self.checked_indices.discard(s)
                self.dataChanged.emit(self.createIndex(s, 0),
                                      self.createIndex(s, 0))


class TagManager:
    def __init__(self):
        pass

    def index(self):
        pass
