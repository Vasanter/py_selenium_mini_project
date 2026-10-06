import allure
import platform
from selenium.webdriver import Keys

from base.base_page import BasePage
from config.links import Links
from selenium.webdriver.support import expected_conditions as EC


class PersonalPage(BasePage):

    PAGE_URL = Links.PERSONAL_PAGE

    FIRST_NAME_FIELD = ("xpath", "//input[@name='firstName']")
    SAVE_BUTTON = ("xpath", "(//button[@type='submit'])[1]")
    SPINNER = ("xpath", "//div[contains(@class,'oxd-loading-spinner')]")

    def change_name(self, new_name):
        with allure.step(f"Change name on '{new_name}'"):
            first_name_field = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
            # Ждём пока поле заполнится данными с сервера (Vue подгружает асинхронно)
            self.wait.until(lambda d: d.find_element(*self.FIRST_NAME_FIELD).get_attribute("value") != "")
            first_name_field = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD))
            # Кроссплатформенное выделение всего текста: COMMAND на Mac, CONTROL на Win/Linux
            select_all_key = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
            # Пробуем несколько способов очистки, чтобы работать в headless Linux/Windows
            try:
                first_name_field.send_keys(select_all_key, "a")
            except Exception:
                first_name_field.send_keys(select_all_key + "a")
            first_name_field.send_keys(Keys.BACKSPACE)
            # Fallback через JS если поле не очистилось
            if first_name_field.get_attribute("value") != "":
                self.driver.execute_script("arguments[0].value = '';", first_name_field)
                # Триггерим input событие для Vue
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", first_name_field)
            first_name_field.send_keys(new_name)
            self.name = new_name

    @allure.step("Save changes")
    def save_changes(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Changes have been saved successfully")
    def is_changes_saved(self):
        self.wait.until(EC.invisibility_of_element_located(self.SPINNER))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_FIELD))
        self.wait.until(EC.text_to_be_present_in_element_value(self.FIRST_NAME_FIELD, self.name))

    # Для обратной совместимости со старым названием (опечатка)
    def is_changes_saves(self):
        return self.is_changes_saved()