import random
import os
import copy
import csv
import pprint
data_dir = "../../"
punc = ".,~!@#$%^&*()！@#￥%……&*（——）。，+-*/=;"
def construct_train_data_corpus_vocabulary_dictionary(begin,end):
	corpus_file_name = "train_data.txt"
	riddle_voc = dict()
	ans_voc = dict()
	riddle_cnt = 0
	ans_cnt = 0
	line_cnt = begin
	with open(os.path.join(data_dir,corpus_file_name),'r',encoding='UTF-8') as f:
		f.readline()
		for line in f:
			if line_cnt >= end:
				break
			line = line[:-1]
			record = line.split('\t',2)[1:3]
			riddle = record[0]
			ans = record[1]
			for word in riddle:
				if word in punc:
					continue
				if word not in riddle_voc:
					riddle_voc[word] = riddle_cnt
					riddle_cnt += 1
			for word in ans:
				if word in punc:
					continue
				if word not in ans_voc:
					ans_voc[word] = ans_cnt
					ans_cnt += 1
			line_cnt += 1
	return riddle_voc, ans_voc

def read_dataset():
	dataset_file = "train_data.txt"
	ret = list()
	try:
		with open(os.path.join(data_dir,dataset_file),'r',encoding='UTF-8') as f:
			f.readline()
			for line in f:
				if(line[-1] == '\n'):
					line = line[:-1]
				record = line.split('\t',2)[1:3]
				a = [0,1]
				record.append(a)
				ret.append(record)
	except FileNotFoundError:
		print("file name error, file not exist")
		exit(0)
	return ret

if __name__ == "__main__":
	ret = read_dataset()
	# print(ret[0:10])