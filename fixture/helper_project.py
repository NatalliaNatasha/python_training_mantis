
from model.project import Project
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




class HelperProject:
    def __init__(self,app):
        self.app = app


    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

    def change_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@class='button-small'][@type='submit'][@value='Create New Project']").click()
        self.change_field("name", project.name)
        self.change_field("description", project.description)
        self.submit_project_creation()



    def submit_project_creation(self):
       wd = self.app.wd
       wd.find_element_by_xpath("//input[@class='button'][@type='submit'][@value='Add Project']").click()


    def get_project_list(self):
        wd = self.app.wd
        self.open_projects_page()
        self.project_list = []

        try:
            for e in wd.find_elements_by_css_selector("tr.row-1, tr.row-2"):
                td_value = e.find_element_by_xpath('./td[1]')
                text=td_value.text

                # Wait for the link with href
                link = WebDriverWait(e, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, ".//a[contains(@href, 'manage_proj_edit_page.php?project_id=')]"))
                )
                href = link.get_attribute('href')
                project_id = int(href.split('project_id=')[-1])
                # Append the project to the project list
                self.project_list.append(Project(name=text, id=project_id))

        except Exception :
            print(f"Error")

        return list(self.project_list)


    def select_project_by_name(self,name):
        wd = self.app.wd
        find_name=wd.find_element_by_xpath(f"//a[contains(text(),'{name}')]")
        find_name.click()




    def delete_project_by_name(self,name):
        wd = self.app.wd
        self.open_projects_page()
        self.select_project_by_name(name)
        wd.find_element_by_xpath("//input[@class='button'][@type='submit'][@value='Delete Project']").click()
        wd.find_element_by_xpath( "//input[@class='button'][@type='submit'][@value='Delete Project']").click()
        self.open_projects_page()