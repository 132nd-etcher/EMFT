# coding=utf-8

import abc

from src.ui.main_ui_tab_widget import MainUiTabMethod

TAB_NAME = 'Reorder lua tables'


class TabReorderAdapter:
    @MainUiTabMethod(TAB_NAME)
    @abc.abstractmethod
    def tab_reorder_update_view_after_artifact_scan(self, *args, **kwargs):
        """"""

    @MainUiTabMethod(TAB_NAME)
    @abc.abstractmethod
    def tab_reorder_update_view_after_branches_scan(self, *args, **kwargs):
        """"""
