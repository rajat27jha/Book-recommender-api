import pandas as pd
import flask
from flask import request, Flask
from pandas import json

app = Flask(__name__)


@app.route('/library', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' or 'GET':
        book_name = request.args.get(bname) #receving argument send by user on app as bname but error is bname is not recognised
        column_names = ['user_id', 'ISBN', 'rating']
        df = pd.read_csv('BX-Book-ratngss.data', sep=';', names=column_names, skiprows=1)
        dg = df[df['user_id']<=3000]
        book_titles = pd.read_csv('Bx-books.data',sep=';',skiprows=1,names=['ISBN','BOOK-TITLE','another','another2','another3','another4','another5','another6'])
        book_titles=book_titles.drop(["another4",'another','another3','another2','another6','another5'],axis=1)
        dg = pd.merge(dg,book_titles,on='ISBN')
        ratings = pd.DataFrame(dg.groupby('BOOK-TITLE')['rating'].mean())
        ratings['num of ratings'] = pd.DataFrame(dg.groupby('BOOK-TITLE')['rating'].count())
        bookmat = dg.pivot_table(index='user_id',columns='BOOK-TITLE',values='rating')
        c1984_ratings = bookmat[book_name]
        similar_to_1984 = bookmat.corrwith(c1984_ratings)
        corr_1984 = pd.DataFrame(similar_to_1984,columns=['Correlation'])
        # corr_1984 = corr_1984.join(ratings['num of ratings'])
        corr_1984.dropna(inplace=True)
        recomm = list(corr_1984.index[0:5].values)
        return flask.jsonify({"success": 1,"result":recomm})
    
    return flask.jsonify({"success": 0})


app.run()
