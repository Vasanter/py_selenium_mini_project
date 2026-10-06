import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="function")
def driver(request):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--ignore-certificate-errors")
    # фикс для медленного CI: увеличиваем таймауты страницы
    driver = webdriver.Chrome(options=options, service=Service())
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Аттачим скриншот при падении для Allure
    if call.when == "call" and call.excinfo is not None:
        driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
        if driver:
            try:
                import allure
                from allure_commons.types import AttachmentType
                allure.attach(
                    body=driver.get_screenshot_as_png(),
                    name="failure_screenshot",
                    attachment_type=AttachmentType.PNG,
                )
                allure.attach(
                    body=driver.page_source,
                    name="page_source",
                    attachment_type=allure.attachment_type.HTML,
                )
                allure.attach(
                    body=driver.current_url,
                    name="current_url",
                    attachment_type=allure.attachment_type.TEXT,
                )
            except Exception:
                pass
