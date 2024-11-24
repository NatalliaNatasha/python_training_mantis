from suds.client import Client
from suds import WebFault




class SoapHelper:
    def __init__(self, app):
        self.app=app

    def can_login(self,username,password):
        client = Client(self.app.baseUrl + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username,password)
            return True
        except WebFault as f:
            return f



    def get_project_list(self):
        client = Client(self.app.baseUrl + "api/soap/mantisconnect.php?wsdl")
        try:
            get_user_projects = client.service.mc_projects_get_user_accessible("administrator", "root")
            return get_user_projects
        except WebFault as fault:
            return fault

