import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import altair as alt


app = dash.Dash(__name__)

data = pd.read_csv("data/processed/mental_health_clean.csv")

# app layout
app.layout = html.Div(
    [
        html.Iframe(id="gender_barplot", style={"width": "100%", "height": "400px"}),
        dcc.Dropdown(
            id="q_selection",
            value="tech_org",
            options=[{"label": i, "value": i} for i in data.columns[:18]],
        ),
    ]
)

# plot specs
@app.callback(Output("gender_barplot", "srcDoc"), Input("q_selection", "value"))
def plot_gender_chart(q_selection="mental_health_benefits_employer"):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            alt.X("gender", title=""),
            alt.Y("count()"),
            color=alt.Color("gender", legend=None),
            column=alt.Column(q_selection, type="nominal", title="Responses by Gender"),
        )
    )
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)