from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


SECONDS_TO_WAIT = 10

def get_series(code):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www3.bcb.gov.br/sgspub/")

    try:
        element = WebDriverWait(driver, SECONDS_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "txCodigo"))
        )
    finally:
        element.send_keys(code)
        action = ActionChains(driver)
        action.send_keys(Keys.ENTER)
        action.perform()

    elements = driver.find_elements(By.CSS_SELECTOR, 'input.botao')
    driver.implicitly_wait(2)
    ActionChains(driver).click(elements[0]).perform()
    driver.implicitly_wait(2)
    ActionChains(driver).click(elements[3]).perform()

    try:
        element = WebDriverWait(driver, SECONDS_TO_WAIT).until(
            EC.presence_of_element_located((By.ID, "dataInicio"))
        )
    finally:
        element.clear()
        element.send_keys("01012021")

    elements = driver.find_elements(By.CSS_SELECTOR, 'input.botao')
    driver.implicitly_wait(2)
    ActionChains(driver).click(elements[0]).perform()
    driver.implicitly_wait(2)
    ActionChains(driver).click(elements[4]).perform()

    try:
        element = WebDriverWait(driver, SECONDS_TO_WAIT).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="valoresSeries"]'))
        )
    finally:
        rows = element.find_elements(By.TAG_NAME, "tr")

    data = {}
    for row in rows:
        col = row.find_elements(By.TAG_NAME, "td")
        for index, coluna in enumerate(col):
            if index == 0:
                dict_key = coluna.text
            else:
                try:
                    float(coluna.text.replace(",", "."))
                except ValueError:
                    pass
                else:
                    dict_value = coluna.text
                    data[dict_key] = dict_value
    # data = extract_data(rows)
    print("\nDATA: ", data)

    driver.close()
