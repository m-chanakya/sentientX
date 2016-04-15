import sys
from myParser import *
from topia.termextract import extract
from nltk.corpus import stopwords
import inflect
sentipath = 'judge/SentiWordNet_3.0.0_20130122.txt'

def split_line(line):
    cols = line.split("\t")
    return cols
 
def get_words(cols):
    words_ids = cols[4].split(" ")
    words = [w.split("#")[0] for w in words_ids]
    return words
 
def get_positive(cols):
    return cols[2]
 
def get_negative(cols):
    return cols[3]
 
def get_objective(cols):
    return 1 - (float(cols[2]) + float(cols[3]))
 
def get_gloss(cols):
    return cols[5]
 
def get_scores(filepath, word):
    temp = [0,0,0]
    count = 0
    f = open(filepath)
    for line in f:
        if not line.startswith("#"):
            cols = split_line(line)
            words = get_words(cols)
            
            if word in words:
                temp[0] += float(format(get_positive(cols)))
                temp[1] += float(format(get_negative(cols)))
                temp[2] += float(format(get_objective(cols)))
                return temp
    if(count > 0):
	    for i in range(len(temp)):
	        temp[i] = temp[i]/count
    return temp


def find_distances(graph,bag_words,aspect):
	neg_list = []
	queue = []
	for i in bag_words:
		if(aspect+'-' in i):
			aspect = i
			break
	queue.append(aspect)
	visited = {}
	dist = {}
	dist[aspect] = 0
	visited[aspect] = 1
	curr_level = 0
	while(len(queue)!=0):
		try:
			a = negation_dict[queue[0]]
			if(queue[0] not in neg_list):
				neg_list.append(queue[0])
				dist[queue[0]] = dist[queue[0]] * -1
			else:
				if(len(a) > 1):
					neg_list.remove(queue[0])
					dist[queue[0]] = dist[queue[0]] * -1
		except:
			abc= 1
		for i in graph[queue[0]]:
			try:
				visited[i]
			except:
				visited[i] = 1
				queue.append(i)
				dist[i] = abs(dist[queue[0]])+1
				try:
					if(queue[0] in neg_list):
						dist[i] *= -1
						neg_list.append(i)
				except:
					abc = 1
		queue = queue[1:]
	return dist

def find_aspect_sentiment(aspect,graph,bag_words):
	aspect_split = aspect.split()
	main_arr = [0,0,0]
	for k in aspect_split:
		final_dist = find_distances(graph,bag_words,k)
		for i in final_dist:
			if(final_dist[i]!=0):
				word = i.split('-')[0]
				temp_arr = get_scores(sentipath,word)
				for j in range(len(temp_arr)):
					temp_arr[j] = temp_arr[j]/4**(abs(final_dist[i])-1)
					if(final_dist[i]<0):
						main_arr[j] -= temp_arr[j]
					else:
						main_arr[j] += temp_arr[j]
	for i in range(len(main_arr)):
		main_arr[i]/=len(aspect_split)
	return main_arr

def judger(review):
	plural_handler = inflect.engine()
	stop = stopwords.words('english')
	stop_dict = {}
	for i in stop:
		stop_dict[str(i)] = 1
	stop_dict = {}
	total_aspects = {}
	for k in review:
		sen = k.lower()
		print k
		result = my_parse(sen)
		store_POS = {}
		st = ''
		for i in range(len(result['words'])):
			store_POS[result['words'][i][0]] = result['words'][i][1]['PartOfSpeech']
			st += result['words'][i][0]+ ' '
		dep_store = []
		negation_dict = {}
		for i in result['indexeddependencies']:
			temp = []
			temp.append(i[1])
			temp.append(i[2])
			if('neg' in i[0]):
				try:
					negation_dict[i[2]].append(i[1])
				except:
					negation_dict[i[2]] = []
					negation_dict[i[2]].append(i[1])
				try:
					negation_dict[i[1]].append(i[2])
				except:
					negation_dict[i[1]] = []
					negation_dict[i[1]].append(i[2])
			if('ROOT-0' not in i):
				dep_store.append(temp)
		
		graph = {}
		for i in dep_store:
			try:
				graph[i[0]].append(i[1])
			except:
				graph[i[0]] = []
				graph[i[0]].append(i[1])
			try:
				graph[i[1]].append(i[0])
			except:
				graph[i[1]] = []
				graph[i[1]].append(i[0])


		bag_words = []
		for i in store_POS:
			bag_words.append(i)

		arr_aspects = []
		extractor = extract.TermExtractor()
		extractor.filter = extract.permissiveFilter
		arr_aspects = extractor(st)
		final_aspects = []
		check_arr = map((lambda x: x.split('-')[0]),bag_words)
		for i in range(len(arr_aspects)):
			temp = ''
			spl = arr_aspects[i][0].split(' ')
			for j in spl:
				if( j in check_arr):
					if(temp!=''):
						temp+=' '
					temp += j
				elif(plural_handler.plural(j) in check_arr):
					if(temp!=''):
						temp += ' '
					temp += plural_handler.plural(j)
			if(len(temp)>0):
				final_aspects.append(temp)
		for i in final_aspects:
			ar = find_aspect_sentiment(str(i),graph,bag_words)
			temp = total_aspects.get(str(i), [0, "Neutral"])
			temp[0] = temp[0]+(ar[0]-ar[1])
			if temp[0] > 0:
				temp[1] = "Positive"
			elif temp[0] < 0:
				temp[1] = "Negative"
			total_aspects[str(i)] = temp
	return total_aspects
