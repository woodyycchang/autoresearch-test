from src.logger import log
from src.auth import login

def test_login_logs():
    log.messages.clear()
    login("alice")
    assert any("alice" in m for level, m in log.messages)
