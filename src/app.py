import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import plotly.graph_objects as go
import numpy as np
import html_components as hc



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

data = pd.read_csv("data/processed/mental_health_clean_reformat.csv")
feature_list = pd.read_csv("data/processed/features_list.csv", encoding="utf-8")
feature_list.set_index("variables", inplace=True)


# app layout
app.layout = dbc.Container(
    [
        html.H1("Mental Health in Tech Dashboard"),
        html.Hr(),
        hc.get_tab_section(),
    ]
)


@app.callback(Output("tab-content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return hc.get_overview_section(data, feature_list)
    elif at == "tab-2":
        return hc.get_second_section()
    elif at== "tab-3":
        return hc.get_third_section()
    return html.P("This shouldn't ever be displayed...")


# plot specs
@app.callback(Output("gender_barplot", "srcDoc"), Input("q_selection", "value"))
def plot_gender_chart(q_selection="mental_health_benefits_employer"):
    
        # dictionary for ordering values in plot
    order_dict = {'self_employed':['Yes', 'No', 'No response'], 
            'num_employees':['1-5', '6-25', '26-100', '26-100', '100-500', '500-1000', 'More than 1000', 'No response'], 
            'tech_org': ['Yes', 'No', 'No response'],
    'mental_health_benefits_healthcare': ['Yes', 'No', 'Not eligible for coverage',"I don't know", 'No response'], 
            'mental_health_resources': ['Yes', 'No', "I don't know", 'No response'],
    'mental_health_leave': ['Very easy', 'Somewhat easy', 'Neither easy nor difficult', 'Somewhat difficult',
                            'Very difficult', "I don't know", "No response"],
            'mental_disorder_discuss': ['Yes', 'Maybe', 'No', 'No response'],
    'health_disorder_discuss': ['Yes', 'Maybe', 'No', 'No response'],
            'discuss_coworker': ['Yes', 'Maybe', 'No', 'No response'],
    'discuss_supervisor': ['Yes', 'Maybe', 'No', 'No response'], 
            'online_resources': ['Yes, I know several', 'I know some', "No, I don't know any", 'No response'], 
            'productivity': ['Yes', 'No', 'Unsure','Not applicable to me', 'No response'],
    'productivity_percent': ['1-25%', '26-50%', '51-75%','76-100%', "No response"], 
            'have_mental_helth_disorder' : ['Yes', 'Maybe', 'No', 'No response']}

    chart = (
        alt.Chart(data, title=f"{feature_list.loc[q_selection]['variables2']}").transform_joinaggregate(
        total = 'count(*)', groupby=['gender']).transform_calculate(
        pct = '1/datum.total').mark_bar().encode(
        alt.X('sum(pct):Q', axis=alt.Axis(format='%'), title = ''),
        alt.Y(q_selection, title = '', sort=order_dict[q_selection]),
        color=alt.value("#027b8e"),
        column=alt.Column("gender", type="nominal", title="")).configure_header(labelFontSize=10).configure_title(fontSize=18, font="Courier", anchor="middle", color="gray").properties(height=300, width=200)
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


@app.callback(Output("remote_barplot", "srcDoc"), Input("age_slider", "value"), Input("gender_selection", "value"))
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


COUNTRIES = ['United States of America', 'United Kingdom', 'Canada', 'Germany']


@app.callback(Output("formal_discuss_donutplot", "figure"),
              Input("formal_discuss_radio", "value"))
def formal_discuss_donut_chart(formal_discuss='No'):
    column_name = 'formal_discuss'
    return build_graph(column_name, formal_discuss)


@app.callback(Output("mental_health_benefits_employer_donutplot", "figure"),
              Input("mental_health_benefits_employer_radio", "value"))
def mental_health_benefits_employer_donut_chart(mental_health_benefits_employer='No'):
    column_name = 'mental_health_benefits_employer'
    return build_graph(column_name, mental_health_benefits_employer)


@app.callback(Output("mental_health_leave_donutplot", "figure"),
              Input("mental_health_leave_radio", "value"))
def mental_health_leave_donut_chart(mental_health_leave=''):
    column_name = 'mental_health_leave'
    return build_graph(column_name, mental_health_leave)


def build_graph(column_name, column_input):
    subset_data = data[[column_name, 'country']].copy().dropna()
    subset_data['countries'] = [x if x in COUNTRIES else 'Other' for x in subset_data['country']]
    normalize_countries = subset_data.groupby(["countries"])[column_name].value_counts(
        normalize=True).mul(
        100).unstack(
        column_name).reset_index()
    labels = normalize_countries['countries']
    values = normalize_countries[column_input]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.44)])
    return fig.update_layout(
        autosize=False,
        width=330,
        height=330,
        legend=dict(
            yanchor="bottom",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(r=20, l=0, b=0, t=0)
    )


if __name__ == "__main__":
    app.run_server(debug=True)
