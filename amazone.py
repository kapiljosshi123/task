import undetected_chromedriver as uc
import aspose.words as aw
from selenium.webdriver.common.by import By
import time,urllib,requests
from PIL import Image
from pytesseract import pytesseract



url= 'https://www.amazon.com/errors/validateCaptcha'

path_to_tesseract =r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

driver= uc.Chrome()
driver.get(url)

time.sleep(2)

a=driver.find_element(By.XPATH,'//div[@class="a-row a-text-center"]/img')


filepath = '0001.jpg' 



image  =a.get_attribute('src')


urllib.request.urlretrieve(image,filepath)

img = Image.open(filepath)

pytesseract.tesseract_cmd = path_to_tesseract

text = pytesseract.image_to_string(img)

# Displaying the extracted text
p_text =text[:-1].replace('\n','')
try:driver.find_element(By.XPATH,'//input[@id="captchacharacters"]').send_keys(p_text)
except:driver.find_element(By.XPATH,'//input[@id="captchacharacters"]').send_keys(p_text)
try:driver.find_element(By.XPATH,'//button[@type="submit"]').click()
except:
    driver.find_element(By.XPATH,'//input[@id="captchacharacters"]').send_keys(p_text)
    driver.find_element(By.XPATH,'//button[@type="submit"]').click()
