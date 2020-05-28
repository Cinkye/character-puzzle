import read_data
import random

class Data:
    def __init__(self):
        """
            for train and test data, dataset is in form like [[谜面，答案，地信],]
            for valid data, dataset is [[谜面，谜底，选项],]

            variables begin with `raw` are prepared for calculating valid data.
        """
        # make train, valid, test
        self.n_for_1 = 2
        raw_riddles = read_data.read_dataset() #[[谜面，谜底，选项],]
        random.shuffle(raw_riddles)
        riddles = self.construct_classify_riddle_set(raw_riddles) #[[谜面，答案，地信],]
        one_tenth = len(riddles) // 10
        raw_one_tenth = len(raw_riddles) // 10
        train = riddles[0:one_tenth * 8]
        test = riddles[one_tenth * 8 : one_tenth * 9]
        valid = raw_riddles[raw_one_tenth * 9 : raw_one_tenth * 10]

        # get voc
        self.riddle_voc,self.ans_voc = read_data.construct_train_data_corpus_vocabulary_dictionary(begin = 0, end = one_tenth * 8)
        self.riddle_voc_size = len(self.riddle_voc) + 1 # two more place, one for padding, one for unseen
        self.ans_voc_size = len(self.ans_voc) + 1
        UNSEEN_riddle = self.riddle_voc_size + 1
        UNSEEN_ans = self.ans_voc_size + 1

        #indexize
        def indexizer(riddle,is_valid = False):
            ret = list()
            ret.append( [self.riddle_voc[word] if word in self.riddle_voc else UNSEEN_riddle for word in riddle[0] ] )
            ret.append( self.ans_voc[riddle[1]] if riddle[1] in self.ans_voc else UNSEEN_ans )
            if is_valid:
                ret.append([self.ans_voc[word] if word in self.ans_voc else UNSEEN_ans for word in riddle[2] ])
            else:
                ret.append( riddle[2] )
            #print(ret)
            return ret
        self.train = [indexizer(row) for row in train]
        self.valid = [indexizer(row,is_valid= True) for row in valid]
        self.test = [indexizer(row) for row in test]

        # print(self.train, self.valid, self.test)
        # exit()
        
    def construct_classify_riddle_set(self,riddles):
        #
        # @input:  [[谜面，谜底，选项],]
        # @output: [[谜面，答案，地信],]
        #
        ret = list()
        for riddle in riddles:
            # for opt in riddle[2]:
            #     #item = list()
            #     #item.append(riddle[0]) #谜面
            #     #item.append(opt) #答案
            #     #item.append(opt == riddle[1]) #地信
            #     ret.append([riddle[0],opt,int(opt == riddle[1])])
            if random.random() < 0.5:
                ret.append([riddle[0],riddle[1],1])
            else:
                ret.append([riddle[0],'1' if riddle[1] == '0' else '0', 0])
        return ret

    def get_voc_dict(self):
        return self.riddle_voc
    def get_voc_size(self):
        return self.riddle_voc_size

    #
    #   @ret: [ riddle, answer, answer with options ], dataset size
    #
    def get_train_data(self):
        random.shuffle(self.train)
        return [ [riddle[i] for riddle in self.train] for i in range(3) ],len(self.train)

    def get_valid_data(self):
        return [ [riddle[i] for riddle in self.valid] for i in range(3) ],len(self.valid)

    def get_test_data(self):
        return [ [riddle[i] for riddle in self.test] for i in range(3) ],len(self.test)