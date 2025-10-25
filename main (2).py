import time
import json

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "https://modrinth.com/"
URL2 = "https://modrinth.com"
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
        section = input("What section do you need ? [mods, modpacks, plugins, datapacks or resourcepacks]")
        page = input('How many pages do you need? [1,max or your value]')
        element_number = input("How many elements do you need [3-96], but you can use 100(it can sometimes give error)")
        formate = input("What format do you need? [json or excel]")
        file_name = input("File name:")
    else:
         break




    driver = webdriver.Chrome()
    driver.get(URL)
    start = driver.find_element(By.XPATH, "//a[@data-v-48d6e828]")
    start.click()

    def get_platform(plat):
        try:
            filters= driver.find_element(By.XPATH, f"//button[@data-v-96db6ef4 and contains(text(), ' {plat}')]").click()
        except NoSuchElementException:
            filters = driver.find_element(By.XPATH, "//button[@data-v-96db6ef4]").click()


    def find_platform(plat):
        if plat.lower().strip() == "fabric":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "datapack":
            get_platform(plat[:4].title().strip() + " " + plat[4:].title().strip())
        elif plat.lower().strip() == "neoforge":
            get_platform(plat[:3].title().strip() + plat[3:].title().strip())
        elif plat.lower().strip() == "forge":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "quilt":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "velocity":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "bukkit":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "folia":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "paper":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "purpur":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "waterfall":
            get_platform(plat.title().strip())
        elif plat.lower().strip() == "bungeecord":
            get_platform(plat[:6].title().strip() + plat[6:].title().strip())
        elif plat.lower().strip() == "iris":
            get_platform(plat.title())
        elif plat.lower().strip() == "optifine":
            get_platform(plat[:4].title().strip() + plat[4:])
        elif plat.lower().strip() == "resourcepack":
            get_platform(plat[:8].title().strip() + " " + plat[8:].title().strip())


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
        find_platform(plat)
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

    def save_to_exel(data:list, name):
        df = pd.DataFrame(data)
        df.to_excel(f"{name}.xlsx", index=False)
        print("Done")

    def save_to_json(data:list, name):
        with open(f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Done")

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

    def choose_format(data):
        if formate.lower().strip() == "json":
            save_to_json(data, file_name)
        elif formate.lower().strip() == "excel":
            save_to_exel(data, file_name)


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

            choose_format(data)
    if __name__ == "__main__":
        main()
