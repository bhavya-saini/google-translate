
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import pandas as pd
import pymongo

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["transliteration"]
scrape_collection = db["scrape_bengali"]
translations_collection = db["translations"]

# text = scrape_collection.find({}, {"_id": 0, "input": 1, "lang": 1}).limit(1)

total_documents = scrape_collection.count_documents({})
start_point = 26000  # Start from the 404th document

# Fetch the next 1000 texts from the 'scrape' collection, starting from position 11
text = scrape_collection.find().skip(start_point).limit(1000)

# for tt in text:
#     input_text = tt["input"]

#     driver.get('https://www.google.com/search?q=translate&oq=tr&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIGCAEQRRhAMg4IAhBFGDkYQxiABBiKBTIGCAMQRRg8MgYIBBBFGDwyBggFEEUYPDIGCAYQRRg8MgYIBxBFGDzSAQc2MDNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8')

#     # Ensure the element is enabled
#     input_element = driver.find_element(By.ID, "tw-source-text-ta")   #id of textarea
#     if input_element.is_enabled():
#         input_element.send_keys(input_text)
#     else:
#         print("Element is disabled")

#     time.sleep(2)

#     translation = driver.find_element(By.XPATH, "//div[@id='tw-target-text-container']")
#     translation_text = translation.text.strip('"').strip("'")

#     transliteration = driver.find_element(By.XPATH,"//div[contains(@id,'tw-source-rmn')]")
#     transliteration_text = transliteration.text.strip('"').strip("'")


#     document = {
#         "input": input_text,
#         "lang": tt["lang"],           
#         "translation": translation_text,
#         "transliteration": transliteration_text
#     }

# # Insert the document into MongoDB
#     translations_collection.insert_one(document)
    

#open site
driver.get('https://www.google.com/search?q=translate&oq=tr&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIGCAEQRRhAMg4IAhBFGDkYQxiABBiKBTIGCAMQRRg8MgYIBBBFGDwyBggFEEUYPDIGCAYQRRg8MgYIBxBFGDzSAQc2MDNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8')

for tt in text:
    input_text = tt["input"]
    # Ensure the element is enabled
    input_element = driver.find_element(By.ID, "tw-source-text-ta")   #id of textarea
    if input_element.is_enabled():
        # input_element.clear()  # can be cleared after transliteration
        input_element.send_keys(input_text)
    else:
        print("Element is disabled")

    time.sleep(3)

    translation = driver.find_element(By.XPATH, "//div[@id='tw-target-text-container']")
    translation_text = translation.text.strip('"').strip("'")

    transliteration = driver.find_element(By.XPATH,"//div[contains(@id,'tw-source-rmn')]")
    transliteration_text = transliteration.text.strip('"').strip("'")
    

    document = {
        "input": input_text,
        "lang": tt["lang"],           
        "translation": translation_text,
        "transliteration": transliteration_text
    }

# Insert the document into MongoDB
    translations_collection.insert_one(document)
    input_element.clear()

driver.quit()
print("Translated")


