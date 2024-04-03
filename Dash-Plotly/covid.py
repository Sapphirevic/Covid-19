import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv("cleaned_data.csv")

df["Total_Tests"] = pd.to_numeric(df["Total_Tests"], errors="coerce")
df["Population(pop)"] = pd.to_numeric(df["Population(pop)"], errors="coerce")

df["Recovery_Rate"] = df["Recovered"] / df["Total_Cases"]

top_countries_recovery_rate = df.sort_values("Recovery_Rate", ascending=False).head(10)

app = dash.Dash(__name__)

fig_total_cases = px.bar(
    df.sort_values("Total_Cases", ascending=False).head(10),
    x="Country",
    y="Total_Cases",
    title="Top 10 Countries by Total COVID-19 Cases",
)

fig_total_deaths_pie = px.pie(
    df.sort_values("Total_Deaths", ascending=False).head(10),
    values="Total_Deaths",
    names="Country",
    title="Top 10 Countries with the most recorded Deaths",
)
fig_recovery_rate_line = px.line(
    top_countries_recovery_rate,
    x="Country",
    y="Recovery_Rate",
    title="Top 10 Countries by COVID-19 Recovery Rate",
)
stacked_bar_data = df.sort_values("Total_Cases", ascending=False).head(20)[
    ["Country", "Active_Cases", "Recovered", "Total_Deaths"]
]
fig_stacked_bar = px.bar(
    stacked_bar_data,
    x="Country",
    y=["Active_Cases", "Recovered", "Total_Deaths"],
    title="Top 20 Countries by (Active, Recovered, Deaths)",
    barmode="stack",
)

fig_critical_cases = px.bar(
    df.sort_values("Critical_Cases", ascending=False).head(10),
    x="Country",
    y="Critical_Cases",
    title="Top 10 Countries with high Critical Cases",
)
fig_bubble = px.scatter(
    df,
    x="Total_Cases",
    y="Total_Deaths",
    size="Recovered",
    color="Country",
    hover_name="Country",
    log_x=True,
    log_y=True,
    title="Total Cases vs Total Deaths (Bubble Chart)",
    labels={
        "Total_Cases": "Total Cases",
        "Total_Deaths": "Total Deaths",
    },
)


app.layout = html.Div(
    [
        html.H1("COVID-19 Data Visualization"),
        dcc.Dropdown(
            id="metric-dropdown",
            options=[
                {"label": "Total Cases", "value": "Total_Cases"},
                {"label": "Total Deaths", "value": "Total_Deaths"},
                {"label": "Total Recoveries", "value": "Recovered"},
            ],
            value="Total_Cases",
        ),
        dcc.Graph(id="covid-graph"),
        html.Hr(),  # Adding a horizontal line for separation
        html.H2("Top 10 Countries by Various Metrics"),
        dcc.Graph(figure=fig_total_cases, id="fig_total_cases"),
        dcc.Graph(figure=fig_total_deaths_pie, id="fig_total_deaths_pie"),
        dcc.Graph(figure=fig_recovery_rate_line, id="fig_recovery_rate_line"),
        dcc.Graph(figure=fig_stacked_bar, id="fig_stacked_bar"),
        dcc.Graph(figure=fig_critical_cases, id="fig_critical_cases"),
        dcc.Graph(figure=fig_bubble, id="fig_bubble"),
    ]
)


@app.callback(Output("covid-graph", "figure"), [Input("metric-dropdown", "value")])
def update_graph(selected_metric):
    choro = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color=selected_metric,
        hover_name="Country",
        title=f"COVID-19 {selected_metric} by Country",
        labels={selected_metric: "Number recorded"},
    )
    return choro


if __name__ == "__main__":
    app.run(port=4050, debug=True)
