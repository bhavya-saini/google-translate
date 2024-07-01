from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import pymongo
import logging
import os



# Configure logging
logging.basicConfig(filename='translation.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://bhavyasaini2005:Qwerty1120@cluster0.zc0dxik.mongodb.net/")
db = client["Transliteration"]
scrape_collection = db["bengali"]
translations_collection = db["Translations"]

# total_documents = scrape_collection.count_documents({})
start_point = 26000  # Start from the 404th document

# Fetch the next 1000 texts from the 'scrape' collection, starting from position 11
text = scrape_collection.find().skip(start_point).limit(100)

# Load last processed index
checkpoint_file = 'checkpoint.txt'
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        last_processed_index = int(f.read().strip())
else:
    last_processed_index = start_point

# Open site
driver.get('https://www.google.com/search?q=translate&oq=tr&gs_lcrp=EgZjaHJvbWUqDggAEEUYJxg7GIAEGIoFMg4IABBFGCcYOxiABBiKBTIGCAEQRRhAMg4IAhBFGDkYQxiABBiKBTIGCAMQRRg8MgYIBBBFGDwyBggFEEUYPDIGCAYQRRg8MgYIBxBFGDzSAQc2MDNqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8')

for index, tt in enumerate(text, start=start_point):
    if index < last_processed_index:
        continue  # Skip already processed documents

    input_text = tt["input"]
    retries = 3
    success = False

    while retries > 0 and not success:
        try:
            # Ensure the element is enabled
            input_element = driver.find_element(By.ID, "tw-source-text-ta")   # id of textarea
            if input_element.is_enabled():
                input_element.clear()
                input_element.send_keys(input_text)
            else:
                logging.error(f"Element is disabled for input: {input_text}")
                break

            time.sleep(3)

            translation = driver.find_element(By.XPATH, "//div[@id='tw-target-text-container']")
            translation_text = translation.text.strip('"').strip("'")

            transliteration = driver.find_element(By.XPATH, "//div[contains(@id,'tw-source-rmn')]")
            transliteration_text = transliteration.text.strip('"').strip("'")

            document = {
                "input": input_text,
                "lang": tt["lang"],           
                "translation": translation_text,
                "transliteration": transliteration_text
            }

            # Insert the document into MongoDB
            translations_collection.insert_one(document)
            logging.info(f"Successfully processed document index: {index}")
            success = True

        except Exception as e:
            logging.error(f"Error processing document index {index}: {e}")
            retries -= 1
            time.sleep(5)  # Wait before retrying

    if not success:
        logging.error(f"Failed to process document index {index} after retries")

    # Save checkpoint
    with open(checkpoint_file, 'w') as f:
        f.write(str(index))

driver.quit()
print("Translation completed")
