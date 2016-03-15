from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		app.vars['stock'] = request.form['stock_form']
		app.vars['options'] = request.form.getlist('options')
		print(app.vars['options'])
		return redirect('/result')

@app.route('/result')
def graph():
	import requests
	import simplejson as json
	import pandas as pd
	from StringIO import StringIO

	import time
	from datetime import datetime
	from bokeh.plotting import figure, show, output_file, vplot
	from bokeh.embed import components

	q_key = 'GzvNgrVEuh3HdRwksr5e'
	stock = app.vars['stock'].upper()
	num_points = 300
	show_this = app.vars['options']
	#show_this = ['Open','Close']
	colors = ['#C4CDE9','#FFFEC9','#FBD4DA','#EED2F0']

	try:

		r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=%s'%(stock,q_key))
		df = pd.read_csv(StringIO(r.text),header=0,parse_dates=['Date'])

		path = '/Users/juanmanuelsanchez/Documents/data_science_incubator/heroku-stuff/'
		dates = df.Date[:num_points]
		TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

		r = figure(x_axis_type = "datetime",tools=TOOLS)

		for ticker, color in zip(show_this,colors[:len(show_this)]):
		    y = df[ticker][:num_points]
		    r.line(dates, y, color=color, legend = stock + ': ' + ticker)

		output_file(path + "correlation.html", title="correlation.py example")

		r.title = "Stock Returns. Data from Quandl"
		r.grid.grid_line_alpha=0.3

		from bokeh.resources import CDN
		from bokeh.embed import file_html

		script, div = components(r)

		return render_template('graph.html',div=div,script=script)
	except:
		return render_template('graph.html',div="<div><h1>Something went wrong! (e.g. no ticker with that name)</h1></div>",script='')
	#app.vars['html'] = html

if __name__ == '__main__':
  app.run(port=33507)
