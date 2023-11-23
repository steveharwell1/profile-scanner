from selenium.common.exceptions import NoSuchElementException

def safe_find_element(driver, by, selector):
    try:
        elem = driver.find_element(by, selector)
        return elem
    except NoSuchElementException:
        return None