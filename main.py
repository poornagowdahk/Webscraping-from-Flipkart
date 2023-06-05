from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq
import logging
import requests
# import pandas as pd
from datetime import datetime


fileName = datetime.now().strftime('main_%H_%M_%S_%d_%m_%Y.log')
logging.basicConfig(filename=fileName, level = logging.INFO, format=" %(asctime)s %(levelname)s %(name)s %(message)s")

app = Flask(__name__, template_folder='templates')

@app.route("/",methods = ['POST','GET'])
def index():
    return render_template("index.html")


@app.route("/review", methods = ["POST","GET"])
def results():

    if request.method == "POST":

        try:

            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            
            response = urReq(flipkart_url)
            data_flipkart = response.read()

            response.close()

            beautified_html = bs(data_flipkart,"html.parser")

            beautified_all_phones = beautified_html.find("div",{"class":"_1YokD2 _3Mn1Gg"})
            beautiful_ph = beautified_all_phones.find("a",{"class":"_1fQZEK"})

            
            beautiful_ph_link = beautiful_ph.get("href")
            
            beautiful_ph_site = flipkart_url + beautiful_ph_link

            
            product6 = requests.get(beautiful_ph_site)

            product6.encoding = "utf-8"

            product6_page = bs(product6.text,'html.parser')
           
            commentboxes = product6_page.find_all("div",{"class":"_16PBlm"})

            reviews = []
            
            for commentsB in commentboxes:

                # price = product6_page.find('div',{'class':'_30jeq3 _16Jk6d'}).text
                
                try:
                    # comments = commentsB.div.div.find_all('div',{'class':''})
                    # custComment = comments[0].div.text
                    comments = commentsB.div.div.find('div',{'class':''}).text
                    custComment = comments
                except:
                    print("No comments found")
                
                try:
                    # name = commentsB.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    name = commentsB.div.div.find("p",{"class":"_2sc7ZR _2V5EHH"}).text
                    
                except:
                    print('Name Information Not available')

                try:
                    price = product6_page.find('div',{'class':'_30jeq3 _16Jk6d'}).text

                except:
                    print("price is not available")

                try:
                    ratings = product6_page.find("text",{"class":"_2Ix0io"}).text

                except:
                    print("ratings not available")

                    
                mydict = {"Comment":custComment,'Name':name,"price":price,"ratings":ratings}
                reviews.append(mydict)

            #return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
            return render_template('results.html', reviews1=reviews[0:len(reviews)])
            
        except:
            return render_template('Issue in the code check')
            
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)