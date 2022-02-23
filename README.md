# 2021_EnhancedWebBot

* Requirements

-- For Windows

Python 3.8.8, pip, mysql and latest google chrome installed

Donwload from here: https://www.python.org/downloads/release/python-388/
..and here: https://dev.mysql.com/downloads/mysql/
..and here: https://www.google.com/chrome/

-- For Ubuntu - Linux

Pythin 3.8, pip, mysql and latest google chrome installed

Run this commads to install:

sudo apt install python3.8

sudo apt-get install python3-pip

sudo apt install mysql-server

sudo mysql_secure_installation

google chrome install from here: https://www.google.com/chrome/

* Mysql
 Make sure remember the url of the server, the user and password and the mysql server is started.
 Αfterward check the env.ini file and set this information in the proper fields.

* Description of the project

The purpose of the project is to create a web bot which, in addition to the usual information, will store additional information for each link and save to mysql     database. The purpose is to be able to calculate the importance of each link, based on the following characteristics: Image size, Font size and other font properties (bold, italics, etc), color, position within the website, of course for each website should be stored the common information such as URL, title, size, modification time, access time. 

The Enhanced Web Bot is able to render web sites and extract all urls for each page with the information we need. As policy we create the urls as a search tree and we able to cross all over with depth-first and breadth first algorithm at specifc depth. After scap each link with the necessary information are stored in mysql database. Also have error handeler and retry - queue for check again a url.

* About

 This project is done in the context of a thesis of a student of the University of Computer Engineering and Electronic Systems of Thessaloniki,Greece.
