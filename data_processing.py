
import nltk
from nltk.corpus import stopwords

from cleanReviewData import cleanReview
from calculate_probabilities import calculate_prob

import re



from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
import csv




# for laplace smooting and reving zero values
def laplace_add(vocab,count_neg_or_pos):
    return float(1/(vocab+count_neg_or_pos+1))

#method for reprocessing i.e. cleaning of file removing stop words punctuation

def analyzeData(mode):
    #input directory
    review_directory = r'/Users/manishtandon/Documents/SML/movie_review_data'
    #review_directory = r'/Users/manishtandon/Documents/SML/movie'

    movie_train = load_files(review_directory)


    dict_words_complete_list={}
    dict_words_outer={}
    #splitting the file for training the data , was changed from 0.1 to 0.9 for analysing
    size_split=1
    #mode can be either test or train

    X_train, y_train, x_test, y_test = train_test_split(movie_train.data, movie_train.target, test_size = (1-size_split))

    dict_id_target={}
    if mode == 'train':
        with open('file_id_target.csv','a') as csv_file:
            for idx, val in enumerate(X_train):
                str_review=cleanReview(val)


                current_review=str_review
                X_train[idx]=str_review
                word_list_cur_review=current_review.split(' ')

                dict_words={}

                dict_id_target[idx]=x_test[idx]
                for each_word_in_cur_review in word_list_cur_review:
                    if each_word_in_cur_review in dict_words_outer:
                        dict_words_outer[each_word_in_cur_review]=dict_words_outer.get(each_word_in_cur_review)+1;
                    else:
                        dict_words_outer[each_word_in_cur_review]=1
                    if each_word_in_cur_review not in dict_words:
                        dict_words[each_word_in_cur_review]=word_list_cur_review.count(each_word_in_cur_review)

                list_of_tuples=[]
                for key,val in dict_words.items():
                    if key in dict_words_complete_list:

                        dict_words_complete_list.get(key).append((idx,val))

                    else:
                        dict_words_complete_list[key]=[(idx,val)]

        final_matrix_dict={}
        triplet_list1 = []

    if mode=='train':
        with open("file.txt","a") as output_file:

            for key,value in dict_words_outer.items():

                if key not in final_matrix_dict:
                    final_matrix_dict[key]=[0]*len(movie_train.data)
                    tuple_list_for_word=dict_words_complete_list[key]
                    for tuple in tuple_list_for_word:
                        val_tup=tuple[1]
                        val_id=tuple[0]
                        final_matrix_dict[key][tuple[0]] = val_tup
                        if val_tup !=0:

                            output_file.write(str(key) + ' ' + str(val_id) + ' ' + str(val_tup) + '\n')
        with open("file.csv","a") as output_file:

            for key,value in dict_words_outer.items():

                if key not in final_matrix_dict:
                    final_matrix_dict[key]=[0]*len(movie_train.data)
                    tuple_list_for_word=dict_words_complete_list[key]
                    for tuple in tuple_list_for_word:
                        val_tup=tuple[1]
                        val_id=tuple[0]
                        final_matrix_dict[key][tuple[0]] = val_tup
                        if val_tup !=0:

                            output_file.write(str(key) + ',' + str(dict_id_target[val_id]) + ',' + str(val_tup) + '\n')




        calculate_prob()
    #for test mode we will calculate each probabilty using naive baiyes
    if mode =='test':
        final_accuracy_dict={}
        correct=0
        lookup_prob={}
        total_neg_count=1
        total_pos_count=1
        #based on data analysis
        vocab=78000
        with open('file_count_neg_pos.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                total_neg_count = int(row[0])
                total_pos_count=int(row[1])

        with open('file_prob.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                word = row[0]
                neg_prob=float(row[1])
                pos_prob=float(row[2])

                lookup_prob[word]=[neg_prob,pos_prob]


        for id,val in enumerate(movie_train.data):
            cleaned_review=cleanReview(val)
            word_list_cur_review = cleaned_review.split(' ')
            review_neg_probability=float((14363/(14363+14016)))
            review_pos_probability=float(14016/(14363+14016))
            for each_word_in_cur_review in word_list_cur_review:
                negative=float(1)
                positive=float(1)
                if each_word_in_cur_review in lookup_prob:
                    negative=float(lookup_prob[each_word_in_cur_review][0])
                    positive=float(lookup_prob[each_word_in_cur_review][1])
                    if negative==0:
                        negative=laplace_add(vocab,total_neg_count)
                    if positive==0:
                        positive=laplace_add(vocab,total_pos_count)
                else:
                    negative = laplace_add(vocab, total_neg_count)
                    positive = laplace_add(vocab, total_neg_count)
                review_neg_probability=review_neg_probability*negative
                review_pos_probability=review_pos_probability*positive

            if review_neg_probability>review_pos_probability and movie_train.target[id]==0 :
                correct +=1

            if review_neg_probability<review_pos_probability and movie_train.target[id]==1 :
                correct +=1


        print(correct/len(movie_train.data))


