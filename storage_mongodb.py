from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pymongo

# Setup WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["transliteration"]
collection = db["scrape"]

# here make changes to store the scraped text
# then using mongo db input the stored text for the google translate 


i=1
text=[]
while i<=10:

    # driver.get(f'https://www.bbc.com/bengali/topics/cqywj91rkg6t?page={i}') # make the last no. dynamic
    # driver.get(f'https://www.bbc.com/bengali/topics/c907347rezkt?page={i}')  
    # driver.get(f'https://www.bbc.com/bengali/topics/cjgn7233zk5t?page={i}')
    driver.get(f'https://www.bbc.com/bengali/topics/cg7265yyxn1t?page={i}')

    # Find all the link elements below the images
    link_elements = driver.find_elements(By.XPATH,"//ul[@data-testid='topic-promos']//a ")

    for ele in link_elements:
        text = ele.text  # till now i got data on the link
        # Prepare the document to insert into MongoDB
        document = {
            "input": text.strip('"').strip("'"),
            "lang": "Bengali",  # changes for each language
        }
        collection.insert_one(document)
        

    for index in range(len(link_elements)):
        # Re-find the elements to avoid stale element reference
        link_elements = driver.find_elements(By.XPATH, "//ul[@data-testid='topic-promos']//a")
        link_elements[index].click()
    
        inner_data = driver.find_elements(By.XPATH,"//div[@dir='ltr']//p")
        for ele in inner_data:
            text = ele.text
            document = {
                "input": text.strip('"').strip("'"),
                "lang": "Bengali",  # changes for each language
            }
            collection.insert_one(document)
        driver.back()
         
        print(f"Inserted txt")
    i+=1

    # Prepare the document to insert into MongoDB
   

# print(text)
# print(len(text))
# 9 - 1115




# Close the WebDriver
driver.quit()



print("Data inserted into MongoDB")



# import pymongo

# # Connect to MongoDB server
# client = pymongo.MongoClient("mongodb://localhost:27017/")

# # Access the database named "translation_db"
# db = client["transliteration"]

# # Access the collection named "translations"
# collection = db["translations"]

# # Insert a document into the collection
# document = {
#     "input": "Hello, world!",
#     "translation": "Hola, mundo!",
#     "transliteration": "Hola, mundo!"
# }
# collection.insert_one(document)

# print("Document inserted into MongoDB")
