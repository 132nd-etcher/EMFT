# coding=utf-8

import os
from logging import Handler, LogRecord, Logger, NOTSET, disable

import pytest

from emft.core.logging import Logged, make_logger


class DummyHandler(Handler):
    def __init__(self):
        # Bypass pytest
        super(DummyHandler, self).__init__()

    def emit(self, record):
        pass


class TestCustomLogging:
    def test_make_main_logger(self):
        logger = make_logger()
        assert isinstance(logger, Logger)
        assert logger.name == '__main__'

    @pytest.mark.parametrize('level', ['text', True, 42, None])
    def test_wrong_level(self, level):
        with pytest.raises(ValueError):
            make_logger(ch_level=level)
        with pytest.raises(ValueError):
            make_logger(fh_level=level)

    def test_make_sub_logger(self):
        logger = make_logger('test')
        assert isinstance(logger, Logger)
        assert logger.name == '__main__.test'
        del logger

    def test_class_logger(self):
        class SomeClass(Logged):
            pass

        obj = SomeClass()
        assert hasattr(obj, 'logger')
        assert isinstance(getattr(obj, 'logger'), Logger)
        assert getattr(obj, 'logger').name == '__main__.SomeClass'

    def test_logfile_creation(self, tmpdir):
        p = tmpdir.join('logfile')
        logger = make_logger(log_file_path=str(p))
        assert p.exists()
        del logger

    def test_logfile_reset(self, tmpdir, mocker, monkeypatch):
        p = tmpdir.join('logfile')
        make_logger(log_file_path=str(p))
        assert p.exists()

        mock = mocker.MagicMock()
        monkeypatch.setattr(os, 'remove', mock)

        logger = make_logger(log_file_path=str(p))
        assert mock.call_count == 1
        assert mock.call_args_list == [mocker.call(str(p))]
        del logger

    def test_custom_handler(self, mocker):
        handler = DummyHandler()
        mock = mocker.MagicMock()
        handler.emit = mock

        logger = make_logger()
        logger.handlers = [handler]

        disable(NOTSET)
        logger.debug('test')

        assert mock.call_count == 1
        emit_call = mock.mock_calls[0]
        name, args, kwargs = emit_call
        assert name == ''
        log_record = args[0]
        assert isinstance(log_record, LogRecord)
        assert log_record.msg == 'test'
        assert log_record.levelname == 'DEBUG'

        del logger

    def test_sublogger_handler(self):
        logger = make_logger()
        handler = DummyHandler
        sublogger = make_logger('sub', custom_handler=handler)
        assert handler in sublogger.handlers
        del logger
        del sublogger
