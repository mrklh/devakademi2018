# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from dt import create_dt
import numpy as np
from functools import reduce

app = Flask(__name__)
clf, cat_dict, job_dict = create_dt()

def get_ranges(cnt):
	'''
	Boş bırakılan alanlar için bütün ihtimallerin dönmesini sağlar.
	'''
	if cnt == 0:
		return range(2)
	elif cnt == 1:
		return range(6)
	elif cnt == 2:
		return range(4)
	elif cnt == 3:
		return range(2)
	elif cnt == 4:
		return range(len(job_dict.keys()))
	elif cnt == 5:
		return range(6)
	elif cnt == 6:
		return range(len(cat_dict.keys()))

def get_possibility(inp):
	'''
	Bütün ihtimalleri predict edip average'ını bulur.
	'''
	inputs = []
	for cnt, value in enumerate(inp):
		if value == '-1' or value == -1:
			inputs.append(get_ranges(cnt))
		else:
			inputs.append([value])

	dt_inp = np.zeros((reduce(lambda x, y: x*y, [len(i) for i in inputs]), 7))

	for cnt, inp in enumerate(inputs):
		times = dt_inp.shape[0]/len(inp)

		for i in range(times):
			for j in range(len(inp)):
				dt_inp[i*len(inp) + j,cnt] = inp[j]

	x = clf.predict_proba(dt_inp)
	return np.sum(x, 0)/float(len(x))

@app.route('/')
def index():
	return render_template(
        "page.html",
        cat_data=['Hepsi'] + cat_dict.keys(), job_data=['Hepsi'] + job_dict.keys())

@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		inp = [
			result.getlist('gen')[0],
			result.getlist('age')[0],
			result.getlist('edu')[0],
			result.getlist('mar')[0],
			job_dict.get(result.getlist('job')[0]) if job_dict.get(result.getlist('job')[0]) is not None else -1,
			result.getlist('clk')[0],
			cat_dict.get(result.getlist('cat')[0]) if cat_dict.get(result.getlist('cat')[0]) is not None else -1,
		]

		poss = get_possibility(inp)
		return render_template("result.html", value=float(result.getlist('wrs')[0] or 100)*(1 + 10*poss[1]))		


if __name__ == "__main__":
	app.run()