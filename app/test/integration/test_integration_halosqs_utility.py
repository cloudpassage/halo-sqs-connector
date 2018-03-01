import imp
import os
import sys


module_name = 'halosqs'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
halosqs = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationUtility(object):
    def test_integration_utility_pack_unpack_message(self):
        control = "I am a test string, yo."
        gz_str = halosqs.Utility.pack_message(control)
        print gz_str
        result = halosqs.Utility.unpack_message(gz_str)
        assert result == control
