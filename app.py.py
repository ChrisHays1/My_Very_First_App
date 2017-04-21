from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models.widgets import Slider, Select
from bokeh.models import CustomJS, ColumnDataSource
#from bokeh.models.widgets.layouts import column
from bokeh.layouts import column


app = Flask(__name__)

@app.route('/')
def main():

	x = [x*0.005 for x in range(0, 400)]
	y = x

	source = ColumnDataSource(data=dict(x=x, y=y))

	plot = figure(plot_width=800, plot_height=400)
	plot.line('x', 'y', source=source, line_width=3, line_alpha=1500)

	callback = CustomJS(args=dict(source=source), code="""
	    var data = source.data;
	    var f = cb_obj.value
	    x = data['x']
	    y = data['y']
	    for (i = 0; i < x.length; i++) {
	        y[i] = Math.pow(x[i], f)
	    }
	    source.trigger('change');
	""")

	slider = Slider(start=0.0001, end=10, value=1, step=.0001, title="power")
	# slider = Slider(start=0.1, end=4, value=1, step=.1, title="power", callback=callback)
	slider.js_on_change('value', callback)

	layout = column(slider, plot)

	script, div = components( layout )

	return render_template('0.html', js_resources = INLINE.render_js(), css_resources=INLINE.render_css(), script = script, div = div)


if __name__ =='__main__':
	app.run(debug=True, host='0.0.0.0')