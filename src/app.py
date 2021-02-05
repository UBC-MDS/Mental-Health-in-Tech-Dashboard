from datetime import datetime

import altair as alt
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import html_components as hc

app = dash.Dash(__name__,
                title='Mental Health in Tech Dashboard',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

server = app.server

data = pd.read_csv("data/processed/mental_health_clean.csv")
feature_list = pd.read_csv("data/processed/features_list.csv", encoding="utf-8")
feature_list.set_index("variables", inplace=True)

today = datetime.today()
formated_date = today.strftime('%b %d, %Y')

# app layout
app.layout = dbc.Container(
    [
        html.H1("Mental Health in Tech Dashboard"),
        html.Hr(),
        hc.get_tab_section(),
        html.Footer(f"The University of British Columbia - MDS students. Last time updated on {formated_date}. All rights "
                    f"reserved.", style=hc.FOOTER_STYLE)
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
    chart = (
        alt.Chart(data, title=f"{feature_list.loc[q_selection]['variables2']}")
        .mark_bar()
        .encode(
            alt.X("gender", title=""),
            alt.Y("count()", title="Number of Responses"),
            color=alt.Color("gender", legend=None),
            column=alt.Column(q_selection, type="nominal", title=""),
        )
        .configure_header(labelFontSize=10)
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
    # To apply filters to the plot data:
    plot_data = plot_data.query(
        'work_interfere_treated != "Not applicable to me" & work_interfere_not_treated != "Not applicable to me" & @age_slider[0] <= age <= @age_slider[1]'
    )
    # To filter data for responses in the target gender:
    if gender != "all":
        plot_data = plot_data.query("gender == @gender")

    # To generate the plots:
    treated = (
        alt.Chart(plot_data, title="When Treated")
        .mark_bar(color="#a39fc9")
        .encode(
            x=alt.X(
                "work_interfere_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=alt.Axis(title=" "),
            ),
            y=alt.Y(
                "count()",
                scale=alt.Scale(domain=(0, 550)),
                axis=alt.Axis(title="Number of Responses"),
            ),
        )
        .properties(height=200, width=200)
    )
    untreated = (
        alt.Chart(plot_data, title="When Untreated")
        .mark_bar(color="#a39fc9")
        .encode(
            x=alt.X(
                "work_interfere_not_treated",
                sort=["Never", "Rarely", "Sometimes", "Often"],
                axis=alt.Axis(title=" "),
            ),
            y=alt.Y(
                "count()", scale=alt.Scale(domain=(0, 550)), axis=alt.Axis(title=" "),
            ),
        )
        .properties(height=200, width=200)
    )
    viz = alt.hconcat(
        treated,
        untreated,
        title="Does your mental health issue interfere with your work?",
    ).configure_title(fontSize=18, font="Courier", anchor="middle", color="black")
    return viz.to_html()


@app.callback(
    Output("remote_barplot", "srcDoc"),
    Input("age_slider", "value"),
    Input("gender_selection", "value"),
)
def plot_remote_work(age_slider=[15, 65], gender="all"):
    replace_dic = {
        "Maybe": "Mental Health Response:\nMaybe",
        "Yes": "Mental Health Response:\nYes",
        "No": "Mental Health Response:\nNo",
    }

    # Remove null values
    remote_df = data[data["gender"].notnull()].copy()
    remote_df["have_mental_helth_disorder"].replace(replace_dic, inplace=True)

    remote_df = remote_df.query("age >= @age_slider[0] & age <= @age_slider[1]")

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


COUNTRIES = ["United States of America", "United Kingdom", "Canada", "Germany"]


@app.callback(
    Output("formal_discuss_donutplot", "figure"), Input("formal_discuss_radio", "value")
)
def formal_discuss_donut_chart(formal_discuss="No"):
    column_name = "formal_discuss"
    return build_graph(column_name, formal_discuss)


@app.callback(
    Output("mental_health_benefits_employer_donutplot", "figure"),
    Input("mental_health_benefits_employer_radio", "value"),
)
def mental_health_benefits_employer_donut_chart(mental_health_benefits_employer="No"):
    column_name = "mental_health_benefits_employer"
    return build_graph(column_name, mental_health_benefits_employer)


@app.callback(
    Output("mental_health_leave_donutplot", "figure"),
    Input("mental_health_leave_radio", "value"),
)
def mental_health_leave_donut_chart(mental_health_leave=""):
    column_name = "mental_health_leave"
    return build_graph(column_name, mental_health_leave)


def build_graph(column_name, column_input):
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
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.44)])
    return fig.update_layout(
        autosize=False,
        width=330,
        height=330,
        legend=dict(yanchor="bottom", y=0.99, xanchor="left", x=0.01),
        margin=dict(r=20, l=0, b=0, t=0),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
