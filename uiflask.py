from flask import Flask,render_template,request
import requests
import pickle
import pandas as pd
import numpy as np
movies=pickle.load(open('top3.pkl','rb'))
movie=pickle.load(open('moviep.pkl','rb'))
similarity=pickle.load(open('similarity3.pkl','rb'))
posters=pickle.load(open('posters.pkl','rb'))
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('Templates/home.html',
                           title=list(movies['title'].values),
                           overview=list(movies['overview'].values),
                           ratings=list(movies['vote_average'].values),
                           poster=list(movies['posters'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('Templates/recommended.html',
                           title=list(movies['title'].values),
                           overview=list(movies['overview'].values),
                           ratings=list(movies['vote_average'].values),
                           )
@app.route('/samemovie',methods=['post'])
def same():
    uinput=request.form.get('uinput')
    index = movie[movie['title'] ==uinput ].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    distances=distances[1:7]
    films = []
    overview=[]
    ratings=[]
    poster=[]


    df = pd.DataFrame(distances, columns=['index', 'similarity'])

    for i in df['index']:
        films.append(movie.iloc[i].title)
        overview.append(movie.iloc[i].overview)
        ratings.append(movie.iloc[i].vote_average)
        poster.append(movie.iloc[i].posters)

    return render_template('Templates/movies.html',
                           films=films,
                           plot=overview,
                           ratings=ratings,
                           poster=poster,

                           )

if __name__=='__main__':
    app.run(debug=True)
