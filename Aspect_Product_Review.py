#Aspect Based Product Review Analysis Using Python
#Library use for building application
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

def aspect_Product():
    #Extracting the Product Review from Vendor like (Flipkart)
    rate,title,description = extract()    #Extract function will return 3 list having 1.rating,2.Title,3.Description

    #Stroing Data into J5_Review.csv
    store(title,description)    
    
    #Removing noise from data to have clean data
    pp_review = removing_noise(description)

    #Removing Stopwords from Review
    pp_review_stopwords = removing_stopword(pp_review)
    
    #Extracting feature from Review like camera
    aspect_data = extract_feature(pp_review_stopwords)
    
    #Calculating Positve & Negative about data
    action,subject,per_pos_neg = senti_review(aspect_data)
    
    #PLoting graph of aspect data
    plot_graph(per_pos_neg)
    
                    
def extract():
    #Using Selinium for extracting Product Review of Samsung J5 Galaxy from different Vendor like Flipkart,Snapdeal,Amazon
    driver = webdriver.Firefox()
    i = 0
    j = 1
    o1=[]
    o2=[]
    o3=[]
    while i < 10:
        link = 'https://www.flipkart.com/samsung-galaxy-j5-6-new-2016-edition-white-16-gb/product-reviews/itmegmrnzqjcpfg9?page=%d&pid=MOBEG4XWJG7F9A6Z'%j
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        for entry in soup.find_all('div', '_3DCdKtW48_r0oBfxxzGDuN'):
            for x in entry.find_all('div','hGSR34dV_01iw9lhaXfbr _2beYZwhviGeQ_pNATVavBl E_uFuv9DG5D79UkdWDmZ0'):
    #            print((x.text).encode('ascii','ignore'))
                o1.append((x.text).encode('ascii','ignore'))
            for y in entry.find_all('p','_2xg6Ul2Q-YucCc2Yanfrz9'): 
    #            print(y.text)
                o2.append(y.text)
            for z in entry.find_all('div','qwjRop-Ma_yEUwGRoaCsj'):
    #            print(z.text)
                o3.append(z.text)
        j = j + 1
    return o1,o2,o3

#Storing Review into .csv file 
def store(data1,data2):
    Final_J5 = pd.DataFrame({'Title':data1,'Description':data2})
    Final_J5.to_csv('J5_Review.csv',encoding = 'utf-8')
    print "Successfully Write!!!"
    
def removing_noise(data):
    pp_o3 = []
    for i in range(len(data)):
        a = re.sub('READ MORE','',data[i])
        a = re.sub('\.{2,}|!+|\/',' ',a)
        a = re.sub('J5|hi|HI|Hi','',a)
        a = re.sub('\d',' ',a)
        a = re.sub(',',' ',a)
        a = re.sub('\(|\)','',a)
        a = re.sub('"','',a)
        a = re.sub('&|%|#|@|\*|\'|\+|\$|>|-{1,}|\?{1,}|;|:|_',' ',a)
        a = ' '.join(a.split())
        a = a.encode('ascii','ignore')
        pp_o3.append(a)
    return pp_o3

def removing_stopword(data):
    stop = set(stopwords.words("english"))
    temp_list = []
    new_data = []         #Removing Stopwords & stroing in Tweet_list
    for i in range(len(data)):
        temp_list=[]
        for j in data[i].lower().split():
            if j not in stop:
                temp_list.append(j)
        new_data.append(' '.join(temp_list))  
    print "Successfully Removed Stopwords" 
    return new_data

def extract_feature(data):
    camera = []
    for i in range(len(data)):
        if re.search('camera|camra|photos|photo|click|images|image|photos',data[i]):
            camera.append(data[i])
    print "Successfully Extract"
    return camera

def senti_review(status):
    pos_neg = []
    subject = []
    pos = 0
    neg = 0 
    neut =0
    pos_per=neg_per=neu_per= 0
    for i in range(len(status)):
        bb = TextBlob(status[i])
        subject.append(bb.sentiment[1])
        if(bb.sentiment[0]>0.0):
            pos_neg.append("Positive")
            pos = pos + 1
        elif(bb.sentiment[0]==0.0):
            pos_neg.append("Neutral")
            neut = neut + 1
        else:
            pos_neg.append("Negative")
            neg = neg + 1
    pos_per = round((pos/float(len(status)))*100,3)
    neg_per = round((neg/float(len(status)))*100,3)
    neu_per = round((neut/float(len(status)))*100,3)
    pnn = [pos_per,neu_per,neg_per]
    print "Positivity in Review : ",round((pos/float(len(status)))*100,3),"%"
    print "Negativity in Review : ",round((neg/float(len(status)))*100,3),"%"
    return pos_neg,subject,pnn

def plot_graph(pp_per):
    labels = ['Positve', 'Neutral', 'Negative', ]
    sizes = pp_per
    colors = ['yellowgreen', 'gold', 'lightskyblue']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()