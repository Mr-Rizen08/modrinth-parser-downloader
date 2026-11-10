from mods_platform import find_platform
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core import BROWSERS
from service.saver import SaverBase, SaveToFile

URL = "https://modrinth.com/"
URL2 = "https://modrinth.com"

driver = BROWSERS()
driver.get(URL)
start = driver.find_element(By.XPATH, "//a[@data-v-48d6e828]")
start.click()

while True:
    functions = input("What function do you need? [parser/downloader or stop]")
    if functions.lower().strip() == "downloader":
        section = input("What section do you need ? [mods, modpacks, plugins, shaders, datapacks or resourcepacks]")
        name = input("What is the name?")
        version = input("minecraft version ?")
        platforms = input("""What platform ?[mods/modpacks: quilt, forge, neoforge, fabric; shaders: iris, optifine;
                    plugins: bungeecord, velocity, bukkit, folia, paper, purpur, waterfall; 
                    datapacks: datapack; resourcepacks: resourcepack; ]""")
    elif functions.lower().strip() == "parser":
        choice = input(f"Формат ({'/'.join(SaverBase.available())}): ").strip().lower()
        section = input("What section do you need ? [mods, modpacks, plugins, datapacks or resourcepacks]")
        page = input('How many pages do you need? [1,max or your value]')
        element_number = input("How many elements do you need [3-96], but you can use 100(it can sometimes give error)")
        formate = input("What format do you need? [json or excel]")
        file_name = input("File name:")
    else:
         break


    def download_mod(name, ver, plat):
        search = driver.find_element(By.CSS_SELECTOR, 'input.h-12')
        search.send_keys(name)
        time.sleep(1)
        mod = driver.find_element(By.CSS_SELECTOR, "article.project-card")
        mod_link = mod.find_element(By.CSS_SELECTOR, "a.icon").get_attribute("href")
        driver.get(mod_link)
        select = driver.find_element(By.XPATH, "//a[contains (@class, 'button-animation')][span[contains (text(), 'Version')]]").get_attribute("href")
        driver.get(select)
        time.sleep(1)
        game_ver = driver.find_element(By.XPATH, "//button[@data-v-02e335bf and contains(normalize-space(text()), 'Game versions')]").click()
        time.sleep(1)
        search_ver = driver.find_element(By.ID, "search-input")
        search_ver.send_keys(ver+Keys.ENTER)
        time.sleep(1)
        find_platform(plat, driver)
        time.sleep(1)
        download_link= driver.find_element(By.CSS_SELECTOR, "a.absolute").get_attribute("href")
        driver.get(download_link)
        download = driver.find_element(By.XPATH, "//a[@data-v-7a9bd08b]").get_attribute("href")
        driver.get(download)
        driver.get(URL)
        time.sleep(10)

    def get_mods():
        data = []
        time.sleep(2)
        mods = driver.find_elements(By.CSS_SELECTOR, "article.project-card")
        time.sleep(2)
        for mod in mods:
            name = mod.find_element(By.CSS_SELECTOR, "h2.name").text
            description = mod.find_element(By.CSS_SELECTOR, "p.description").text
            try:
                enviroment = mod.find_element(By.CSS_SELECTOR, "span.environment").text
            except NoSuchElementException:
                enviroment = None
            if enviroment:
                categories =  mod.find_element(By.CSS_SELECTOR, ".categories.tags").find_elements(By.TAG_NAME, "span")[1:]
            else:
                categories = mod.find_element(By.CSS_SELECTOR, ".categories.tags").find_elements(By.TAG_NAME, "span")

            tags = [
                tag.text
                for tag in categories
            ]

            info = mod.find_elements(By.CSS_SELECTOR, "div.stat")
            downloads = info[0].text
            likes = info[1].text
            last_update = info[2].text
            link = URL2 + mod.find_element(By.TAG_NAME, "a").get_attribute("href")
            try:
                img = mod.find_element(By.TAG_NAME, "img").get_attribute("src")
            except NoSuchElementException:
                img = None
            data.append({
                "Name": name,
                "Description": description,
                "Enviroment":enviroment,
                "Tags": tags,
                "Download": downloads,
                "Likes": likes,
                "Last_update": last_update,
                "Link":link,
                "Img": img
            })
        return data

    def get_pages():
        time.sleep(2)
        data = []
        if page == "max":
            try:
                page_max = driver.find_element(By.XPATH, "//div[contains(@class,'page-number shrink')]/div[contains(@class,'btn-wrapper')]/a[@data-v-2aff609e-s]").text
            except NoSuchElementException:
                page_max = driver.find_element(By.XPATH,"//div[contains(@class,'page-number shrink')]/div[contains(@class,'btn-wrapper')]/button[@data-v-2aff609e-s]").text
            pages = int(page_max)
            for pag in range(1, pages + 1):
                time.sleep(1)
                mods = get_mods()
                try:
                    new_page = driver.find_element(By.XPATH,f"//div[contains(@class,'page-number page-number-container')]/div[contains(@class,'btn-wrapper')]/a[contains(text(), '{pag+1}')]").click()
                except NoSuchElementException:
                    new_page = driver.find_element(By.XPATH,f"//div[contains(@class,'page-number page-number-container')]/div[contains(@class,'btn-wrapper')]/button[contains(text(), '{pag + 1}')]").click()
                data.append({
                    "Page Number": pag,
                    "Mods": mods
                })

            return data

        elif int(page) > 1:
            pag = int(page)
            for i in range(1, pag + 1):
                time.sleep(1)
                mods = get_mods()
                try:
                    new_page = driver.find_element(By.XPATH,f"//div[contains(@class,'page-number page-number-container')]/div[contains(@class,'btn-wrapper')]/a[contains(text(), '{i + 1}')]").click()
                except NoSuchElementException:
                    new_page = driver.find_element(By.XPATH,f"//div[contains(@class,'page-number page-number-container')]/div[contains(@class,'btn-wrapper')]/button[contains(text(), '{i + 1}')]").click()
                data.append({
                    "Page Number": i,
                    "Mods": mods
                })

            return data

    def get_driver(name, number):
        if functions.lower().strip() == "downloader":
            sections = driver.find_element(By.XPATH,f"//a[contains (@class, 'button-animation')][span[contains (text(), '{name}')]]").get_attribute("href")
            driver.get(sections)
        elif functions.lower().strip() == "parser":
            sections = driver.find_element(By.XPATH,f"//a[contains (@class, 'button-animation')][span[contains (text(), '{name}')]]").get_attribute("href")
            driver.get(sections + f"?m={number}")
        else:
            raise TypeError("You did something wrong")


    def main():
        time.sleep(1)
        if functions.lower().strip() == "downloader":
            if section.lower().strip() == "mods":
                download_mod(name, version, platforms)
            elif section.lower().strip() == "modpacks":
                get_driver(section.title().strip(), None)
                download_mod(name, version, platforms)
            elif section.lower().strip() == "shaders":
                get_driver(section.title().strip(), None)
                download_mod(name, version, platforms)
            elif section.lower().strip() == "resourcepacks":
                get_driver(section[:8].title().strip()+" "+section[8:].title().strip(), None)
                download_mod(name, version, platforms)
            elif section.lower().strip() == "datapacks":
                get_driver(section[:4].title().strip()+" "+section[4:].title().strip(), None)
                download_mod(name, version, platforms)
            elif section.lower().strip() == "plugins":
                get_driver(section.title().strip(), None)
                download_mod(name, version, platforms)
            else:
                raise TypeError("You did something wrong")
        elif functions.lower().strip() == "parser":
            if section.lower().strip() == "mods":
                get_driver(section.title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            elif section.lower().strip() == "modpacks":
                get_driver(section.title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            elif section.lower().strip() == "shaders":
                get_driver(section.title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            elif section.lower().strip() == "resourcepacks":
                get_driver(section[:8].title().strip() + " " + section[8:].title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            elif section.lower().strip() == "datapacks":
                get_driver(section[:4].title().strip() + " " + section[4:].title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            elif section.lower().strip() == "plugins":
                get_driver(section.title().strip(), element_number)
                if page == "max" or int(page) > 1:
                    data = get_pages()
                else:
                    get_mods()
                    data = get_mods()
            else:
                raise TypeError("You did something wrong")

            saver = SaverBase.create1(choice)

            SaveToFile(saver, data).save("mods")

    if __name__ == "__main__":
        main()
