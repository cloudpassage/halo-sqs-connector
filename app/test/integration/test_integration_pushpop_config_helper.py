import imp
import os
import pytest
import sys


module_name = 'pushpop'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
pushpop = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationConfigHelper(object):
    def test_integration_config_helper_instantiate_push_events(self,
                                                               monkeypatch):
        monkeypatch.setenv("HALO_API_KEY", "abc123")
        monkeypatch.setenv("HALO_API_SECRET_KEY", "def456")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "push")
        monkeypatch.setenv("HALO_MODULE", "events")
        monkeypatch.setenv("START_TIME", "2018-01-01")
        assert pushpop.ConfigHelper()

    def test_integration_config_helper_instantiate_push_fail(self,
                                                             monkeypatch):
        monkeypatch.setenv("HALO_API_KEY", "abc123")
        monkeypatch.setenv("HALO_API_SECRET_KEY", "def456")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "push")
        with pytest.raises(ValueError):
            assert pushpop.ConfigHelper()

    def test_integration_config_helper_instantiate_pop(self,
                                                       monkeypatch):
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "pop")
        monkeypatch.setenv("HALO_MODULE", "events")
        assert pushpop.ConfigHelper()

    def test_integration_config_helper_instantiate_pop_fail(self,
                                                            monkeypatch):
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "pop")
        monkeypatch.setenv("HALO_MODULE", "events")
        monkeypatch.delenv("APPLICATION_MODE")
        with pytest.raises(ValueError):
            assert pushpop.ConfigHelper()
