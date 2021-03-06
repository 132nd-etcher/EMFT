# coding=utf-8

from PyQt5.QtGui import QStandardItem, QStandardItemModel

from emft.core.singleton import Singleton


class AutoProfileModelContainer(metaclass=Singleton):
    def __init__(self, parent=None):
        self._model = AutoProfileModel(parent)

    @property
    def model(self) -> QStandardItemModel:
        return self._model


class AutoProfileModel(QStandardItemModel):
    def __init__(self, parent=None):
        QStandardItemModel.__init__(self, parent)

    def appendRow(self, output_folder_name: str):  # noqa: N802
        item = QStandardItem(output_folder_name)
        super(AutoProfileModel, self).appendRow(item)
