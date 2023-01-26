import json
import phonenumbers
import string
import time
from random import randint, choices, shuffle, choice
from random_username.generate import generate_username
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def generate_password():
    password = []
    pass_len = randint(10, 20)
    special_symbols = '!?+-*%$#@'
    symbol_groups = (string.ascii_lowercase, string.ascii_uppercase, special_symbols, special_symbols)
    symbol_range = string.ascii_lowercase + string.ascii_uppercase + string.digits + special_symbols
    # Adding one of the special symbol
    for group in symbol_groups:
        password.append(choice(group))
    # Filling rest password length with random symbols
    password.extend(choices(symbol_range, k=pass_len - len(symbol_groups)))
    # Mixing sequence of the symbols in the password
    shuffle(password)
    return "".join(password)


options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Driver for docker
driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)

# # Driver for dev
# driver = webdriver.Chrome(service=Service('../chromedriver'), options=options)

url = 'https://www.fastmail.com/'

driver.get(url)

user_data = {'email': generate_username()[0].lower() + '@fastmail.com',
             'password': generate_password()
             }

# Sign up to fastmail
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "round-link-btn"))).click()
time.sleep(5)

# Fill the required fields (username, email, password)
driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div/div/div[1]/div/div/form/div[1]/input"
).send_keys(user_data.get('email'))

driver.find_element(
    By.XPATH,
    '/html/body/div[2]/div/div/div/div/div[1]/div/div/form/fieldset/div[2]/div[1]/input'
).send_keys(user_data.get('email'))

time.sleep(5)

driver.find_element(
    By.XPATH,
    "/html/body/div[2]/div/div/div/div/div[1]/div/div/form/p[1]/div/div/input"
).send_keys(user_data.get('password'))

time.sleep(5)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH,
    '/html/body/div[2]/div/div/div/div/div[1]/div/div/form/p[3]/button'
))).click()

time.sleep(10)


# Phone number verification
phone_number_status = False
while not phone_number_status:
    try:
        phone_number = input('\033[31m' + "Enter Phone Number ex.(+1232566465654) for Verification: " + '\033[0m')
        phone_number_status = phonenumbers.parse(phone_number)
        phone_number_status = phonenumbers.is_possible_number(phone_number_status)
    except Exception:
        pass

driver.find_element(
    By.XPATH,
    '/html/body/div[2]/div/div/div/div/div[1]/div/div/div/div/fieldset/div/div[2]/input'
).send_keys(phone_number)

time.sleep(5)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH,
    '/html/body/div[2]/div/div/div/div/div[1]/div/div/div/div/button'
))).click()

# Providing the site with verification code
confirmation_code = input('\033[31m' + "Enter received confirmation code: " + '\033[0m')

driver.find_element(By.XPATH,
                    '/html/body/div[2]/div/div/div/div/div[1]/div/div/div/div/fieldset/div/div[2]/input'
                    ).send_keys(confirmation_code)
time.sleep(5)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
    By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/div/div/div/div/button'
))).click()


# Adding new user data to the file
json_data = json.dumps(user_data, indent=4)
with open('email_accounts_data.json', 'w') as file:
    file.write(json_data)
