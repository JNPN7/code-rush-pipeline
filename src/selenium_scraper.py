from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from time import sleep, time
import re
import json

from models.movie import Movie
from models.celeb import Celeb


class SeleniumScraper:

    def __init__(self):
        self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        self.driver.get("https://www.imdb.com")
        self.wait = WebDriverWait(self.driver, 10)


    def __scroll_to_element(self, element):
        self.driver.execute_script("return arguments[0].scrollIntoView(true);", element)
        sleep(1)
        self.driver.execute_script("window.scrollBy(0, -150)")


    def __scroll_to_element_using_css_selector(self, css_selector: str):
        element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
        self.__scroll_to_element(element)


    def __click_element(self, css_selector: str):
        element = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()


    def __wait_until_invisible(self, css_selector: str):
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )


    def __search_celeb(self, celeb_name: str):
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys(celeb_name)
        search.send_keys(Keys.RETURN)


    def __get_element(self, css_selector: str):
        try: 
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
            return element
        except:
            raise TimeoutError("Couldn't get element'")


    def __check_is_movie(self, year):
        has_number = bool(re.search(r'\d', year))
        if has_number:
            return year, "Movie"
        else:
            return self.__get_element(".sc-8c396aa2-0 > li:nth-child(2) > span:nth-child(2)").get_attribute("innerHTML"), year


    def __get_movie_info_after_inside_page(self):
        name = self.__get_element(".sc-b73cd867-0").text
        year = self.__get_element(".sc-8c396aa2-0 > li:nth-child(1)").text
        year, typ = self.__check_is_movie(year)

        rating = self.__get_element(".sc-849ec3ff-12 > div:nth-child(1) > div:nth-child(1) > a:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1)").get_attribute("innerHTML")
        try :
            director = self.__get_element("ul.ipc-metadata-list:nth-child(3) > li:nth-child(1) > div:nth-child(2) > ul:nth-child(1) > li:nth-child(1) > a:nth-child(1)").text
        except:
            director = "" 

        genre_elements = self.__get_element(".ipc-chip-list--baseAlt > div:nth-child(2)") 
        genre_elements = genre_elements.find_elements(By.XPATH, "./*")
        genre = []
        for genre_element in genre_elements:
            genre.append(genre_element.text)

        return Movie(name, typ, year, rating, director, genre)


    def get_celeb_info(self, celeb_name: str):
        self.__search_celeb(celeb_name)
        ## get to celebrity page
        self.__click_element("li.find-name-result:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)")

        name = self.__get_element(".sc-856aec89-0").text

        ## get all the profession of celebrity
        professions_element = self.__get_element(".sc-856aec89-4")
        professions_element = professions_element.find_elements(By.XPATH, "./*")
        professions = []
        for profession in professions_element:
            professions.append(profession.text)

        ## see all works
        see_more_css = ".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > button:nth-child(1)" 
        self.__scroll_to_element_using_css_selector(see_more_css)
        self.__click_element(see_more_css)
        self.__wait_until_invisible(see_more_css)

        ## get all works
        #TODO need better logic this is bit clumsy
        works_element = self.__get_element(".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > ul:nth-child(1)")
        works_element = works_element.find_elements(By.XPATH, "./*")
        total_works = len(works_element)
        print(f"{total_works} no of works")

        works = []
        for i in range(total_works):
            works_element = self.__get_element(".ipc-accordion__item--expanded > div:nth-child(4) > div:nth-child(1) > ul:nth-child(1)")
            works_element = works_element.find_elements(By.XPATH, "./*")
            self.__scroll_to_element(works_element[i])
            works_element[i].click()

            #TODO keep logics to scrape the data from the page
            sleep(1)
            work = self.__get_movie_info_after_inside_page()
            works.append(work)

            self.driver.back()

        celeb = Celeb(name, professions, works)
        return celeb



if __name__ == "__main__":
    t0 = time()
    scraper = SeleniumScraper()
    t1 = time()
    celeb = scraper.get_celeb_info("Nataline Portman")
    celeb.store()
    t2 = time()
    print(f"total time taken: {t2-t0}s | {(t2-t0)/60}m")
