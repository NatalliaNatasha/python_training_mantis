
import json
import pytest
from fixture.application import Application
import os.path
import ftputil



fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target=json.load(f)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))




@pytest.fixture
def app(request,config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture=Application(browser=browser,config=config)
    return fixture

def install_server_configuration(host,username,password):
    with ftputil.FTPHost(host,username,password) as remote:
        if remote.path.isfile("config_inc.php.sample.bak"):
            remote.remove("config_inc.php.sample.bak")
        if remote.path.isfile("config_inc.php.sample"):
            remote.rename("config_inc.php.sample","config_inc.php.sample.bak")
        remote.upload(os.path.join(os.path.dirname(__file__),"resources/config_inc.php.sample") ,"config_inc.php.sample")

def restore_server_configuration(host,username,password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.sample.bak"):
            if remote.path.isfile("config_inc.php.sample"):
                remote.remove("config_inc.php.sample")
            remote.rename("config_inc.php.sample.bak", "config_inc.php.sample")






@pytest.fixture(scope="session", autouse = True)
def configure_server(request,config):
    install_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'],config['ftp']['username'],config['ftp']['password'])
        request.addfinalizer(fin)





def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata=load_from_module(fixture[5:])
            metafunc.parametrize(fixture,testdata,ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])



def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())

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












