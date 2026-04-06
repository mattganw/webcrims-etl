from operator import le

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def build_driver() -> webdriver:
    options = Options()
    #options.add_argument("--headless=new")
    driver = webdriver.Edge(options=options)
    return driver

def get_num_courtparts() -> int:
    
    url = "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc=&td=&rbOutputFormat=HTML&txtEmail="
    
    with build_driver() as driver:
        driver.get(url)

        court_part_dropdown = driver.find_element(By.ID, 'textCourtPart')
        options_all = court_part_dropdown.find_elements(By.TAG_NAME, "option")
        options_filtered = [opt for opt in options_all if opt.get_attribute("value") != "0"]

        if len(options_filtered) <= 0:
            raise Exception("No court parts were returned")

        return len(options_filtered)

if __name__ == "__main__":
   
    res = get_num_courtparts()
    print(f"{res} court parts available in dropdown")
