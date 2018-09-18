
import csv
import pandas as pd

#helper function that calculates and saves the probability of each word
def calculate_prob():
    dict_word = {}
    count_total_neg=0
    count_total_pos=0
    with open('file.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            word=row[0]
            target=int(row[1])
            count=int(row[2])
            if word in dict_word:
                if target==0:
                    val_0=dict_word[word][0]
                    dict_word[word][0]=val_0+count
                    count_total_neg=count_total_neg+count
                else:
                    val_1 = dict_word[word][1]
                    dict_word[word][1] = val_1 + count
                    count_total_pos = count_total_neg + count
            else:
                if target==0:
                    dict_word[word]=[count,0]
                    count_total_neg = count_total_neg + count
                else:
                    dict_word[word] = [0, count]
                    count_total_pos = count_total_neg + count


    save_probability(dict_word,count_total_neg,count_total_pos)

#save probability to file for lookup during testing
def save_probability(dict_word,count_total_neg,count_total_pos):
    with open('file_prob.csv','w') as csv_file:
        for id,val in dict_word.items():
            prob_neg=float((dict_word[id][0])/count_total_neg)
            prob_pos=float((dict_word[id][1])/count_total_pos)
            csv_file.write(id+','+str(prob_neg)+','+str(prob_pos)+'\n')
    with open('file_count_neg_pos.csv','w') as csv_file:
        csv_file.write(str(count_total_neg)+','+str(count_total_pos)+'\n')

