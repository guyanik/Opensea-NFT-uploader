import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from decouple import config

import time

from CSV import CSV
from JSON import JSON
from NFT import NFT

EXTENSION_PATH = config("EXTENSION_PATH")

RECOVERY_CODE = config("RECOVERY_CODE")

PASSWORD = config("PASSWORD")

CHROME_DRIVER_PATH = config("CHROME_DRIVER_PATH")

collection_upload_link = "https://opensea.io/collection/thelemmingssample/assets/create"


def setup_metamask_wallet(driver):
    driver.switch_to.window(driver.window_handles[0])  # focus on metamask tab
    time.sleep(10)

    driver.find_element(By.XPATH, '//button[text()="Get Started"]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//button[text()="Import wallet"]').click()
    time.sleep(1)

    driver.find_element_by_xpath('//button[text()="No Thanks"]').click()
    time.sleep(1)
    
    inputs = driver.find_elements_by_xpath("//input")
    inputs[0].send_keys(RECOVERY_CODE)
    time.sleep(1)

    inputs[1].send_keys(PASSWORD)
    inputs[2].send_keys(PASSWORD)
    time.sleep(1)

    driver.find_element_by_css_selector(".first-time-flow__terms").click()
    driver.find_element_by_xpath('//button[text()="Import"]').click()
    time.sleep(5)
    
    driver.find_element_by_xpath('//button[text()="All Done"]').click()
    time.sleep(1)


def move_to_opensea(driver):
    driver.execute_script(f'''window.open("{collection_upload_link}","_blank")''')
    driver.switch_to.window(driver.window_handles[2])
    time.sleep(5)


def signin_to_opensea(driver):
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/div/div/div[2]/ul/li[1]/button').click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[3])
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[4]/div[2]/button[2]').click()
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    time.sleep(5)

    while True:
        try:
            driver.switch_to.window(driver.window_handles[3])
            driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/button[2]').click()
            break
        except:
            driver.switch_to.window(driver.window_handles[2])
            driver.refresh()
            time.sleep(5)
    time.sleep(2)
    

def fillMetadata(driver, metadataMap: dict):
    driver.find_element_by_xpath('//div[@class="AssetFormTraitSection--side"]/button').click()
    for key in metadataMap:
        input1 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[1]/div/div/input')
        input2 = driver.find_element_by_xpath('//tbody[@class="AssetTraitsForm--body"]/tr[last()]/td[2]/div/div/input')

        input1.send_keys(str(key))
        input2.send_keys(str(metadataMap[key]))
        driver.find_element_by_xpath('//button[text()="Add more"]').click()

    time.sleep(1)
    driver.find_element_by_xpath('//button[text()="Save"]').click()


def upload(driver, nft: NFT):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(3)

    driver.find_element_by_id("media").send_keys(nft.file)
    driver.find_element_by_id("name").send_keys(nft.name)
    driver.find_element_by_id("description").send_keys(nft.description)
    time.sleep(3)

    fillMetadata(driver, nft.metadata)
    time.sleep(3)

    driver.find_element_by_xpath('//button[text()="Create"]').click()
    time.sleep(10)

    error_text = "Oops, something went wrong"
    assert error_text not in driver.page_source
    driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[1]/section/div/div/div/div/img')

    driver.execute_script(f'''location.href="{collection_upload_link}"''')

if __name__ == '__main__':
    # setup metamask
    opt = webdriver.ChromeOptions()
    opt.add_extension(EXTENSION_PATH)
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=opt)
    setup_metamask_wallet(driver)
    time.sleep(2)
    move_to_opensea(driver)
    signin_to_opensea(driver)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(7)  # todo- need to manually click on sign button for now
    data = JSON(os.getcwd() + "/data/metadata.json").readFromFile()
    for item in data:
        name = item["name"] # NAME OF YOUR FILE
        description = item["description"] # NOTE: YOU NEED TO UPDATE THIS ACCORDINGLY
        file = item["file"]
        metadata = item["attributes"]

        while True:
            try:
                upload(driver, NFT(name, description, metadata, os.getcwd() + "/data/images/" + file))
                break
            except:
                print(name)
    
    print("DONE!!!")
    driver.quit()
