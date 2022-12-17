import plotly
import plotly.graph_objects as go
import pandas as pd
from flask_app.module.dbModule import Database

class Visualiser:
    def __init__(self):
        pass

    def pie(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['장르','작품수']).set_index("장르")
        fig = go.Figure(data=[go.Pie(labels=df.index, values=df["작품수"], hole=.5, title=title)])
        fig.write_html("./flask_app/static/charts/piechart.html")

    
    def hbar(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['장르','인기도']).set_index("장르")
        df = df.sort_values(by="인기도",ascending=True)
        fig = go.Figure(data=[go.Bar(
            x=df["인기도"],
            y=df.index,
            orientation='h')])
        fig.update_layout(title_text=title)
        fig.write_html("./flask_app/static/charts/hbarchart.html")

    def vbar(self, data=None, title=""):
        df = pd.DataFrame(data=data,columns=['장르','평균별점']).set_index("장르")
        fig = go.Figure(data=[go.Bar(
            x=df.index,
            y=df["평균별점"],
            orientation='v')])
        fig.update_layout(title_text=title)
        fig.update_yaxes(range=[9.0, 10])
        fig.write_html("./flask_app/static/charts/vbarchart.html")
