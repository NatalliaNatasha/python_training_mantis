from  model.project import Project
import pytest
import random
import string


def random_string(prefix,maxlen):
    symbols=string.ascii_letters+string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata=[Project(name=random_string("name",5), description="")]+ [
     Project(name=random_string("name",10),
             description=random_string("description",17)

             )
     for i in range(1)
    ]


# @pytest.mark.parametrize("project",testdata)
# def test_add_project(app,project):
#     app.session.login("administrator", "root")
#     old_projects=app.helper_project.get_project_list()
#     print(old_projects)
#     app.helper_project.open_projects_page()
#     app.helper_project.fill_project_form(project)
#     app.helper_project.open_projects_page()
#     new_projects=app.helper_project.get_project_list()
#     print(new_projects)
#     assert len(old_projects) + 1 == len(new_projects)
#     old_projects.append(project)
#     assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

@pytest.mark.parametrize("project",testdata)
def test_add_project(app,project):
    app.session.login("administrator", "root")
    old_projects=app.soap.get_project_list()
    print(old_projects)
    app.helper_project.open_projects_page()
    app.helper_project.fill_project_form(project)
    app.helper_project.open_projects_page()
    new_projects=app.soap.get_project_list()
    print(new_projects)
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)



