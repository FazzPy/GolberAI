# Project GolberAI
# Libraries
# ================

# VERSION 1.3

import requests
import sys
from colorama import Fore
import colorama
from bs4 import BeautifulSoup
import re
from googlesearch import search
import os
from pymongo import MongoClient
from tqdm import trange
from time import sleep 
import random
import urllib.request
import pdfkit

colorama.init()

# =====================================

class GOLBERAI():
    # SETTINGS
    # ========

    def __init__(self):
        self.ENTRY()
        self.ACTIVATED_LANG = "TR"

    # MAIN FUNCTIONS
    # ==============

    def SEARCHING(self):
        global WEB_RESULTS, SUBJECT
        
        print("\n")

        SUBJECT = str(input("SUBJECT : "))

        f = open(f"{SUBJECT}.txt","a", encoding="utf-8")
        f.close()

        print(Fore.GREEN+"Finding web sites...")

        WEB_RESULTS = []

        for j in search(SUBJECT, tld="co.in", num=10, stop=10, pause=2, lang=self.ACTIVATED_LANG):
            WEB_RESULTS.append(j)
    
        SEARCH_WIKI = re.search("wikipedia", str(WEB_RESULTS))

        if SEARCH_WIKI:
            self.WIKIPEDIA()
            
    def WIKIPEDIA(self):

        print("\n")
        print(Fore.BLUE+"GolberAI | Blogging is start!")
        print("\n")
        print(Fore.YELLOW+"JobsForAI | Daha iyisi olsaydı onu yazardık.")
        
        # WIKIPEDIA SCRAPING FUNCTIONS
        # ============================

        PARAGRAPHS = []

        def WIKI(Url, NUMBER):

            print("\n")

            for i in trange(10, desc =f"PAGE {NUMBER} ", colour="green"):
                sleep(0.1)


            html = requests.get(Url).content
            Soup = BeautifulSoup(html, "html.parser")
            
            # TITLE
            # =====

            try:
                List = Soup.find_all("h1", {"id":"firstHeading"}, limit=1)
                
                for x in List:
                    TITLE = x.span.text

            except:
                List = Soup.find_all("h1", {"id":"firstHeading"}, limit=1)

                for x in List:
                    TITLE = x.i.text

            # TEXT
            # ====

            try:
                List = Soup.find("div", {"class":"mw-parser-output"}).find_all("p", recursive=False)
            except:
                pass

            DENEME = ""
            BOOL_LIST = []

            for i in List:
                DENEME = i
                if len(DENEME) == 0:
                    pass
                else:
                    CONTROL_1 = re.search("Retrieved from", i.text)
                    if CONTROL_1:
                        sys.exit()
                    else:
                        pass
                    
                    PARAGRAPHS.append("<br>")
                    PARAGRAPHS.append("<h3 align='center'>"+TITLE+"</h3>")
                    PARAGRAPHS.append("<br>")

                    PARAGRAPHS.append(i.text)
                    BOOL_LIST.append(True)

                    COUNT = PARAGRAPHS.count("<h3 align='center'>"+TITLE+"</h3>")

                    if COUNT > 1:
                        COUNT -= 1
                        while True:
                            PARAGRAPHS.remove("<h3 align='center'>"+TITLE+"</h3>")
                            if COUNT == 1:
                                break
                            else:
                                pass

            # IMG ALGORITHM
            # =============

            CHECK_1 = True

            IMG_LIST = []

            try:
                FOTOS = Soup.find_all("div", {"class":"thumbinner"})
                CHECK_1 = True
            except:
                CHECK_1 = False

            if CHECK_1 == True:
                # DOWNLOAD IMAGE ALGORTIHM

                URL_LIST = []

                IMAGES = []

                for i in FOTOS:
                    URLS = i.img["src"]
                    TEXTS = i.text
                    HTTPS = "https:"
                    FOTO_URL = HTTPS + URLS
                    URL_LIST.append(FOTO_URL)

                COUNT = 0

                LENGTH = len(URL_LIST)

                try:
                    os.mkdir("img")
                except:
                    pass

                for x in URL_LIST:
                    DIGITS = random.randrange(1, 1000)
                    NAME = str(DIGITS) + ".jpeg"
                    urllib.request.urlretrieve(x, f"img/{NAME}")
                    IMAGES.append(NAME)

                CARD_LIST = []

                # IMAGE DESCRIPTION TEXT

                # ======================

                CARD_COUNT = 0

                for i in IMAGES:

                    if CARD_COUNT == 1:
                        IMAGES.pop(0)
                        CARD = f"""

                        <div class="col-md-6 float-md-end mb-3 ms-md-3">
                            <div class="card" style="width: 14rem;">
                                <img class="card-img-top" src="img/{i}" alt="Card image cap">
                            </div>
                        </div>

                        <br>

                        """

                        CARD_LIST.append(CARD)
                    else:
                        CARD = f"""

                        <div class="col-md-6 float-md-end mb-3 ms-md-3">
                            <div class="card" style="width: 14rem;">
                                <img class="card-img-top" src="img/{IMAGES[0]}" alt="Card image cap">
                                <div class="card-body">
                                    <p class="card-text">{TEXTS}</p>
                                </div>
                            </div>
                        </div>

                        <br>

                        """

                        CARD_LIST.append(CARD)
                        CARD_COUNT+=1
                

                CARD_TXT = open("images.txt", "w+", encoding="utf-8")

                for i in CARD_LIST:
                    CARD_TXT = open("images.txt", "a", encoding="utf-8")
                    CARD_TXT.write(i)

                CARD_TXT = open("images.txt", "r", encoding="utf-8")

                CARD_ITEM = CARD_TXT.read()

                COLUMN = f"""
                    <div class="row row-cols-1 align-items-end">
                        {CARD_ITEM}
                    </div>
                """

                PARAGRAPHS.append(COLUMN)

            else:
                pass

            # UNSUCCESSFUL ALGORITHM
            # ======================

            if len(BOOL_LIST) <= 0:
                try:
                    List = Soup.find("div", {"class":"mw-body-content mw-content-ltr"})
                except:
                    pass

                DENEME = ""

                for i in List:
                    DENEME = i
                    if len(DENEME) == 0:
                        pass
                    else:
                        CONTROL_1 = re.search("Retrieved from", i.text)
                        if CONTROL_1:
                            sys.exit()
                        else:
                            pass

                        PARAGRAPHS.append("<br>")
                        PARAGRAPHS.append("<h3 align='center'>"+TITLE+"</h3>")
                        PARAGRAPHS.append("<br>")
  
                        PARAGRAPHS.append(i.text)
                        BOOL_LIST.append(True)

                        COUNT = PARAGRAPHS.count("<h3 align='center'>"+TITLE+"</h3>")

                        if COUNT > 1:
                            COUNT -= 1
                            while True:
                                PARAGRAPHS.remove("<h3 align='center'>"+TITLE+"</h3>")
                                if COUNT == 1:
                                    break
                                else:
                                    pass



        # WEB SITE VARIABLES
        # ==================

        FIRST = WEB_RESULTS[0]
        SECOND = WEB_RESULTS[1]
        THIRD = WEB_RESULTS[2]
        FOURTH = WEB_RESULTS[3]
        FIFTH = WEB_RESULTS[4]
        SIXTH = WEB_RESULTS[5]
        SEVENTH = WEB_RESULTS[6]
        EIGHTH = WEB_RESULTS[7]
        NINTH = WEB_RESULTS[8]
        TENTH = WEB_RESULTS[9]

        # WEB SITE QUERY
        # ==============

        FIRST_SEARCH_K = re.search("Kategori", FIRST)
        SECOND_SEARCH_K = re.search("Kategori", SECOND)
        THIRD_SEARCH_K = re.search("Kategori", THIRD)
        FOURTH_SEARCH_K = re.search("Kategori", FOURTH)
        FIFTH_SEARCH_K = re.search("Kategori", FIFTH)
        SIXTH_SEARCH_K = re.search("Kategori", SIXTH)
        SEVENTH_SEARCH_K = re.search("Kategori", SEVENTH)
        EIGHTH_SEARCH_K = re.search("Kategori", EIGHTH)
        NINTH_SEARCH_K = re.search("Kategori", NINTH)
        TENTH_SEARCH_K = re.search("Kategori", TENTH)

        try:
            if FIRST_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[0], "1")
        except:
            pass
 
        try:
            if SECOND_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[1], "2")
        except:
            pass

        try:
            if THIRD_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[2], "3")
        except:
            pass

        try:
            if FOURTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[3], "4")
        except:
            pass

        try:
            if FIFTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[4], "5")
        except:
            pass

        try:
            if SIXTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[5], "6")
        except:
            pass

        try:
            if SEVENTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[6], "7")
        except:
            pass

        try:
            if EIGHTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[7], "8")
        except:
            pass

        try:
            if NINTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[8], "9")
        except:
            pass

        try:
            if TENTH_SEARCH_K:
                pass
            else:
                WIKI(WEB_RESULTS[9], "10")
        except:
            pass

        if len(PARAGRAPHS) == 0:
            WIKI(f"https://tr.wikipedia.org/wiki/{SUBJECT}", "11")
        else:
            pass

        # ==================================================

        # WRITE HTML
        # ==========

        v = ""

        for i in PARAGRAPHS:
            v = i
            with open(f"{SUBJECT}.txt","a", encoding="utf-8") as file:
                file.write(v)
                file.close()

        PARAGRAPH = open(f"{SUBJECT}.txt","r", encoding="utf-8")

        STYLE = """
        
        <style>
            /*-----------------Style Starter-----------------*/

            /*-----------------Font Download-----------------*/ 
            @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,600;0,700;1,300&display=swap');
            @import url("https://fonts.googleapis.com/css?family=Poppins:200.300.400.500.600.700.800.900&display=swap");
            @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@200&display=swap');

            /*-----------------Sayfa ortalama-----------------*/

            *{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            /*-----------------Body için yapılan süslemeler-----------------*/
            body{
                background-color: rgb(90, 28, 90);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

            /*-----------------Ana gövde icin düzenleme-----------------*/
            .container {
                position: relative;
                margin-top: 80px;
                margin-bottom: 80px;
                width: 900px;
                height: auto;
                font-family: 'Poppins', sans-serif;
                grid-template-columns: 1fr 2fr;
                box-shadow:  0 35px 55px rgba(0,0,0,0.8);
                background-color: #fff;
                border-radius: 26px;
            }

            /*-----------------Paragrafın özelliklerini belirleme-----------------*/
            #p{
                background: #fff;
                margin: auto;
                pad: auto;
                font-size: 1.5em;
                margin-top: 20px;
                font-weight: 600;
                line-height: 1.4em;
                font: Poppins;
                text-align: center;
            }

            /*-----------------Başlıkların özelliklerin belirleme-----------------*/
            #title{
                color: black ;
                text-transform: uppercase;
                font-weight: 600;
                letter-spacing: 1px;
                margin-top: 5px;
                margin-bottom: 15px;
            }
            #title2{
                color: #003147;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 10px
            }

            /*-----------------Görüntü ölçeği ayarı-----------------*/
            @media (max-width: 1000px)
            {
                .container
                {
                    margin: 10px;
                    grid-template-columns: repeat(1,1fr);
                }
                .interest ul
                {
                    grid-template-columns: repeat(1,1fr);
                }
            }
            @media (max-width: 600px)
            {
                .about .box
                {
                    flex-direction: column;
                }
                .about .box .year_company
                {
                    margin-bottom: 5px;
                }
                .interest ul
                {
                    grid-template-columns: repeat(1,1fr);
                }
                .skills .box
                {
                    grid-template-columns: repeat(1,1fr);
                }
            }

            /*-----------------Style Finish-----------------*/
        </style>

        """

        WIKIPEDIAOUTPUT = '''
        <!DOCTYPE html>
        <head>

        <!-------------------Meta Starter------------------->
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-------------------Meta Finish------------------->

        <!-------------------Title & Link Starter------------------->
        <title>FazzTech | GolberAI</title>
        <link rel = "icon" href = "golberai.png" type = "image/x-icon">
        <!-------------------Title & Link Finish------------------->

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

        {CSS}

    </head>

    <!-------------------Body Starter------------------->
    <body>

        <!-------------------Body Starter------------------->


        <!-------------------Div Starter------------------->
        <div class="container" align="center">


            <!-------------------Title Starter------------------->
            <h1 id="title">{KONU1}</h1>
            <hr>

            <!-------------------Paragraf Starter------------------->
            <p>

                
                <!-------------------secondary Title Starter------------------->
                <h5>#-----------------------------------------------------------#</h5>
                <h3 id="title2"0>{KONU2}</h3>
                <h5>#-----------------------------------------------------------#</h5>
                <!-------------------secondary Title Finish------------------->

                <div class="clearfix">
                    {PARAGRAF}
                </div

            </p>
            <!-------------------Paragraf Finish------------------->


            <!-------------------Footer Starter------------------->
            <footer id="Footer">
                <br>
                <h3 >Copyright &#169; JobsForAI | GolberAI</h3>
                <br>
            </footer>
            <!-------------------Footer Finish------------------->
        
        </div>
        <!-------------------Div Finish------------------->

        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

    </body>
    </html>     
                    '''.format(KONU1 = SUBJECT, KONU2 = SUBJECT , PARAGRAF = PARAGRAPH.read(), CSS=STYLE)

        FILE = open(f"{SUBJECT}.html", "w+", encoding="utf-8")
        FILE.write(WIKIPEDIAOUTPUT)
        FILE.close()

        os.startfile(f"{SUBJECT}.html")

        PARAGRAPH.close()

        os.remove(f"{SUBJECT}.txt")
        os.remove(".google-cookie")
        os.remove("images.txt")

        print("\n")
        print(Fore.RED+"""
        
        1) PDF Dönüştürülmesi
        
        """)
        print("\n")

        process = int(input("Process : "))

        if process == 1:
            import docraptor

            doc_api = docraptor.DocApi()

            doc_api.api_client.configuration.username = 'QDVbhDUoj7p2k3fXsKnE'

            with open(f'{SUBJECT}.html', 'r', encoding="utf-8") as f:
                document_content = f.read()

            try:
                response = doc_api.create_doc({
                    'test': True,
                    'document_type': 'pdf',
                    'document_content': document_content,
                })

                with open(f'{SUBJECT}.pdf', 'w+b') as f:
                    binary_formatted_response = bytearray(response)
                    f.write(binary_formatted_response)
                    f.close()
            except docraptor.rest.ApiException as error:
                print(error.status)
                print(error.reason)
                print(error.body)
        else:
            pass

    def SETTINGS(self, NUMBER):

        # DEFAULT SETTINGS

        if NUMBER == 0:

            TR = True
            EN = False

            self.ACTIVATED_LANG = TR

            if TR == True:
                self.ACTIVATED_LANG = "TR"
            elif EN == True:
                self.ACTIVATED_LANG = "EN"
        else:
            print(Fore.BLUE+f"""
            
            JobsForAI | GolberAI - Settings

            Active Languages : TR, EN

            Activated : {self.ACTIVATED_LANG}
            
            """)

            print("\n")

            print("""
            
            1) Choose language
            2) Coming soon..
            
            """)

            process = int(input("Process : "))

            if process == 1:
                print(Fore.LIGHTGREEN_EX+"Active Languages : TR, EN")

                LANG = input("Language (TR or EN): ")

                if LANG == "TR":
                    if self.ACTIVATED_LANG == LANG:
                        print(f"{LANG} already selected")
                    else:
                        print(f"{self.ACTIVATED_LANG} changed! Current language : {LANG}")
                        self.ACTIVATED_LANG = LANG
                elif LANG == "EN":
                    if self.ACTIVATED_LANG == LANG:
                        print(f"{LANG} already selected")
                    else:
                        print(f"{self.ACTIVATED_LANG} changed! Current language : {LANG}")
                        self.ACTIVATED_LANG = LANG
                else:
                    print(Fore.RED+"Wrong entry! Restart please.")
            elif process == 2:
                print("Coming soon..")
                restart = input("Restart please")
            else:
                pass

    def HELP(self):
        print(Fore.GREEN+"GOLBER Artifical Intelligence | FazzTech Inc.")
        print(Fore.LIGHTBLUE_EX+"Help | Page : 1")
        print("GolberAI is an automated blogging artificial intelligence.")
        print("How to work?")
        print(Fore.YELLOW+"The continuation will come.")

    # STARTING FUNCTIONS
    # ==================

    def ENTRY(self):
        print(Fore.LIGHTMAGENTA_EX+"GOLBER Artifical Intelligence | FazzTech Inc.")
        print(Fore.RED+"Official language is turkish! You can change it in settings.")

        print("\n")

        print(Fore.WHITE+"""
        1) START PROGRAM
        2) SETTINGS
        3) QUIT PROGRAM
        4) HELP    
        """)

        PROCESS = int(input("PROCESS : "))

        if PROCESS == 1:
            self.SETTINGS(0)
            self.SEARCHING()
        elif PROCESS == 2:
            self.SETTINGS(1)
        elif PROCESS == 3:
            sys.exit()
        elif PROCESS == 4:
            self.HELP()

AI = GOLBERAI()
