
import json
import pytest
from fixture.application import Application
import os.path



fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target=json.load(f)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config=load_config(request.config.getoption("--target"))['web']
    if fixture is None or not fixture.is_valid():
        fixture=Application(browser=browser,baseUrl=web_config["baseUrl"])
    fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture

@pytest.fixture(scope="session", autouse = True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


#pytest_addoption(parser):
#special hook that pytest will look for when it starts up. It takes a parser argument, which is used to add options to the pytest command line

def pytest_addoption(parser):
    parser.addoption("--browser", action="store",default="firefox")
    parser.addoption("--target", action="store", default="target.json")












