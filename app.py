import plotly.express as px
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly
import palmerpenguins
import seaborn as sns

ui.page_opts(title="Filling layout", fillable=True)
with ui.layout_columns():

    @render_plotly
    def plot1():
        return px.histogram(px.data.tips(), y="tip")

    @render_plotly
    def plot2():
        return px.histogram(px.data.tips(), y="total_bill")


penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Valerie's Penguin Data", fillable=True)

# Sidebar content

with ui.sidebar():
    ui.h2("Sidebar")
    ui.input_selectize(
        "Selected_attribute",
        "Penguin  Details",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )
    ui.input_numeric("plotly_bin_count", "Bin_count", 1, min=1, max=15)
    ui.input_slider("seaborn_bin_count", "Seaborn bin count", 1, 100, 20)
    ui.input_checkbox_group(
        "selected_species_group",
        "select species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=True,
    )
    ui.hr()
    ui.a(
        "Valerie's GitHub Repository",
        href="https://github.com/Valpal84/cintel-02-data",
        target="_blank",
    )

# Main area content

# Display a data table and data grid in the main content area.
with ui.layout_columns():
    with ui.navset_card_pill(id="tab1"):
        with ui.nav_panel("Data Table"):

            @render.data_frame
            def penguins_data_table():
                return render.DataTable(penguins_df)

        with ui.nav_panel("Data Grid"):

            @render.data_frame
            def penguins_data_grid():
                return render.DataGrid(penguins_df)

    # Display a plotly histogram showing all species
    with ui.navset_card_pill(id="tab2"):
        with ui.nav_panel("Penguin Histogram"):

            @render_plotly
            def plotly_histogram():
                plotly_hist = px.histogram(
                    data_frame=penguins_df,
                    x=input.Selected_attribute(),
                    nbins=input.plotly_bin_count(),
                    color="species",
                ).update_layout(
                    title="Penguins Plotly Data",
                    xaxis_title="Selected Attribute",
                    yaxis_title="Count",
                )
                return plotly_hist

    # Display a seaborn histogram showing all species
    with ui.navset_card_pill(id="tab3"):
        with ui.nav_panel("Seaborn Penguin Histogram"):
            @render.plot
            def seaborn_histogram():
               histplot = sns.histplot(data=penguins_df, x="body_mass_g", hue="species", bins=input.seaborn_bin_count())
               histplot.set_title("Palmer Penguins")
               histplot.set_xlabel("Mass")
               histplot.set_ylabel("Count")
               sns.set_style('darkgrid')
               return histplot 

    # Display a plotly Scatterplot showing all species
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                penguins_df,
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                color_discrete_map={
                    'Adelie': 'purple',
                    'Chinstrap': 'green',
                    'Gentoo': 'yellow'},
            )
                

