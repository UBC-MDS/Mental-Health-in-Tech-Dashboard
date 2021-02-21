from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    "height": "25px",
    "padding": "3px 0 0 5px",
    "backgroundColor": "#3c3d58",
    "color": "white",
    "fontSize": "small",
}

PLOTLY_LOGO = "assets/img/1111512.png"

today = datetime.now()
formatted_date = today.strftime("%b %d, %Y")


def get_overview_section(data, feature_list):
    plot1 = html.Div(
        [
            html.Br(),
            dbc.Row(
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Quick Info", className="card-title"),
                                html.P(
                                    "The Mental Health in Tech Dashboard dashboard visualizes a dataset consisting of survey questions and responses about various aspects of the mental health of tech workers. It shows both an overview of the survey responses as well as additional visualizations specifically relevant to HR domain experts. The dataset used and github source are available in the links below.",
                                    className="card-text",
                                ),
                                dbc.CardLink(
                                    "Dataset",
                                    href="https://www.kaggle.com/osmi/mental-health-in-tech-2016",
                                    target="_blank",
                                ),
                                dbc.CardLink(
                                    "Github Source",
                                    href="https://github.com/UBC-MDS/Mental-Health-in-Tech-Dashboard",
                                    target="_blank",
                                ),
                            ]
                        ),
                    )
                ]),
            ),
            html.Hr(),
            dbc.Row(
                dbc.Col([
                    html.H3("Data overview for different survey questions"),
                    html.Br()
                ]),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                id="q_selection",
                                value="tech_org",
                                options=[
                                    {
                                        "label": feature_list.loc[i]["variables3"],
                                        "value": i,
                                    }
                                    for i in np.r_[data.columns[0:14]]
                                ],
                            ),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            html.Iframe(
                                id="gender_barplot",
                                style={
                                    "width": "100%",
                                    "height": "500px",
                                    "border": "0px",
                                },
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
    return plot1


def get_second_section():
    section2 = html.Div(
        [
            html.Hr(),
            dbc.Row(
                dbc.Col([
                    html.H3("Human Resources questions for different groups of respondents"),
                    html.Br()
                ]),
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Gender"),
                            dcc.RadioItems(
                                id="gender_selection",
                                options=[
                                    {"label": "All", "value": "all"},
                                    {"label": "Male", "value": "Male"},
                                    {"label": "Female", "value": "Female"},
                                    {"label": "Others", "value": "Other"},
                                ],
                                value="all",
                                inputStyle={"marginLeft": "20px", "marginRight": "5px"},
                                labelStyle={"display": "block"},
                            ),
                            html.Br(),
                            html.H5("Age of Respondents:"),
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
                        style={
                            "padding": 15,
                            "borderRadius": 6,
                        },
                    ),
                    dbc.Col(
                        [
                            html.Iframe(
                                id="work_interfere_barplot",
                                style={
                                    "width": "100%",
                                    "height": "400px",
                                    "border": "0px",
                                },
                            ),
                            html.Iframe(
                                id="remote_barplot",
                                style={
                                    "width": "100%",
                                    "height": "400px",
                                    "border": "0px",
                                },
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )

    return section2


def get_third_section():
    section3 = html.Div(
        [
            html.Hr(),
            dbc.Row(
                dbc.Col([
                    html.H3("Employee benefits and wellness programs in different countries"),
                    html.Br()
                ]),
            ),
            dbc.Row(
                [

                    dbc.Col(
                        [
                            html.P(
                                "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?"
                            ),
                            dcc.RadioItems(
                                id="formal_discuss_radio",
                                options=[
                                    {"label": "Yes", "value": "Yes"},
                                    {"label": "No", "value": "No"},
                                    {"label": "I don't know", "value": "I don't know"},
                                ],
                                value="Yes",
                                inputStyle={"marginLeft": "20px", "marginRight": "5px"},
                                labelStyle={"display": "block"},
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col([dcc.Graph(id="formal_discuss_donutplot", ), ], md=6, )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "Do you know the options for mental health care available under your employer-provided coverage?"
                            ),
                            dcc.RadioItems(
                                id="mental_health_benefits_employer_radio",
                                options=[
                                    {"label": "Yes", "value": "Yes"},
                                    {"label": "No", "value": "No"},
                                    {
                                        "label": "I am not sure",
                                        "value": "I am not sure",
                                    },
                                ],
                                value="Yes",
                                inputStyle={"marginLeft": "20px", "marginRight": "5px"},
                                labelStyle={"display": "block"},
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [dcc.Graph(id="mental_health_benefits_employer_donutplot"), ],
                        md=6,
                    ),
                ]),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P(
                                "If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:"
                            ),
                            dcc.RadioItems(
                                id="mental_health_leave_radio",
                                options=[
                                    {"label": "Very easy", "value": "Very easy"},
                                    {
                                        "label": "Somewhat easy",
                                        "value": "Somewhat easy",
                                    },
                                    {
                                        "label": "Neither easy nor difficult",
                                        "value": "Neither easy nor difficult",
                                    },
                                    {
                                        "label": "Somewhat difficult",
                                        "value": "Somewhat difficult",
                                    },
                                    {
                                        "label": "Very difficult",
                                        "value": "Very difficult",
                                    },
                                ],
                                value="Very easy",
                                inputStyle={"marginLeft": "20px", "marginRight": "5px"},
                                labelStyle={"display": "block"},
                            ),
                        ],
                        md=6,
                    ),
                    dbc.Col([dcc.Graph(id="mental_health_leave_donutplot"), ], md=6, ),
                ],
            ),
        ]
    )

    return section3


def get_tab_section():
    tab_section = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Overview", tab_id="tab-1"),
                    dbc.Tab(label="HR Questions", tab_id="tab-2"),
                    dbc.Tab(label="Employee Benefits Questions", tab_id="tab-3"),
                ],
                id="tabs",
                active_tab="tab-1",
            ),
            html.Div(id="tab-content"),
        ]
    )
    return tab_section


navbar = dbc.NavbarSimple(
    html.Img(src=PLOTLY_LOGO, height="70px"),
    brand="Mental Health in Tech Dashboard",
    brand_href="#",
    color="#3c3d58",
    dark=True,
)

container = dbc.Container(
    [
        # html.H1("Mental Health in Tech Dashboard"),
        html.Br(),
        get_tab_section(),
        html.Footer(
            [f"(C) Copyright UBC-MDS students: Chirag Rank, Fatime Selimi, Mike Lynch, Selma Duric. ",
             f"Last time updated on {formatted_date}."],
            style=FOOTER_STYLE,
        ),
    ]
)
