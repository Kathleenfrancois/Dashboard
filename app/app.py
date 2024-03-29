from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import plotly.express as px
import pandas as pd

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def welcome(request: Request, db: Session=Depends(get_db)):
    x=crud.get_Project(db)
    df =pd.DataFrame.from_records(x,columns=['State','Total','Hom','Sui','Ranks'])
    px. defaults.width = 266
    px. defaults.height = 200

    fig = px.bar(df.head(10),x='State', y='Ranks',color='Ranks').update_yaxes(categoryorder="total descending")
    fig = px.bar(df.head(10),x='State', y='Ranks',title='Top 10 States w/ Gun Releated Deaths')
    fig.update_layout( yaxis = dict( tickfont = dict(size=5)),
        xaxis = dict( tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    top10=fig.to_html(full_html=False, include_plotlyjs='cdn')

    dfteam = df.groupby('State')['Total'].sum()
    dfteam = dfteam.reset_index()
    dfteam = dfteam.sort_values('Total', ascending=False).head(10)

    fig10 = px.bar(dfteam, x='State', y='Total')
    fig10.update_layout( yaxis = dict( tickfont = dict(size=5)),
        xaxis = dict( tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    team10 = fig10.to_html(full_html=False, include_plotlyjs='cdn')

    dfteam = df.loc[df['State'].isin(dfteam.State)]
    figteam = px.bar(dfteam, x='State', y='Total',color='Ranks').update_xaxes(categoryorder="total descending")
    figteam.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    teamsalary = figteam.to_html(full_html=False, include_plotlyjs='cdn')

    pos10 = dfteam.groupby('State')['Sui'].mean().sort_values(ascending=False).head(10)
    pos10 = pos10.reset_index()
    figpos = px.box(dfteam.loc[dfteam['State'].isin(pos10.State)],x='State', y='Total')
    figpos.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    possalary = figpos.to_html(full_html=False, include_plotlyjs='cdn')

    bottom10 = df.groupby('State')['Total'].sum()
    bottom10 = bottom10.reset_index()
    bottom10 = dfteam.sort_values('State', ascending=False).tail(10)
    dfteam = df.loc[df['Total'].isin(bottom10.Total)]

    pos10 = dfteam.groupby('State')['Hom'].mean().sort_values(ascending=False).head(10)
    pos10 = pos10.reset_index()
    figpos2 = px.box(dfteam.loc[dfteam['State'].isin(pos10.Hom)],x='State', y='Hom', color_discrete_sequence=['red'])
    figpos2.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    possalary2 = figpos2.to_html(full_html=False, include_plotlyjs='cdn')

    dfteam = df.groupby('State')['Ranks'].head(10)
    dfteam = dfteam.reset_index()
    dfteam = dfteam.sort_values('Ranks', ascending=False)

    figpie = px.pie(dfteam, values='Ranks', names='Ranks')
    figpie.update_layout(yaxis = dict(tickfont = dict(size=5)),
        xaxis = dict(tickfont = dict(size=5)),
        font=dict(size=5),
        margin=dict(l=0, r=0, t=0, b=0))
    pospie = figpie.to_html(full_html=False, include_plotlyjs='cdn')

    return templates.TemplateResponse("chart.html", {"request": request,"top10":top10, "team10":team10,"teamsalary":teamsalary,"possalary":possalary,"possalary2":possalary2,"pospie":pospie})
