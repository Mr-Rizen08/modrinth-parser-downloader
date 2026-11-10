from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

PLATFORM = {
    "fabric" : "Fabric",
    "datapack": "Data Pack",
    "neoforge": "NeoForge",
    "forge": "Forge",
    "quilt": "Quilt",
    "velocity": "Velocity",
    "bukkit": "Bukkit",
    "folia": "Folia",
    "paper": "Paper",
    "purpur": "Purpur",
    "waterfall": "Waterfall",
    "iris": "Iris",
    "resourcepack": "Resource Pack",
    "optifine": "OptiFine",
}


def get_platform(plat, driver):
    try:
        filters = driver.find_element(By.XPATH, f"//button[@data-v-96db6ef4 and contains(text(), ' {plat}')]").click()
    except NoSuchElementException:
        filters = driver.find_element(By.XPATH, "//button[@data-v-96db6ef4]").click()

def find_platform(plat, driver):
    if not plat.lower().strip() in PLATFORM:
        get_platform("Fabric", driver)
        return
    i = PLATFORM.get(plat.lower().strip())
    get_platform(i, driver)
