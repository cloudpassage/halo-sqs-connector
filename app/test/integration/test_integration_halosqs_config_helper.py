import imp
import os
import pytest
import sys


module_name = 'halosqs'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
halosqs = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationConfigHelper(object):
    def test_integration_config_helper_instantiate_send_events(self,
                                                               monkeypatch):
        monkeypatch.setenv("HALO_API_KEY", "abc123")
        monkeypatch.setenv("HALO_API_SECRET_KEY", "def456")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "send")
        monkeypatch.setenv("HALO_MODULE", "events")
        monkeypatch.setenv("START_TIME", "2018-01-01")
        assert halosqs.ConfigHelper()

    def test_integration_config_helper_instantiate_send_fail(self,
                                                             monkeypatch):
        monkeypatch.setenv("HALO_API_KEY", "abc123")
        monkeypatch.setenv("HALO_API_SECRET_KEY", "def456")
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "send")
        with pytest.raises(ValueError):
            assert halosqs.ConfigHelper()

    def test_integration_config_helper_instantiate_receive(self,
                                                           monkeypatch):
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "abc123")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "abc123")
        monkeypatch.setenv("SQS_QUEUE_URL", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "receive")
        monkeypatch.setenv("HALO_MODULE", "events")
        assert halosqs.ConfigHelper()

    def test_integration_config_helper_instantiate_receive_fail(self,
                                                                monkeypatch):
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "abc123")
        monkeypatch.setenv("APPLICATION_MODE", "receive")
        monkeypatch.setenv("HALO_MODULE", "events")
        monkeypatch.delenv("APPLICATION_MODE")
        with pytest.raises(ValueError):
            assert halosqs.ConfigHelper()
