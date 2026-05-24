from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def table_filter(driver, row_locator, column_locator):
    rows = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located(row_locator)
    )

    table_dict = []

    for row in rows:
        columns = row.find_elements(*column_locator)

        row_data = {
            "name": columns[0].text,
            "email": columns[1].text,
            "department": columns[2].text,
            "registrationId": columns[3].text,
            "age": columns[4].text
        }
        table_dict.append(row_data)

    return table_dict
