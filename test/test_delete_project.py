from  model.project import Project
import pytest
import random

def test_delete_project(app):
    app.session.login("administrator", "root")
    if len(app.helper_project.get_project_list()) == 0:
        app.helper_project.open_projects_page()
        app.helper_project.fill_project_form(
            Project(name="first", description="middle"))
    old_projects = app.helper_project.get_project_list()
    project = random.choice(old_projects)
    project_name=project.name
    app.helper_project.delete_project_by_name(project_name)
    new_projects=app.helper_project.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)





