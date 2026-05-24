from selenium.webdriver.support.ui import WebDriverWait

def wait_for_table_to_contain_rows(driver, row_locator, column_locator, timeout=10):
    def table_has_expected_name(driver):
        rows = driver.find_elements(*row_locator)

        for row in rows:
            columns = row.find_elements(*column_locator)

            if len(columns) >= 5:
                return True

        return False

    WebDriverWait(driver, timeout).until(table_has_expected_name)