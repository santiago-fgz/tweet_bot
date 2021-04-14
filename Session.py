import csv
from getpass import getpass
from time import sleep
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver #
from selenium.webdriver.support import expected_conditions as EC #
from selenium.webdriver.common.by import By #
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait #

class Session:
    def __init__(self,username,password,sleep_time=2):
        self.username = username
        self.password = password
        self.sleep_time = sleep_time
        options = EdgeOptions()
        options.use_chromium = True
        self.driver = Edge(options=options)
    
    def login(self):
        self.driver.get("https://www.twitter.com/login")
        sleep(self.sleep_time)
        u_name = self.driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        u_name.send_keys(self.username)
        p_word = self.driver.find_element_by_xpath('//input[@name="session[password]"]')
        p_word.send_keys(self.password)
        p_word.send_keys(Keys.RETURN)
        sleep(self.sleep_time)

    def tweet_selection(self,search_str,csv_tit,max_tweets=300):
        sleep(self.sleep_time)
        search_input = self.driver.find_element_by_xpath('//input[@aria-label="Search query"]')
        search_input.clear()
        search_input.send_keys(search_str)
        search_input.send_keys(Keys.RETURN)
        sleep(self.sleep_time)
        data = []
        tweet_ids = set()
        last_pos = self.driver.execute_script("return window.pageYOffset;")
        scrolling = True
        while scrolling:
            cards = self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
            for card in cards[-15:]:
                tweet = self.get_tweet_data(card)
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)
            scroll_attempt = 0
            while True:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(self.sleep_time)
                curr_pos = self.driver.execute_script("return window.pageYOffset;")
                if last_pos == curr_pos:
                    scroll_attempt += 1
                    if scroll_attempt >= 3:
                        scrolling = False
                        break
                    else:
                        sleep(2*self.sleep_time)
                else:
                    last_pos = curr_pos
                    break
        with open(csv_tit,'w',encoding="utf-8") as out:
            csv_out=csv.writer(out)
            csv_out.writerow(['user','date','text','quoting','reply count','retweet count','like count'])
            for row in data:
                csv_out.writerow(row)

    def get_tweet_data(self,card):
        user = card.find_element_by_xpath('.//span[contains(text(),"@")]').text
        try:
            date = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        text = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        reply_count = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        retweet_count = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        like_count =card.find_element_by_xpath('.//div[@data-testid="like"]').text
        tweet = (user,date,text,responding,reply_count,retweet_count,like_count)
        return tweet
    
    def tweet(self,tuit): # REQUIERE INTERACTUAR CON EDGE
        sleep(self.sleep_time)
        tuit_input = self.driver.find_element_by_xpath('//div[@data-testid="tweetTextarea_0"]')
        tuit_input.clear()
        tuit_input.send_keys(tuit)
        # NO HACER ESTO PQ TE BANNEAN 
        # RIP a alienconalas1
        #tuit_btn = self.driver.find_element_by_xpath('//div[@data-testid="tweetButtonInline"]') 
        #tuit_btn.click()

