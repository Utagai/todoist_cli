import pytest
from todo.conf_schema import TodoConfig
from todo.cli import TodoistCLI


@pytest.fixture
def todoist_cli():
    conf = TodoConfig.get_config()
    to = TodoistCLI(conf)
    return to


def test_do_projects(todoist_cli):
    projs = todoist_cli.do_projects("")
    proj_names = [p.name for p in projs]
    assert "Inbox" in proj_names
