from time import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from urllib.parse import urljoin
import validators
from selenium.common.exceptions import WebDriverException
from utils.timeout import timer, TimerThread
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.color import Color
from utils.fonts import getFontWeight
from datetime import datetime
import webcolors
import re
import time
import sys
import mysql.connector
from configparser import ConfigParser
from mysql.connector.errors import Error
from mysql.connector import errorcode
from utils.db import connectDb2

# web bot class
# for dynamic sites


class Webbot():
    # init method
    def __init__(self, dfs_depth_summary=[], db=None, botId=None, urlId=None, errors = []):
        super().__init__()
        self.dfs_depth_summary = dfs_depth_summary
        self.load_driver()
        self.db = db
        self.botId = botId
        self.urlId = urlId
        self.errors = errors
        self.connectToDb()
        self.createBotToDb()

    # load chrome driver and set to headless mode
    def load_driver(self):
        options = ChromeOptions()
        options.headless = True
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        global driver
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=s, options=options)

    # render the site
    def renderSite(self, url):
        driver.implicitly_wait(5)
        driver.get(url)
        time.sleep(3)
        global base_url
        base_url = url
        return self.ScrapLinks()

    # Scrape and return all links for this page
    def ScrapLinks(self):
        #temp_urls = set()
        mylist = []
        try:
            urls = driver.find_elements_by_xpath("//a[@href]")
            for url in urls:
                item = {"link": "",
                        "link_title": "",
                        "width": None,
                        "height": None,
                        "color": "",
                        "x": None,
                        "y": None,
                        "font_size": None,
                        "font_name": "",
                        "font_attrs": "",
                        "visited": False,
                        "url" : None,
                        "url_title" : None,
                        "url_size" : None,
                        "url_status": True,
                        "url_access_time": None,
                        "url_modification_time": None,
                        }
                rect = url.rect
                font_size = url.value_of_css_property("font-size")
                color = Color.from_string(
                    url.value_of_css_property("color")).hex
                fontWeight = url.value_of_css_property("font-weight")
                fontWeightName = getFontWeight(fontWeight)
                fontName = url.value_of_css_property("font-family")
                text = url.text
                url = url.get_attribute('href')
                title = driver.title

                if (url is not None and url != ""):
                    url = urljoin(base_url, url)
                    if (validators.url(url)):
                        # temp_urls.add(url)
                        item["link"] = url
                        item["link_title"] = text
                        item["width"] = rect["width"]
                        item["height"] = rect["height"]
                        item["color"] = color
                        item["x"] = rect["x"]
                        item["y"] = rect["y"]
                        item["font_size"] = font_size
                        item["font_name"] = fontName
                        item["font_attrs"] = fontWeightName
                        item['url_title'] = title
                        item['url'] = base_url
                        item['url_size'] = 33
                        item['url_access_time'] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        mylist.append(item)
            return mylist
        except UnicodeEncodeError as ue_err:
            print(ue_err)
            self.errors.append(ue_err)
        except Exception as e:
            print(e)
            self.errors.append(e)
        except AttributeError as non_Ex:
            print(non_Ex)
        except TypeError as type_err:
            print(type_err)

    # Deapth First Algorithm
    def dfs(self, base, max_depth, path="", visited=None, depth=0, times=1):
        if depth < max_depth:
            try:
                if visited is None:
                    visited = set([base])
                    self.updateBotStatus(max_depth, self.dfs.__name__)
                hrefs = self.renderSite(base)
                for href in hrefs:
                    if href["link"] not in visited:
                        visited.add(href["link"])
                        href["visited"] = True
                        #href["found_depth"] = depth
                        href["url_modification_time"] = datetime.now().strftime(
                            "%d/%m/%Y %H:%M:%S")
                        print(f"Depth {depth}: {href['link']}")
                        self.saveUrlsToDb(href)
                        self.dfs_depth_summary.append(depth)
                        if href["link"].startswith("http"):
                            self.dfs(
                                href["link"], max_depth, "", visited, depth + 1)
                        else:
                            self.dfs(
                                base, max_depth, href["link"], visited, depth + 1)
            except WebDriverException as wb_ex:
                if (times == 0):
                    print("-- Timeout.")
                    print("-- Error: The url cannot be resolved.")
                    self.errors.append(wb_ex)
                    return
                print("-- Error: The url cannot be resolved.")
                self.errors.append(wb_ex)
                TimerThread(f"TimeOutThread_{times}", timer, 5)
                self.dfs(base, max_depth, times=times-1)
            except Exception as ex:
                print("-- Error: Something goes wrong or the input url does not exist")
                self.errors.append(ex)

    # Breadth First Algorithm

    def bfs(self, start_url, depth, times=1):
        try:
            if depth <= 0:
                return print(start_url)
            visited = set()
            queue = []
            visited.add(start_url)
            queue.append(start_url)
            print("\n -- BFS Started -- \n")
            print(f"Starting from: {start_url} \n")
            self.updateBotStatus(depth, self.bfs.__name__)
            for i in range(depth):
                print(f"\nDepth: {i+1}")
                for count in range(len(queue)):
                    url = queue.pop(0)
                    urls = self.renderSite(url)
                    if urls is False:
                        continue
                    for j in urls:
                        if j["link"] not in visited:
                            visited.add(j["link"])
                            queue.append(j["link"])
                            j["visited"] = True
                            j["url_modification_time"] = datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S")
                            encodedUrl = j["link"].encode('utf-8')
                            print(f"\t{encodedUrl}")
                            self.saveUrlsToDb(j)
                print(f"Number of urls for Depth {i+1}: {len(queue)}")
        except WebDriverException as wb_ex:
            if (times == 0):
                print("-- Timeout.")
                print("-- Error: The url cannot be resolved.")
                self.errors.append(wb_ex)
                return
            print("-- Error: The url cannot be resolved.")
            self.errors.append(wb_ex)
            TimerThread(f"TimeOutThread_{times}", timer, 5)
            self.bfs(start_url, depth, times-1)
        except Exception as ex:
            #print("-- Error: Something goes wrong or the input url does not exist")
            print(ex)
            self.errors.append(ex)
            # print(url.encode('utf-8'))
        finally:
            print("\n -- BFS Completed -- \n")
            driver.quit()

    # check page response for 404 or not found
    def checkNotFound(self, soup):
        notFound = soup.title.text
        if (("404" in notFound) or ("Not Found" in notFound)):
            return False
        else:
            return True

    def closeDriver(self):
        driver.quit()

    def connectToDb(self):
        database = connectDb2()
        self.db = database

    def createBotToDb(self):
        now = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")
        sql = "INSERT INTO bots (bot_status,bot_start_time) VALUES ('Pending', %s);"
        cursor = self.db.cursor()
        cursor.execute(sql, (now,))
        lastrowid = cursor.lastrowid
        self.botId = lastrowid
        self.db.commit()
        # print(lastrowid)

    def updateBotStatus(self, depth, method):
        sql = "UPDATE bots set bot_method = %s , bot_depth = %s where id = %s;"
        cursor = self.db.cursor()
        cursor.execute(sql, (method, depth, self.botId))
        self.db.commit()

    def botCompletedStatus(self):
        endTime = now = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S")
        sql = "UPDATE bots set bot_status = %s, bot_end_time = %s where id = %s;"
        cursor = self.db.cursor()
        cursor.execute(sql, ("Completed", endTime, self.botId))
        self.db.commit()

    def saveUrlsToDb(self, data):
        
        check = self.checkForDoublicateUrl(data)
        
        if not check:
            now = datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S")
            sql = "INSERT INTO urls (url,url_title,url_size,url_status,url_access_time,url_modification_time) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor = self.db.cursor()

            cursor.execute(
                    sql, (data["url"], data["url_title"], data["url_size"], data["url_status"], data["url_access_time"], data["url_modification_time"])
                    )
            self.db.commit()
            urlId = cursor.lastrowid

            sql2 = "INSERT INTO bots_urls(urls_id,bots_id) VALUES (%s,%s)"
            cursor2 = self.db.cursor()
            cursor2.execute(
                sql2, (urlId, self.botId)
                )
            self.urlid = urlId
            self.db.commit()
            #print(self.urlId)
            self.saveLinksToDb(data)
            #print(data)
        else:
            #myData = check
            #print(check)
            doublicateEntry = self.checkForDoublicateBotsUrl(check)
            #print(doublicateEntry)
            if not doublicateEntry:
                sql3 = "INSERT INTO bots_urls(urls_id,bots_id) VALUES (%s,%s)"
                cursor2 = self.db.cursor()
                #print(check[0][0], self.botId)
                cursor2.execute(
                    sql3, (check[0][0], self.botId)
                    )
                self.urlid = check[0][0]
                self.db.commit()
                #print(data)
            self.saveLinksToDb(data)

        

    def saveLinksToDb(self, data):
        doublicateLinks = self.checkForDoublicateLinks(data)
        if (not doublicateLinks):
            now = datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S")
            sql = "INSERT INTO links(urls_id,link,link_title,width,height,color,x,y,font_size,font_name,font_attrs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = self.db.cursor()
            cursor.execute(
                sql, (self.urlid, data['link'], data['link_title'], data['width'], data['height'], data['color'], data['x'], data['y'], data['font_size'], data['font_name'], data['font_attrs'])
                )
            self.db.commit()
        
      
    def checkForDoublicateUrl(self, data):
        sql = "SELECT * FROM urls WHERE url = %s LIMIT 1"
        cursor = self.db.cursor()
        cursor.execute(
                sql, ( data["url"],)
                )
        myresult = cursor.fetchall()
        
        #print(myresult[0][0])
        if myresult:
            return myresult
        return False
      

    def checkForDoublicateBotsUrl(self, data):
        sql = "SELECT * FROM bots_urls WHERE urls_id = %s AND bots_id= %s LIMIT 1"
        cursor = self.db.cursor()
        cursor.execute(
                sql, ( data[0][0], self.botId)
                )
        myresult = cursor.fetchall()
        #print(myresult[0][0])
        if myresult:
            return myresult
        return False
      

    def checkForDoublicateLinks(self, data):
        sql = "SELECT * FROM links WHERE link = %s LIMIT 1"
        cursor = self.db.cursor()
        cursor.execute(
                sql, ( data["link"],)
                )
        myresult = cursor.fetchall()
        #print(myresult[0][0])
        if myresult:
            return myresult
        return False


    def saveErrorsToDbLog(self):
        if self.errors:
            for i in self.errors:
                print("testtttttttttttttttt")
                print(i)
                sql = "INSERT INTO logs(bId, status, message, errors) VALUES (%s,%s,%s,%s)"
                cursor = self.db.cursor()
                cursor.execute(
                        sql, (self.botId , "ERROR - TERMINATED", "ERROR: See the errors tab", "test error")
                        )
                self.db.commit()
                
