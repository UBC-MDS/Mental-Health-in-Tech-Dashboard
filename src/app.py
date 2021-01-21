import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

data = pd.read_csv("data/processed/mental_health_clean.csv")

# app layout
app.layout = dbc.Container([
    html.H1("Mental Health in Tech Dashboard"),
        dbc.Row([
                dbc.Col([
                        dcc.Dropdown(
                            id="q_selection",
                            value="tech_org",
                            options=[
                                {"label": i, "value": i} for i in data.columns[:18]],),],md=4),
                dbc.Col([
                        html.Iframe(
                            id="gender_barplot",
                            style={"width": "100%", "height": "400px"},),]),])])

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
