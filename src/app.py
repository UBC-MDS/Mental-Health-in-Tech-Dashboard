from datetime import datetime

import altair as alt
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from plotly import graph_objects as go

import html_components as hc

app = dash.Dash(
    __name__,
    title="Mental Health in Tech Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

server = app.server

data = pd.read_csv("data/processed/mental_health_clean_reformat.csv")
feature_list = pd.read_csv("data/processed/features_list.csv", encoding="utf-8")
feature_list.set_index("variables", inplace=True)

today = datetime.today()
formated_date = today.strftime("%b %d, %Y")

# app layout
app.layout = dbc.Container(
    [
        html.H1("Mental Health in Tech Dashboard"),
        html.Hr(),
        hc.get_tab_section(),
        html.Footer(
            [f"(C) Copyright UBC-MDS students. Last time updated on {formated_date}",
             html.Br(),
             f"Authors: Chirag Rank, Fatime Selimi, Mike Lynch, Selma Duric. All rights reserved."],
            style=hc.FOOTER_STYLE,
        ),
    ]
)


@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return hc.get_overview_section(data, feature_list)
    elif at == "tab-2":
        return hc.get_second_section()
    elif at == "tab-3":
        return hc.get_third_section()
    return html.P("This shouldn't ever be displayed...")


# plot specs
@app.callback(Output("gender_barplot", "srcDoc"), Input("q_selection", "value"))
def plot_gender_chart(q_selection="mental_health_benefits_employer"):
    """Generates a bar plot grouped by gender and y-axis determined my provided variable name found in dataframe

    Parameters
    ----------
    q_selection : str, optional
        variable name to populate on y-axis, by default "mental_health_benefits_employer"

    Returns
    -------
    chart in html format
    """
    # dictionary for ordering values in plot
    order_dict = {
        "self_employed": ["Yes", "No", "No response"],
        "num_employees": [
            "1-5",
            "6-25",
            "26-100",
            "26-100",
            "100-500",
            "500-1000",
            "More than 1000",
            "No response",
        ],
        "tech_org": ["Yes", "No", "No response"],
        "mental_health_benefits_healthcare": [
            "Yes",
            "No",
            "Not eligible for coverage",
            "I don't know",
            "No response",
        ],
        "mental_health_resources": ["Yes", "No", "I don't know", "No response"],
        "mental_health_leave": [
            "Very easy",
            "Somewhat easy",
            "Neither easy nor difficult",
            "Somewhat difficult",
            "Very difficult",
            "I don't know",
            "No response",
        ],
        "mental_disorder_discuss": ["Yes", "Maybe", "No", "No response"],
        "health_disorder_discuss": ["Yes", "Maybe", "No", "No response"],
        "discuss_coworker": ["Yes", "Maybe", "No", "No response"],
        "discuss_supervisor": ["Yes", "Maybe", "No", "No response"],
        "online_resources": [
            "Yes, I know several",
            "I know some",
            "No, I don't know any",
            "No response",
        ],
        "productivity": ["Yes", "No", "Unsure", "Not applicable to me", "No response"],
        "productivity_percent": ["1-25%", "26-50%", "51-75%", "76-100%", "No response"],
        "have_mental_helth_disorder": ["Yes", "Maybe", "No", "No response"],
    }

    chart = (
        alt.Chart(
            data.fillna("No response"),
            title=f"{feature_list.loc[q_selection]['variables2']}",
        )
            .transform_joinaggregate(total="count(*)", groupby=["gender"])
            .transform_calculate(pct="1/datum.total")
            .mark_bar()
            .encode(
            alt.X("sum(pct):Q", axis=alt.Axis(format="%"), title=""),
            alt.Y(q_selection, title="", sort=order_dict[q_selection]),
            color=alt.value("#027b8e"),
            column=alt.Column("gender", type="nominal", title=""),
        )
            .configure_header(labelFontSize=12)
            .configure_axis(labelFontSize=12)
            .configure_title(fontSize=18, font="Courier", anchor="middle", color="black")
            .properties(height=300, width=200)
    )
    return chart.to_html()


@app.callback(
    Output("work_interfere_barplot", "srcDoc"),
    Input("age_slider", "value"),
    Input("gender_selection", "value"),
)
def plot_work_interfere_bars(age_slider=[15, 65], gender="all"):
    """
    Function that makes the first visualization on the second tab of the dashboard 

    Parameters:
    ----------
    age_slider (int):
        the range of survey respondent ages
    gender (str):
        the gender of the survey respondent

    Returns:
    ----------
    viz
        the html plot
    """
    plot_data = data
    # To apply filters to the plot data:
    plot_data = plot_data.query(
        'work_interfere_treated != "Not applicable to me" & work_interfere_not_treated != "Not applicable to me" & @age_slider[0] <= age <= @age_slider[1]'
    )
    # To filter data for responses in the target gender:
    if gender != "all":
        plot_data = plot_data.query("gender == @gender")

    # To generate the plots:
    title1 = (
        alt.Chart({"values": [{"text": "When Treated"}]})
            .mark_text(dx=100, size=12, font="Courier", color="black")
            .encode(text="text:N")
    )
    treated = alt.vconcat(
        title1,
        alt.Chart(plot_data)
            .mark_bar(color="#a39fc9")
            .encode(
            x=alt.X(
                "work_interfere_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=alt.Axis(title=" ", labelAngle=-45, ),
            ),
            y=alt.Y(
                "count()",
                scale=alt.Scale(domain=(0, 550)),
                axis=alt.Axis(title="Number of Responses"),
            ),
        )
            .properties(height=200, width=200),
    )
    title2 = (
        alt.Chart({"values": [{"text": "When Untreated"}]})
            .mark_text(dx=100, size=12, font="Courier", color="black")
            .encode(text="text:N")
    )

    untreated = alt.vconcat(
        title2,
        alt.Chart(plot_data)
            .mark_bar(color="#a39fc9")
            .encode(
            x=alt.X(
                "work_interfere_not_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=alt.Axis(title=" ", labelAngle=-45, ),
            ),
            y=alt.Y(
                "count()", scale=alt.Scale(domain=(0, 550)), axis=alt.Axis(title=" "),
            ),
        )
            .properties(height=200, width=200),
    )
    viz = (
        alt.hconcat(
            treated,
            untreated,
            title="Does your mental health issue interfere with your work?",
        )
            .configure_title(fontSize=18, font="Courier", anchor="middle", color="black")
            .configure_view(stroke=None)
            .configure_concat(spacing=1)
    )
    return viz.to_html()


@app.callback(
    Output("remote_barplot", "srcDoc"),
    Input("age_slider", "value"),
    Input("gender_selection", "value"),
)
def plot_remote_work(age_slider=[15, 65], gender="all"):
    """
    Function that makes the second visualization on the second tab of the dashboard

    Parameters:
    ----------
    age_slider (int):
        the range of survey respondent ages
    gender (str):
        the gender of the survey respondent

    Returns:
    ----------
    viz
        the html plot
    """
    replace_dic = {
        "Never": "Remote work: Never",
        "Sometimes": "Remote work: Sometimes",
        "Always": "Remote work: Always",
    }
    # Remove null values
    remote_df = data[data["gender"].notnull()].copy()
    remote_df["is_remote"].replace(replace_dic, inplace=True)

    remote_df = remote_df.query("@age_slider[0] <= age <= @age_slider[1]")

    # Default condition
    if gender == "all":
        remote_plot = (
            alt.Chart(
                remote_df,
                title="Do employees that work remotely report fewer mental health issues?",
            )
                .mark_bar(color="#a39fc9")
                .encode(
                x=alt.X(
                    "have_mental_helth_disorder",
                    title="",
                    axis=alt.Axis(labelAngle=-45),
                    sort=["No", "Maybe", "Yes"],
                ),
                y=alt.Y(
                    "count()",
                    title="Number of Responses",
                    scale=alt.Scale(domain=(0, 350)),
                ),
                column=alt.Column(
                    "is_remote",
                    title="",
                    header=alt.Header(labelOrient="top"),
                    sort=[
                        "Remote work: Never",
                        "Remote work: Sometimes",
                        "Remote work: Always",
                    ],
                ),
            )
                .configure_header(labelFontSize=12)
                .properties(height=220, width=170)
                .configure_title(fontSize=18, font="Courier", anchor="middle")
        )
    else:
        # Selected Filter condition
        remote_plot = (
            alt.Chart(
                remote_df[remote_df["gender"] == gender],
                title="Do employees that work remotely report fewer mental health issues?",
            )
                .mark_bar(color="#a39fc9")
                .encode(
                x=alt.X(
                    "have_mental_helth_disorder",
                    title="",
                    axis=alt.Axis(labelAngle=-45),
                    sort=["No", "Maybe", "Yes"],
                ),
                y=alt.Y(
                    "count()",
                    title="Number of Responses",
                    scale=alt.Scale(domain=(0, 350)),
                ),
                column=alt.Column(
                    "is_remote",
                    title="",
                    header=alt.Header(labelOrient="top"),
                    sort=[
                        "Remote work: Never",
                        "Remote work: Sometimes",
                        "Remote work: Always",
                    ],
                ),
            )
                .configure_header(labelFontSize=12)
                .properties(height=220, width=170)
                .configure_title(fontSize=18, font="Courier", anchor="middle")
        )

    return remote_plot.to_html()


COUNTRIES = ["United States of America", "United Kingdom", "Canada", "Germany"]

donut_chart_colors = ['#ccb22b', '#84d0c0', '#8175aa', '#027b8e', '#959c9e']


@app.callback(
    Output("formal_discuss_donutplot", "figure"),
    Input("formal_discuss_radio", "value")
)
def formal_discuss_donut_chart(formal_discuss="No"):
    """
    Function that makes the first donut chart visualization on the third tab of the dashboard

    Parameters:
    ----------
    formal_discuss (str):
        the value of the input of formal_discuss from callback

    Returns:
    ----------
    viz
        the html plot
    """
    column_name = "formal_discuss"
    return build_graph(column_name, formal_discuss)


@app.callback(
    Output("mental_health_benefits_employer_donutplot", "figure"),
    Input("mental_health_benefits_employer_radio", "value"),
)
def mental_health_benefits_employer_donut_chart(mental_health_benefits_employer="No"):
    """
    Function that makes the second donut chart visualization on the third tab of the dashboard

    Parameters:
    ----------
    mental_health_benefits_employer (str):
        the value of the input of mental_health_benefits_employer from callback

    Returns:
    ----------
    viz
        the html plot
    """
    column_name = "mental_health_benefits_employer"
    return build_graph(column_name, mental_health_benefits_employer)


@app.callback(
    Output("mental_health_leave_donutplot", "figure"),
    Input("mental_health_leave_radio", "value"),
)
def mental_health_leave_donut_chart(mental_health_leave=""):
    """
    Function that makes the third donut chart visualization on the third tab of the dashboard

    Parameters:
    ----------
    mental_health_leave (str):
        the value of the input of mental_health_leave from callback

    Returns:
    ----------
    viz
        the html plot
    """
    column_name = "mental_health_leave"
    return build_graph(column_name, mental_health_leave)


def build_graph(column_name, column_input):
    """
    Helper function that build a donut chart

    Parameters:
    ----------
    column_name (str):
        the name of the column to create the plot for
    column_input (str):
        the value of the input from the callback function

    Returns:
    ----------
    viz
        a plotly plot
    """
    subset_data = data[[column_name, "country"]].copy().dropna()
    subset_data["countries"] = [
        x if x in COUNTRIES else "Other" for x in subset_data["country"]
    ]
    normalize_countries = (
        subset_data.groupby(["countries"])[column_name]
            .value_counts(normalize=True)
            .mul(100)
            .unstack(column_name)
            .reset_index()
    )
    labels = normalize_countries["countries"]
    values = normalize_countries[column_input]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.44, sort=False,
                                 marker={'colors': donut_chart_colors})])
    return fig.update_layout(
        autosize=False,
        width=330,
        height=330,
        legend=dict(yanchor="bottom", y=0.99, xanchor="left", x=0.01),
        margin=dict(r=20, l=0, b=0, t=0),
        legend_itemdoubleclick=False
    )


if __name__ == "__main__":
    app.run_server(debug=True)
