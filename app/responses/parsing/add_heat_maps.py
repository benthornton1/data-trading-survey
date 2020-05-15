from abc import ABC, abstractmethod

from bokeh.embed import components
from bokeh.models import (
    ColorBar,
    BasicTicker,
    LinearColorMapper,
    ColumnDataSource,
)
from bokeh.models.formatters import FuncTickFormatter
from bokeh.palettes import plasma
from bokeh.plotting import figure
from bokeh.transform import transform
import pandas as pd
from sqlalchemy import desc

from app import db
from app.models import Card, Response, CardPosition, DataValue
from app.responses.parsing.calculate_response_max_min import calculate_response_min, calculate_response_max


class CreateHeatMap(ABC):
    def __init__(self, study):
        self.study = study
        self.palette = tuple(reversed(plasma(10)))
        self.plots = []
        self.mapper = None

    def add(self, card_x, card_y, data_value_label):
        self.create_plots(card_x, card_y, data_value_label)

    @abstractmethod
    def create_plots(self, card_x, card_y, data_value_label):
        pass

    def create_heat_map(self, title, tooltips, card_x, card_y, data):

        x_range = list(range(self.study.number_of_columns))
        y_range = list(range(self.study.number_of_rows))

        df = pd.DataFrame(data=data)
        source = ColumnDataSource(df)

        plot = figure(
            title=title,
            plot_width=300,
            plot_height=300,
            toolbar_location=None,
            tools="",
            x_range=[str(x) for x in x_range],
            y_range=[str(y) for y in y_range],
            x_axis_label=card_x.name,
            y_axis_label=card_y.name,
            tooltips=tooltips,
        )

        plot.rect(
            x="col",
            y="row",
            width=1,
            height=1,
            source=df,
            fill_color={"field": "values", "transform": self.mapper},
            line_color=None,
        )
        color_bar = ColorBar(
            color_mapper=self.mapper,
            location=(0, 0),
            ticker=BasicTicker(desired_num_ticks=len(self.palette)),
        )
        plot.add_layout(color_bar, "right")
        plot.axis.axis_line_color = None
        plot.axis.major_tick_line_color = None
        plot.axis.major_label_text_font_size = "5pt"
        plot.axis.major_label_standoff = 0
        plot.xaxis.major_label_orientation = 1.0

        template = """
            if(index==0){
                return 'Lowest %s'
            } else if(index == ticks.length-1){
                return 'Highest %s'
            } else {
                return tick
            }
        """
        x_axis_format = template % (
            self.study.card_set_x.measure,
            self.study.card_set_x.measure,
        )
        y_axis_format = template % (
            self.study.card_set_y.measure,
            self.study.card_set_y.measure,
        )
        plot.xaxis.formatter = FuncTickFormatter(code=x_axis_format)
        plot.yaxis.formatter = FuncTickFormatter(code=y_axis_format)
        plot.xaxis.group_text_font = "Helvetica Neue"
        plot.yaxis.group_text_font = "Helvetica Neue"

        plot.xaxis.axis_label_text_font = "Helvetica Neue"
        plot.yaxis.axis_label_text_font = "Helvetica Neue"
        plot.xaxis.axis_label_text_font_style = "normal"
        plot.yaxis.axis_label_text_font_style = "normal"

        script_heatmap, div_heatmap = components(plot)
        self.plots.append((script_heatmap, div_heatmap))

    def calculate_count(self, card_x, card_y):
        values = {}

        for col in range(self.study.number_of_columns):
            for row in range(self.study.number_of_rows):
                values["col_" + str(col) + "_row_" + str(row)] = None

        for response in self.study.responses:
            try:
                card_x_pos = (
                    CardPosition.query.filter(CardPosition.response_id == response.id)
                    .filter(CardPosition.card == card_x)
                    .first()
                )
                card_y_pos = (
                    CardPosition.query.filter(CardPosition.response_id == response.id)
                    .filter(CardPosition.card == card_y)
                    .first()
                )

                if (
                    values[
                        "col_"
                        + str(card_x_pos.position)
                        + "_row_"
                        + str(card_y_pos.position)
                    ]
                    is None
                ):
                    values[
                        "col_"
                        + str(card_x_pos.position)
                        + "_row_"
                        + str(card_y_pos.position)
                    ] = 1
                else:
                    values[
                        "col_"
                        + str(card_x_pos.position)
                        + "_row_"
                        + str(card_y_pos.position)
                    ] += 1
            except AttributeError:
                pass

        data = {"col": [], "row": [], "values": []}

        for col_row, value in values.items():
            data["col"].append(str(col_row.split("_")[1]))
            data["row"].append(str(col_row.split("_")[3]))
            data["values"].append(value)

        return data

    def calculate_price(self, card_x, card_y, data_value_label):
        values = {}

        for col in range(self.study.number_of_columns):
            for row in range(self.study.number_of_rows):
                values["col_" + str(col) + "_row_" + str(row)] = None

        for response in self.study.responses:
            try:
                card_x_pos = (
                    CardPosition.query.filter(CardPosition.response_id == response.id)
                    .filter(CardPosition.card == card_x)
                    .first()
                )
                card_y_pos = (
                    CardPosition.query.filter(CardPosition.response_id == response.id)
                    .filter(CardPosition.card == card_y)
                    .first()
                )

                max_val = calculate_response_max(response, data_value_label)
                min_val = calculate_response_min(response, data_value_label)
                
                data_value = (
                    DataValue.query.filter(DataValue.response_id == response.id)
                    .filter(DataValue.column == card_x_pos.position)
                    .filter(DataValue.row == card_y_pos.position)
                    .filter(DataValue.data_value_label == data_value_label)
                    .first()
                )
                col_row = (
                    "col_"
                    + str(card_x_pos.position)
                    + "_row_"
                    + str(card_y_pos.position)
                )

                if values[col_row] is None:
                    values[col_row] = (data_value.value - min_val) / (max_val - min_val)
                else:
                    values[col_row] += (data_value.value - min_val) / (
                        max_val - min_val
                    )
            except AttributeError:
                pass

        data = {"col": [], "row": [], "values": []}

        for col_row, value in values.items():
            data["col"].append(str(col_row.split("_")[1]))
            data["row"].append(str(col_row.split("_")[3]))
            data["values"].append(value)

        normalised_average_values = []
        count_data = self.calculate_count(card_x, card_y)

        for normalised_val, count in zip(data["values"], count_data["values"]):
            if normalised_val is not None and count_data is not None:
                normalised_average_values.append(float("{:.2f}".format(normalised_val / count)))
            else:
                normalised_average_values.append(None)

        data["values"] = normalised_average_values
        return data


class CreateOneHeatMapCount(CreateHeatMap):
    def create_plots(self, card_x, card_y, data_value_label):
        self.mapper = LinearColorMapper(
            palette=self.palette, low=0, high=len(self.study.responses)
        )
        title = "Count"

        data = self.calculate_count(card_x, card_y)

        tooltips = """ <div> Count: @values </div> """
        self.create_heat_map(title, tooltips, card_x, card_y, data)


class CreateOneHeatMap(CreateHeatMap):
    def create_plots(self, card_x, card_y, data_value_label):
        self.mapper = LinearColorMapper(palette=self.palette, low=0, high=1)
        title = data_value_label.label

        data = self.calculate_price(card_x, card_y, data_value_label)

        tooltips = """ <div> Value: @values </div> """

        self.create_heat_map(title, tooltips, card_x, card_y, data)
