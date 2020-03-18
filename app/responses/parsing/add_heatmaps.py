from abc import ABC, abstractmethod
from app import db
from app.models import HeatMap, Card
from sqlalchemy import desc
import pandas as pd
from bokeh.models import ColorBar, BasicTicker, LinearColorMapper, ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.formatters import FuncTickFormatter
from bokeh.transform import transform
from bokeh.palettes import grey
import pdb

class CreateHeatMaps(ABC):
    
    def add(self, study, card_x_id=None, card_y_id=None):
        heat_maps = None
        if card_x_id==None or card_y_id==None:
            heat_maps = self.get_heatmaps(study_id=study.id, card_x_id=None, card_y_id=None)
        else:
            heat_maps = self.get_heatmaps(study_id=study.id, card_x_id=card_x_id, card_y_id=card_y_id)
        plots = self.create_plots(study, heat_maps)
        return plots
    
        
    @abstractmethod
    def get_heatmaps(self, study_id, card_x_id=None, card_y_id=None):
        pass
    
    def create_plots(self, study, heat_maps):
        heat_map_plots = []
        card_set_x = study.card_sets[0]
        card_set_y = study.card_sets[1]
        palette = tuple(reversed(grey(10)))

        for heat_map in heat_maps:
            data = {'col':[], 'row':[], 'values':[]}
            for col_row,value in heat_map.values.items():
                split = col_row.split('-')
                data['col'].append(split[1])
                data['row'].append(split[3])
                data['values'].append(value)
            
            df = pd.DataFrame(data=data)
            source = ColumnDataSource(df)
            mapper = LinearColorMapper(palette=palette, low=0, high=1)        
            
            x_range = list(range(study.number_of_columns))
            y_range = list(range(study.number_of_rows))
        
            
            p = figure(title=str(heat_map.data_value_label),plot_width=300, plot_height=300, toolbar_location=None, tools="",
                    x_range=[str(x) for x in x_range], y_range=[str(y) for y in y_range], x_axis_label=heat_map.card_x.name, y_axis_label=heat_map.card_y.name)
            
            p.rect(x="col", y="row", width=1, height=1, source=source,fill_color=transform('values', mapper),
                line_color=None)
            color_bar = ColorBar(color_mapper=mapper, location=(0, 0),
                            ticker=BasicTicker(desired_num_ticks=len(palette)),
                        )
            
            p.add_layout(color_bar, 'right')
            p.axis.axis_line_color = None
            p.axis.major_tick_line_color = None
            p.axis.major_label_text_font_size = "5pt"
            p.axis.major_label_standoff = 0
            p.xaxis.major_label_orientation = 1.0
            
            template = """
                if(index==0){
                    return 'Lowest %s'
                } else if(index == ticks.length-1){
                    return 'Highest %s'
                } else {
                    return tick
                }
            """
            x_axis_format = template % (card_set_x.measure, card_set_x.measure)
            y_axis_format = template % (card_set_y.measure, card_set_y.measure)
            p.xaxis.formatter = FuncTickFormatter(code = x_axis_format)
            p.yaxis.formatter = FuncTickFormatter(code = y_axis_format)
            p.xaxis.group_text_font = 'Helvetica Neue' 
            p.yaxis.group_text_font = 'Helvetica Neue'
            
            p.xaxis.axis_label_text_font = 'Helvetica Neue'
            p.yaxis.axis_label_text_font = 'Helvetica Neue'
            p.xaxis.axis_label_text_font_style = 'normal'
            p.yaxis.axis_label_text_font_style = 'normal'
            
            script_heatmap, div_heatmap = components(p)
            heat_map_plots.append((script_heatmap, div_heatmap))
    
        return heat_map_plots
            
    
class CreateAllHeatMaps(CreateHeatMaps):
    
    def get_heatmaps(self, study_id, card_x_id=None, card_y_id=None):
        heat_maps = (db.session.query(HeatMap)
                        .filter_by(study=study_id)
                        .join(Card, HeatMap.card_y_id==Card.id)
                        .order_by(desc(Card.name))
                        .all())
        return heat_maps
    
class CreateOneHeatMap(CreateHeatMaps):
    
    def get_heatmaps(self, study_id, card_x_id, card_y_id):
        heat_map = (HeatMap.query.filter(HeatMap.study==study_id,
                                         HeatMap.card_y_id==int(card_x_id),
                                         HeatMap.card_x_id==int(card_y_id)).first())
        
        return [heat_map]