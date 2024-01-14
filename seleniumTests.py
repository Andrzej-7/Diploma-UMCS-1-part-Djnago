from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import string
from selenium.webdriver.common.keys import Keys
import time


def username_generator():
    words = ["apple", "banana", "cherry", "jake", "Martini"]
    word = random.choice(words)
    number = random.randint(0, 999)  
    return f"{word}{number}"


def email_generator():
    words = ["cool", "fast", "smart", "happy", "bright"]
    domains = ["example.com", "mail.com", "test.org", "demo.net","gmail.com", "outlook.com", "yahoo.com"]

    word = random.choice(words)
    domain = random.choice(domains)
    number = random.randint(1, 9999)
    email = f"{word}{number}@{domain}"

    return email



def password_generator(length, include_special_chars):
    
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation if include_special_chars else ''
    
    all_chars = lower + upper + digits + special_chars

    password = random.choice(lower) + random.choice(upper) + random.choice(digits)
    if include_special_chars:
        password += random.choice(special_chars)

   
    password += ''.join(random.choice(all_chars) for _ in range(length - len(password)))

    password = ''.join(random.sample(password, len(password)))

    return password




def register_user(driver, username, password_length=12, include_special_chars=True):


    time.sleep(1)
    username_element = driver.find_element(By.XPATH, '//*[@id="id_username"]')
    username_element.send_keys(username)

    time.sleep(1)
    email_element = driver.find_element(By.XPATH, '//*[@id="id_email"]')
    email = email_generator()
    email_element.send_keys(email)

    time.sleep(1)
    password_element1 = driver.find_element(By.XPATH, '//*[@id="id_password1"]')
    password = password_generator(password_length, include_special_chars)
    password_element1.send_keys(password)

    time.sleep(1)
    password_element2 = driver.find_element(By.XPATH, '//*[@id="id_password2"]')
    password_element2.send_keys(password)

    time.sleep(1)
    register_button = driver.find_element(By.XPATH, '/html/body/div/form/div[5]/button')
    register_button.send_keys(Keys.ENTER)



def account_logOut():
    headerEmail = driver.find_element(By.XPATH, '/html/body/header/div/div/div/button')
    logOutButton = driver.find_element(By.XPATH, '/html/body/header/div/div/div/div/a[2]')


driver = webdriver.Firefox()

driver.get("http://127.0.0.1:8000/register/")

#weak password
username = username_generator()
register_user(driver,username, 4, True)

#already used username
time.sleep(1)
username = "test12" #already used username
register_user(driver,username, 12, True)

#good case reistration
time.sleep(1)
username = username_generator()
register_user(driver,username, 12, True)


time.sleep(1)
account_logOut()