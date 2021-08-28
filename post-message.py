# Standard Library Modules
import time
import logging

# Third Party Modules
from selenium import webdriver
from selenium.webdriver.common.by import By

# TODO: Implement Selenium Waits instead of time.sleep()
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC


def get_credentials():
    account_email_address = input("Enter your facebook account's email address: ")
    account_password = input("Enter your password: ")
    return account_email_address, account_password

def sleep(timeout=5):
    time.sleep(timeout)

def prepare_browser(browser="chrome"):
    if (browser == "chrome"):
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(options=chrome_options)
        logging.info("Browser {0} is prpared and ready!".format(browser))
        return driver
    else:
        logging.error("Unsupported browser type: ".format(browser))
        return False

def login_to_facebook(web_driver, account_email_address, account_password):
    try:
        web_driver.get("https://www.facebook.com")
        sleep()
        email_element = web_driver.find_element(By.XPATH,'//*[@id="email"]')
        email_element.send_keys(account_email_address)
        password_element = web_driver.find_element(By.XPATH,'//*[@id="pass"]')
        password_element.send_keys(account_password)
        password_element.submit()
        sleep()
        logging.info("Logged into Facebook!")  
    except Exception as unexpected_error:
        logging.error("Failed to login to Facebook!")
        logging.error("Unexpected, unhandled exception has occurred! \n{0}".format(unexpected_error))
    
    return web_driver

def post_message_in_groups(web_driver, facebook_groups, message):
    for group in facebook_groups:
        try:
            web_driver.get(group)
            sleep()
            
            postbox_full_xpath = \
                '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]' \
                    '/div[1]/div[4]/div/div/div/div/div[1]/div[1]/div/div' \
                        '/div/div[1]/div/div[1]/span'
            postbox = web_driver.find_element_by_xpath(postbox_full_xpath)
            postbox.click()
            sleep()
            
            active_post_area = web_driver.switch_to_active_element()
            active_post_area.send_keys(message)
            sleep()
            
            post_button_full_xpath = \
                '/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]' \
                    '/div/div[2]/div/div/div/div/div[1]/form/div/div[1]' \
                        '/div/div/div[1]/div/div[3]/div[2]/div/div'
            post_button = web_driver.find_element_by_xpath(post_button_full_xpath)
            post_button.click()
            sleep()
            
            logging.info("Posted message on group: {0}".format(group))   

        except Exception as unexpected_error:
            logging.error("Message was not posted on group: {0}".format(group))
            logging.error("Unexpected, unhandled exception has occurred: \n{0}".format(unexpected_error))

def main():
    # Set up Facebook login account name and password
    user, password = get_credentials()

    # Set up Facebook groups to post, you must be a member of the group
    groups_links_list = []

    # Set up text content to post
    message = ""

    driver = prepare_browser()
    driver = login_to_facebook(driver, user, password)
    post_message_in_groups(driver, groups_links_list, message)
    driver.close()

if __name__ == '__main__':
  main()
