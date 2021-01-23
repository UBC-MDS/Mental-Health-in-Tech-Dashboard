import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import numpy as np

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

data = pd.read_csv("data/processed/mental_health_clean.csv")

# app layout
app.layout = dbc.Container(
    [
        html.H1("Mental Health in Tech Dashboard"),
        html.Hr(),
        dbc.Row([html.H2("Overview Section:")]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="q_selection",
                            value="tech_org",
                            options=[
                                {"label": i, "value": i} for i in np.r_[data.columns[0:14], data.columns[15:18]]
                            ],
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="gender_barplot",
                            style={"width": "100%", "height": "500px"},
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row([html.Hr()]),
        dbc.Row([html.H2("HR Questions Section:")]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Gender"),
                        dcc.RadioItems(
                            id="gender_selection",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "Male", "value": "Male"},
                                {"label": "Female", "value": "Female"},
                                {"label": "Others", "value": "Other"},
                            ],
                            value="all",
                            inputStyle={"margin-left": "10px", "margin-right": "2px"},
                        ),
                        html.Br(),
                        html.H4("Age of Respondents:"),
                        dcc.RangeSlider(
                            id="age_slider",
                            min=15,
                            max=65,
                            step=None,
                            allowCross=False,
                            marks={
                                15: "15",
                                20: "20",
                                25: "25",
                                30: "30",
                                35: "35",
                                40: "40",
                                45: "45",
                                50: "50",
                                55: "55",
                                60: "60",
                                65: "65",
                            },
                            value=[15, 65],
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Iframe(
                            id="work_interfere_barplot",
                            style={"width": "100%", "height": "300px"},
                        ),
                        html.Iframe(
                            id="remote_barplot",
                            style={"width": "100%", "height": "400px"},
                        ),
                    ]
                ),
            ]
        ),
    ]
)

# plot specs
@app.callback(Output("gender_barplot", "srcDoc"), Input("q_selection", "value"))
def plot_gender_chart(q_selection="mental_health_benefits_employer"):
    chart = (
        alt.Chart(data, title=f"Responses by gender: {q_selection}")
        .mark_bar()
        .encode(
            alt.X("gender", title=""),
            alt.Y("count()", title="Number of Responses"),
            color=alt.Color("gender", legend=None),
            column=alt.Column(q_selection, type="nominal", title=""),
        ).configure_header(labelFontSize=10)
            .configure_title(fontSize=18, font="Courier", anchor="middle", color="gray")
            .properties(height=300, width=80)
    )
    return chart.to_html()


@app.callback(
    Output("work_interfere_barplot", "srcDoc"),
    Input("age_slider", "value"),
    Input("gender_selection", "value"),
)
def plot_work_interfere_bars(age_slider=[15, 65], gender="all"):
    plot_data = data
    # To filter for responses that indicated they had a mental health condition:
    plot_data = plot_data.query(
        'work_interfere_treated != "Not applicable to me" & work_interfere_not_treated != "Not applicable to me"'
    )
    # To filter data for responses in the age range:
    plot_data = plot_data.query("age >= @age_slider[0] & age <= @age_slider[1]")
    # To filter data for responses in the target gender:
    if gender != "all":
        plot_data = plot_data.query("gender == @gender")

    # To generate the plots:
    treated = (
        alt.Chart(plot_data, title="When Treated")
        .mark_bar()
        .encode(
            x=alt.X(
                "work_interfere_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=None,
            ),
            y=alt.Y("count()", axis=alt.Axis(title="Number of Responses")),
            color=alt.Color(
                "work_interfere_treated", legend=alt.Legend(title="How Often?")
            ),
        )
        .properties(height=200, width=200)
    )
    untreated = (
        alt.Chart(plot_data, title="When Untreated")
        .mark_bar()
        .encode(
            x=alt.X(
                "work_interfere_not_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=None,
            ),
            y=alt.Y("count()", axis=alt.Axis(title="Number of Responses")),
            color=alt.Color(
                "work_interfere_not_treated", legend=alt.Legend(title="How Often?")
            ),
        )
        .properties(height=200, width=200)
    )
    viz = alt.hconcat(
        treated,
        untreated,
        title="Does your mental health issue interfere with your work?",
    ).configure_title(fontSize=20, font="Courier", anchor="middle", color="gray")
    return viz.to_html()


@app.callback(Output("remote_barplot", "srcDoc"), Input("gender_selection", "value"))
def plot_remote_work(gender="all"):
    replace_dic = {
        "Maybe": "Mental Health Response:\nMaybe",
        "Yes": "Mental Health Response:\nYes",
        "No": "Mental Health Response:\nNo",
    }

    # Remove null values
    remote_df = data[data["gender"].notnull()].copy()
    remote_df["have_mental_helth_disorder"].replace(replace_dic, inplace=True)

    # Default condition
    if gender == "all":
        remote_plot = (
            alt.Chart(
                remote_df,
                title="Do employees that work remotely report fewer mental health issues?",
            )
            .mark_bar()
            .encode(
                x=alt.X("is_remote", axis=None),
                y=alt.Y("count()", title="Number of Responses"),
                color=alt.Color("is_remote", legend=alt.Legend(title="Remote work")),
                column=alt.Column("have_mental_helth_disorder", title=""),
            )
            .configure_header(labelFontSize=12, labelOrient="bottom")
            .properties(height=220, width=170)
            .configure_title(fontSize=18, font="Courier", anchor="middle", color="gray")
        )
    else:
        # Selected Filter condition
        remote_plot = (
            alt.Chart(
                remote_df[remote_df["gender"] == gender],
                title="Do employees that work remotely report fewer mental health issues?",
            )
            .mark_bar()
            .encode(
                x=alt.X("is_remote", axis=None),
                y=alt.Y("count()", title="Number of Responses"),
                color=alt.Color("is_remote", legend=alt.Legend(title="Remote work")),
                column=alt.Column("have_mental_helth_disorder", title=""),
            )
            .configure_header(labelFontSize=12, labelOrient="bottom")
            .properties(height=220, width=170)
            .configure_title(fontSize=18, font="Courier", anchor="middle", color="gray")
        )

    return remote_plot.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
