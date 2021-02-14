import random
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import os
import sys
import time
import requests


audioToTextDelay = 10
delaytime = 2
audioFile = "\\payload.mp3"

URL = 'https://www.youtube.com/c/MixtapeMadnessOfficial/about'
SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'
firstTime = True
pathToEmailButton = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[4]/table/tbody/tr[1]/td[3]/ytd-button-renderer/a'
audioBtnFound = False
audioBtnIndex = -1
captchaPassed = False

myProxy = ''

def setupDriver():
        
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option("useAutomationExtension", False)
    chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    chromeOptions.add_argument('--disable-notifications')  
    chromeOptions.add_argument("window-size=1280,800")
    chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36")

    driver = webdriver.Chrome(chrome_options=chromeOptions)

    return driver

def delay():
    time.sleep(random.randint(2,3))

def audioToText(audioFile):
    global firstTime
    driver.execute_script('''window.open("", "_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()

    if(firstTime):
        foo = input('First time done\n')
        firstTime = False

    audioInput = driver.find_element_by_xpath('//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element_by_xpath('//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element_by_xpath('//*[@id="root"]/div/div[7]/div/div/div/span')
    
    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def human_type(element, text):
    for char in text:
        time.sleep(random.uniform(0.05,0.85))
        element.send_keys(char)

def findAudioButton():
    global audioBtnFound
    global audioBtnIndex

    g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    outerIframe.click()

    iframes = driver.find_elements_by_tag_name('iframe')

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delaytime)
        try:
            audioBtn = driver.find_element_by_id("recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

def checkIfPassed():
    driver.switch_to.default_content()
    g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
    driver.switch_to.frame(outerIframe)
    tester = driver.find_element_by_id('recaptcha-anchor').get_attribute('class')
    if 'recaptcha-checkbox-checked' in tester:
        return True
    else:
        return False


try:
    driver = setupDriver()
    driver.get(URL)
except Exception as e:
    print(e)
    sys.exit('Need to update the chromedriver.exe')

foo = input('Get Started\n')

driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[1]/div[4]/table/tbody/tr[1]/td[3]/ytd-button-renderer/a').click()

time.sleep(random.uniform(0.85,1.5))

findAudioButton()

if audioBtnFound:
    try:
        while True:
            # get the mp3 audio file
            src = driver.find_element_by_id('audio-source').get_attribute("src")
            print("[INFO] Audio src is: %s" % src)

            # download teh mp3 audio file from source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech to Text Conversion
            key = audioToText( os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key is: %s" % key)

            # driver.switch_to_default_content()
            driver.switch_to.default_content()

            iframe = driver.find_elements_by_tag_name("iframe")[audioBtnIndex]
            driver.switch_to.frame(iframe)
            # driver.switch_to_frame(iframe)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            human_type(inputField, key)


            delay() 
            inputField.send_keys(Keys.ENTER)
            time.sleep(2)
            if(checkIfPassed()):
                print('found')
                break
            else:
                print('not found')
                driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name("iframe")[audioBtnIndex]
            driver.switch_to.frame(iframe)

    except Exception as e:
        print(e)
        sys.exit("[INFO] possibly blocked by google. Change IP, use proxy method for requests")
else:
    sys.exit("[INFO] Audio Button not found")

driver.switch_to.default_content()  
count = 0
while True:
    count+=1
    try:
        driver.find_element_by_id('submit-btn').click()
        email_position = driver.find_elements_by_id('email')[3]
        if(email_position):
            break
        else:
            time.sleep(random.uniform(0.25,0.75))
        if(count > 5):
            break
    except Exception as e:
        print('whoops went left')

driver.find_element_by_id('submit-btn').click()
email_position = driver.find_elements_by_id('email')[3]
email = email_position.get_attribute("innerHTML")
