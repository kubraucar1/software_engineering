import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from twitter_user_info import username,password
from selenium.webdriver.common.keys import Keys
#####"
"""
from selenium.webdriver.chrome.options import Options
ayarlar = Options()
ayarlar.add_argument("--headless")
driver = webdriver.Chrome(options=ayarlar)
"""
driver=webdriver.Chrome()

def twitter_func():
    try:
        twitter_home_page="https://twitter.com/"
        driver.get(twitter_home_page)
        driver.implicitly_wait(3)

        driver.maximize_window()

        sign_in=driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/a")
        sign_in.click()

        
        username_input=driver.find_element(By.XPATH,"//input[@autocomplete='username']")  # Get username field
        username_input.send_keys(username)   #Enter your valid username or email or phone number

        next_btn=driver.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div")
        next_btn.click()

        driver.implicitly_wait(5)
        password_input=driver.find_element(By.XPATH,"//input[@autocomplete='current-password']")
        password_input.send_keys(password)  #Enter your valid password

        login_btn=driver.find_element(By.XPATH,"//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div")
        login_btn.click()
    except Exception as e:
        print(e)

def search_tweets(hastag):
    search_input=driver.find_element(By.XPATH,"//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
    search_input.send_keys(hastag)
    time.sleep(2)
    search_input.send_keys(Keys.ENTER)
   



def get_tweets():
    time.sleep(10) 
    tweets = []
    dates=[]
    result = False
        
    
    last_height = driver.execute_script("return document.body.scrollHeight")

    last_elem=''
    current_elem=''
    scroolCount=0

    while True:
        
        if(scroolCount>20):
            break
        
        scroolCount+=1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(6)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        
        all_tweets = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

        for item in all_tweets[1:]: 
            

            print('--------------------------------------------------------------------------------------')
            #contains tweet text
            try:
                text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text 
                             
            except:
                text = '[empty]'
            print(text)

            #contains tweet ' date
            try:
                date = item.find_element(By.XPATH, './/time').text
            except:
                date = '[empty]'
            print(date)

            
            #contains user name
            try:
                user_name = item.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[6]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
            except:
                user_name = '[empty]'
         
            print(user_name)

            #contains tweet's like count
            try:
                like_count=item.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[4]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/span/span').text
                if(like_count.isspace):
                    like_count="sıfır begeni"
            except:
                like_count="error like count!"
            print(like_count)
            
            #contains tweet's comment count
            try:
                comment_count=item.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[4]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[1]/div/div/div[2]/span/span/span").text
            except:
                comment_count="error comment count!"
            print(comment_count)

            try:
                retweet_count= item.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[8]/div/div/article/div/div/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]').text
            except:
                retweet_count="error retweet count !"
            print(retweet_count)
            try:
                view_count = item.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[3]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span').text
            except:
                view_count = 999999999
            print(view_count)

            tweets.append([ text, user_name, date,like_count,comment_count,retweet_count,view_count])
            

                
            if (last_elem == current_elem):
                result = True
            else:
                last_elem = current_elem
    df = pd.DataFrame(tweets, columns=['Text', 'User Name', 'Date of Tweet', 'Like Count',"Comment Count","retweet Count","View count"])
    df.to_csv('TwitterScrapingProject/datas/tweets.csv' , encoding='utf-8') #save to csv file 


""" 
twitter_func()
time.sleep(5)
search("Taylor Swift")
time.sleep(1)
get_tweets()
"""

