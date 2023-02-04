from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from math import radians, sin, cos, sqrt, atan2
from time import sleep
import re
import csv

CENTER_PARIS_COORDINATES = [48.8699181, 2.3372123]

def generate_url(addresse: str) -> str:
    url = "https://www.google.com/maps/place/" + addresse.replace(" ", "+")
    return url

def extract_coordinates(driver):
    while True:
        url = driver.current_url
        coordinates_match = re.search("@.*,", url)
        fail_safe = re.search("\/data=", url)
        if coordinates_match is None or fail_safe is None:
            sleep(0.5)
            continue
        coordinates_str = coordinates_match.group()
        coordinates_str = coordinates_str[1:-1]
        coordinates = coordinates_str.split(",")
        return float(coordinates[0]), float(coordinates[1])


def get_distance_between(coord1, coord2):
    # Convert latitude and longitude to radians
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth's radius (mean radius = 6,371km)
    R = 6371e3
    
    # Distance in meters
    distance = R * c
    return distance

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Initialisation 
driver.get("https://www.google.com/maps/")

# On clique sur e bouton "Tout accepter"
try:    
    accept_button = driver.find_element(By.XPATH, "//button[@aria-label='Tout accepter']")
    if accept_button is not None : 
        driver.execute_script("arguments[0].click();", accept_button)
except : 
    print("The accept input is not a button")

try:
    accept_input = driver.find_element(By.XPATH, "//input[@aria-label='Tout accepter']")
    if accept_input is not None : 
        driver.execute_script("arguments[0].click();", accept_input)
except : 
    print("The accept input is not an input")

restaurants = [None]
with open("data/restaurants_original.csv", "r", encoding="utf8") as f :
    csvreader = csv.DictReader(f)
    for restau in csvreader:
        adresse = restau["adress"]
        url = generate_url(adresse) 
        driver.get(url)

        sleep(1)

        search_button = driver.find_element(By.ID, "searchbox-searchbutton")
        driver.execute_script("arguments[0].click();", search_button)

        latitude, longitude = extract_coordinates(driver)
        distance = get_distance_between((latitude, longitude), CENTER_PARIS_COORDINATES)
        print(latitude, longitude, distance)
        restau["latitude"] = latitude
        restau["longitude"] = longitude
        restau["distance"] = distance
        
        if restaurants[0] is None:
            restaurants[0] = list(restau.keys())

        restaurants.append(list(restau.values()))

with open("data/restau_treated.csv", "w", encoding="utf8") as f:
    print(restaurants)
    writer = csv.writer(f)
    writer.writerows(restaurants)

driver.quit()