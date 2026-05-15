# Verify NO `log.write(` calls remain in any src file
import os
import re

def test_no_deprecated_calls_anywhere():
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
    for f in os.listdir(src_dir):
        if not f.endswith('.py') or f == 'logger.py':
            continue
        with open(os.path.join(src_dir, f)) as fh:
            content = fh.read()
        # Should have ZERO calls to log.write(
        assert 'log.write(' not in content, f"Found deprecated log.write() in {f}"

def test_new_api_used_in_each_module():
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
    for module in ['auth.py', 'api.py', 'db.py', 'utils.py']:
        with open(os.path.join(src_dir, module)) as fh:
            content = fh.read()
        # Should use at least one of log.info/error/debug
        assert any(x in content for x in ('log.info(', 'log.error(', 'log.debug(')), f"{module} not using new API"
