from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'lister list detail sub-list'})
row = table.find_all('div', attrs={'class':'lister-item mode-advanced'})

row_length = len(row)

temp = [] #initiating a list 

#insert the scrapping process here
for i in row:
    
    #get titles
    titles=i.find('h3', attrs={'class':'lister-item-header'}).find('a').text
    
    #get imdb rating
    rating=i.find('div', attrs={'class':'inline-block ratings-imdb-rating'}).text
    rating=rating.strip()
    
    #get metascore
    metascore = i.find('div', attrs={'class':'inline-block ratings-metascore'})
    if metascore is not None:
        metascore=i.find('div', attrs={'class':'inline-block ratings-metascore'}).find('span').text
        metascore=metascore.strip()
    else:
        metascore='NaN'
    
    #get votes
    votes=i.find('span', attrs={'name':'nv'}).text
    votes=votes.strip()

    temp.append((titles,rating,metascore,votes))
    
temp

#change into dataframe
df = pd.DataFrame(temp, columns=('Title','Rating','Metascore','Votes'))

#insert data wrangling here
df['Rating']=df['Rating'].astype('float64')
df['Metascore']=df['Metascore'].astype('float64')
df['Votes']=df['Votes'].str.replace(',','')
df['Votes']=df['Votes'].astype('int64')

#end of data wranggling 
import numpy as np
df.index = range(1, df.shape[0] + 1)
df.head()

@app.route("/")
def index(): 
	
	card_data = f'{df["Metascore"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)