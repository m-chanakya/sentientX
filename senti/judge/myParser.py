from nltk.parse.stanford import StanfordDependencyParser
import os

path_to_jar = os.path.abspath('../libs/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar')
path_to_models_jar = os.path.abspath('../libs/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0-models.jar')
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

def my_parse(sent):
	result = dependency_parser.raw_parse(sent)
	dep = result.next()

	words = []
	for each in dep.nodes:
		if each != 0:
			temp = [dep.nodes[each]['word']+"-"+str(each), {'PartOfSpeech': dep.nodes[each]['ctag']}]
			words.append(temp)

	ans = []
	for each in dep.nodes:
		if each != 0:
			word = dep.nodes[each]['word']
		else:
			word = "ROOT"
		for d in dep.nodes[each]['deps']:
			for adr in dep.nodes[each]['deps'][d]:
				ans.append([d, word+"-"+str(each), dep.get_by_address(adr)['word']+"-"+str(adr) ])

	return {'words': words, 'indexeddependencies': ans}