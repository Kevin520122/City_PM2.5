# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, dcc, html ,Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


#Load data and add city label
BJ_df = pd.read_csv("Beijing.csv")
BJ_df["city"] = "Beijing"
CD_df = pd.read_csv("Chengdu.csv")
CD_df["city"] = "Chengdu"
GZ_df = pd.read_csv("Guangzhou.csv")
GZ_df["city"] = "Guangzhou"
SH_df = pd.read_csv("Shanghai.csv")
SH_df["city"] = "Shanghai"
SY_df = pd.read_csv("Shenyang.csv")
SY_df["city"] = "Shenyang"

#Merge 5 datasets together
PM_df = pd.concat([BJ_df, CD_df, GZ_df, SH_df, SY_df])
PM_df = PM_df.fillna({
    "Iprec": 0,
    "precipitation": 0,
    "TEMP": 0,
    "PRES": 0,
    "DEWP": 0,
    "Iws": 0,
    "PM": 0,
    "HUMI": 0,
    "season": 0
})

#Data Transformation
PM_df["season"] = PM_df["season"].astype(int)

PM_df["year"] = PM_df["year"].astype(str)
PM_df["month"] = PM_df["month"].astype(str)
PM_df["day"] = PM_df["day"].astype(str)
PM_df["hour"] = PM_df["hour"].astype(str)
PM_df["date"] = PM_df["year"]+ "-" + PM_df["month"] + "-" + PM_df["day"]
PM_df["date"] = pd.to_datetime(PM_df["date"])

#Feature Engineering - Season
PM_df["season"] = PM_df["season"].replace({0: "unknown", 1: "spring", 2: "summer", 3: "fall", 4: "winter"})
PM_df["year_season"] = PM_df["year"] + "-" + PM_df["season"]


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        id="title",
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Dropdown to selceted city
     html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(
            ['Chengdu', 'Guangzhou', "Shanghai", "Shenyang", "Beijing"], 
            'Shanghai',
            id="City"
        ),
        html.Br()
    ], style={'padding': 20, 'flex': 1}),
    
    
    dcc.Graph(
        id='PM'
    ),

    dcc.Graph(
       id="prec"
    )
])

@callback(
    Output("title", "children"),
    Input("City", "value")
)
def update_title(selected_city):
    return f"{selected_city} PM 2.5 Relevent Data Dashboard"


@callback(
    Output("PM", "figure"),
    Input("City", "value")
)
def update_graph(selected_city):
    selected_city_prec = PM_df[PM_df["city"] == selected_city]

    PM_city_year = (
        selected_city_prec.groupby(["year"])["PM"]
        .mean().round(1)
        .reset_index(name="Average PM yearly")
    )
    
    fig = px.bar(PM_city_year, x="year", y="Average PM yearly", title=f"Bar chart - PM2.5 level yearly comparaision for {selected_city}")
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 30, 'r': 0}, 
        hovermode='closest',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


@callback(
    Output("prec", "figure"),
    Input("City", "value")
)
def update_graph2(selected_city):
    selected_city_prec = PM_df[PM_df["city"] == selected_city]

    precip_season = (
        selected_city_prec.groupby(["year_season"])["precipitation"]
            .sum()
            .reset_index(name="seasonal cumulated PREC")
    )
        
    fig = px.line(
        precip_season, x="year_season", y="seasonal cumulated PREC",
        title="Line Chart - Seasonal Precipitation PM"
    )
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 30, 'r': 0}, 
        hovermode='closest',
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
