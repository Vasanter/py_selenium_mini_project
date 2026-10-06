import allure

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage(BasePage):

    PAGE_URL = Links.DASHBOARD_PAGE

    MY_INFO_BUTTON = ("css selector", "[href='/web/index.php/pim/viewMyDetails']")
    DASHBOARD_HEADER = ("xpath", "//h6[contains(@class,'oxd-text') and contains(text(),'Dashboard')]")

    def is_opened(self):
        with allure.step(f"Page {self.PAGE_URL} is opened"):
            # В CI OrangeHRM грузится дольше 10с, ждем URL + ключевой элемент дашборда
            self.wait.until(EC.url_contains(self.PAGE_URL))
            self.wait.until(EC.visibility_of_element_located(self.MY_INFO_BUTTON))

    @allure.step("Click on 'My info' link")
    def click_my_info_link(self):
        self.wait.until(EC.element_to_be_clickable(self.MY_INFO_BUTTON)).click()
