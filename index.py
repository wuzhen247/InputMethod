from __future__ import (print_function, unicode_literals)

from flask import Flask, jsonify, render_template, request

from IME import DefaultDagParams
from IME import dag
from IME import dict_tree
from IME import DefaultHmmParams
from IME import viterbi

dagparams = DefaultDagParams()
#hmmparams = DefaultHmmParams()
tree = dict_tree.DictTree()

app = Flask(__name__)

@app.route('/hello/', methods=['GET', 'POST'])
def hello():
	pinyin = request.args.get('pinyin')
	print(pinyin)
	result = dag(dagparams, ['wo', 'men'], path_num=2, log=True)
	re = {
		"score": result[0].score,
		"sentence": ''.join(result[0].path)
	}
	return jsonify(re)

@app.route('/inputmethod')
def inputmethod():
	pinyin = request.args.get('pinyin')
	result = dag(dagparams, tree.split_pinyin(pinyin.strip()), path_num=10, log=True)
	#result = viterbi(hmm_params=hmmparams, observations=tree.split_pinyin(pinyin.strip()), path_num = 1, log = True)
	resultjson= []
	for i in range(len(result)):
		resultjson.append({"score": result[i].score,
		"sentence": ''.join(result[i].path)})

	return jsonify(result=resultjson)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)