from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
from time import sleep


#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

driver.get("https://www.imdb.com")
print(driver.title)
search = driver.find_element(By.NAME, "q")
search.send_keys("Zack Snyder")
search.send_keys(Keys.RETURN)

try:
    celeb = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ipc-metadata-list-summary-item__t"))
    )
except:
    driver.quit()
#celeb = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")
celeb.click()

try:
    print("here we go")
    #test = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t")
    #print(test)
    profession = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-856aec89-4"))
    )
    #response = HtmlResponse(url=driver.current_url, body=driver.page_source, encoding="utf-8", request=None)
    #Brand = response.css('.sc-856aec89-1::text').get()
    #print(Brand)
    
except:
    print("dome")

professions = profession.find_elements(By.XPATH, ".//*")

for profession in professions:
    print(profession.text)

print("seemore")
#seemore = driver.find_element(By.CSS_SELECTOR, ".ipc-see-more__text")

#sleep(3)
element = driver.find_element(By.CSS_SELECTOR, ".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > button:nth-child(1)")
print(element)
driver.execute_script("return arguments[0].scrollIntoView(true);", element)
sleep(3)
driver.execute_script("window.scrollBy(0, -100)") 


seemore = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > button:nth-child(1)"))
)
seemore.click()

WebDriverWait(driver, 10).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > button:nth-child(1)"))
)

works = driver.find_element(By.CSS_SELECTOR, ".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > ul:nth-child(1)")

works = works.find_elements(By.XPATH, "./*")
for index, work in enumerate(works):
    print(work.get_attribute("class"))
    work.click()
    driver.back()
    #test = work.find_element(By.TAG_NAME, "a")
    #print(test.text)
    #test.click()
    #driver.back()


#driver.back()

sleep(300)
