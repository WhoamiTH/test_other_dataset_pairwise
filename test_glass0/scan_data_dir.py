import glob
import re
import sys
import numpy as np
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
import csv
import copy

class datarecord:
    def __init__(self, name):
        self.aauc = {}
        self.af = {}
        self.ap = {}
        self.ar = {}
        self.aea = {}
        self.aa = {}
        self.aer = {}
        self.name = name
        self.current_file_number = -1

    def getNum(self, file_name):
        firstChar = file_name[-5]
        secondChar = file_name[-6]
        num = firstChar
        if secondChar.isdigit():
            num = secondChar + num
        self.current_file_number = int(num)

    def record_diff_result(self, targetDic, index, result):
        if index in targetDic:
            targetDic[index].append(result)
        else:
            targetDic[index] = [result]

    def check_category(self, current_str, target_str, target_dic):
        if (current_str.find(target_str) != -1):
            i = current_str.replace(target_str, '')
            target_number = float(i)
            self.record_diff_result(target_dic, self.current_file_number, target_number)
   
    def read_file(self, file_name):
        self.getNum(file_name)
        f = open(file_name,'r')
        auc_str = 'the AUC is '
        f_score_str = 'the Fscore is '
        pre_str = 'the average group top precision is '
        recall_str = 'the average group recall is '
        exact_accu_str = 'the average group top exact accuracy is '
        group_accu_str = 'the average group accuracy is '
        er_str = 'the earn rate is '

        for i in f:
            self.check_category(i, auc_str, self.aauc)
            self.check_category(i, f_score_str, self.af)
            self.check_category(i, pre_str, self.ap)
            self.check_category(i, recall_str, self.ar)
            self.check_category(i, exact_accu_str, self.aea)
            self.check_category(i, group_accu_str, self.aa)
            self.check_category(i, er_str, self.aer)


    def calculate_average(self):
        self.average_af = self.calculate_average_value(self.af)

    def calculate_average_value(self, target_dic):
        key_list = []
        result_list = []
        length = len(target_dic)
        # print(target_dic)
        for key in target_dic:
            key_list.append(key)
        key_list.sort()
        for key in key_list:
            result_list.append(target_dic[key])
        key = key_list[0]
        number_of_test = len(target_dic[key])
        divide_result = np.array(result_list)
        self.af = divide_result
        # calculate the sum result of each rows
        sum_result = np.sum(divide_result, axis=1)
        sum_result /= number_of_test
        return sum_result

    def get_max(self):
        print(self.name, np.where(self.average_af==self.average_af.max()), self.average_af.max())

    def plotimage(self):
        # draw picture
        length = self.af.shape[0]
        x = [i for i in range(1, length+1)]
        # print(self.average_af)
        # print(self.af)
        plt.figure()

        # plt.scatter(x, self.af, s=10, c='r', marker='x')
        plt.plot(x, self.af[:,0], label='first', color='b')
        plt.plot(x, self.af[:,1], label='second', color='cyan')
        plt.plot(x, self.af[:,2], label='third', color='yellow')
        plt.plot(x, self.af[:,3], label='fourth', color='g')

        # self.af = self.af.reshape(-1,1)
        # number_of_result = self.af.shape[0]
        # sum_result = np.sum(self.af, axis=0)
        # sum_result /= number_of_result
        # # print(sum_result)
        # average_af = [sum_result for i in range(1, length+1)]

        plt.plot(x, self.average_af, label='average_F', c='r')

        plt.xlabel('test week')
        plt.ylabel('Fscore')
        plt.legend(loc='upper left')
        plt.savefig(self.name + '.pdf')




class different_percent_datarecord(datarecord):
    def __init__(self, name, path, total_record_number):
        datarecord.__init__(self, name)
        self.path = path
        self.total_record_number = total_record_number

    def read_file_list(self):
        for record_number in range(1, total_record_number+1):
            record_path = path + self.name + '/record_{0}/*.txt'.format(record_number)
            print(record_path)
            file_list = glob.glob(record_path)
            file_list.sort()
            for file_name in file_list:
                if file_name.find(self.name) != -1:
                    print(file_name)
                    self.read_file(file_name)

    def calculate_average(self):
        print(self.name)
        self.print_average()
        print(self.af)
        self.row_average_value_af, self.total_average_value_af, self.af = self.calculate_average_value(self.af)
        # print('average_af is {0}'.format(self.average_af))
        self.row_average_value_ap, self.total_average_value_ap, self.ap = self.calculate_average_value(self.ap)
        # print('average_ap is {0}'.format(self.average_ap))
        self.row_average_value_ar, self.total_average_value_ar, self.ar = self.calculate_average_value(self.ar)
        # print('average_ar is {0}'.format(self.average_ar))
        self.row_average_value_aauc, self.total_average_value_aauc, self.aauc = self.calculate_average_value(self.aauc)
        # print('average_aauc is {0}'.format(self.average_aauc))
        # self.af = self.calculate_average_af(self.af)

    def calculate_average_af(self, target_dic):
        key_list = []
        result_list = []
        length = len(target_dic)
        # print(target_dic)
        for key in target_dic:
            key_list.append(key)
        # print(key_list)
        key_list.sort()
        for key in key_list:
            result_list.append(target_dic[key])
        # print(key_list)
        key = key_list[0]
        number_of_test = len(target_dic[key])
        divide_result = np.array(result_list)
        return divide_result

    def calculate_average_value(self, target_dic):
        key_list = []
        result_list = []
        length = len(target_dic)
        print(length)
        # print(target_dic)
        for key in target_dic:
            key_list.append(key)
        # print(key_list)
        key_list.sort()
        for key in key_list:
            result_list.append(target_dic[key])
        # print(key_list)
        key = key_list[0]
        number_of_item_test = len(target_dic[key])
        print(number_of_item_test)
        total_test = number_of_item_test * length
        divide_result = np.array(result_list)
        # self.af = divide_result
        # calculate the sum result of each rows
        rowsum_result = np.sum(divide_result, axis=1)
        row_average_value = rowsum_result/number_of_item_test
        total_sum = np.sum(rowsum_result, axis=0)
        total_average_value = total_sum/total_test
        return row_average_value, total_average_value, divide_result

    def print_average(self):
        print(self.name)
        print_average_aauc = self.calculate_print_average_value(self.aauc)
        print('average_aauc is {0}'.format(print_average_aauc))
        print_average_af = self.calculate_print_average_value(self.af)
        print('average_af is {0}'.format(print_average_af))
        print_average_ap = self.calculate_print_average_value(self.ap)
        print('average_ap is {0}'.format(print_average_ap))
        print_average_ar = self.calculate_print_average_value(self.ar)
        print('average_ar is {0}'.format(print_average_ar))
        

    def calculate_print_average_value(self, target_dic):
        key_list = []
        result_list = []
        length = len(target_dic)
        # print(target_dic)
        for key in target_dic:
            key_list.append(key)
        # print(key_list)
        key_list.sort()
        for key in key_list:
            result_list.append(target_dic[key])
        # print(key_list)
        # key = key_list[0]
        number_of_test = len(key_list)
        number_of_test *= length
        divide_result = np.array(result_list)
        # calculate the sum result of each rows
        # sum_result = np.sum(divide_result, axis=1)
        # calculate the sum result of each columns
        # print(divide_result)
        sum_result = np.sum(divide_result, axis=0)
        sum_result = np.sum(sum_result, axis=0)
        # print(sum_result)
        # print(number_of_test)
        sum_result /= number_of_test
        # print(sum_result)
        return sum_result

    def calculate_average_line(self):
        number_of_test = self.average_af.shape[0]
        local_average_af = copy.deepcopy(self.average_af)
        sum_result = np.sum(self.average_af, axis=0)
        sum_result /= number_of_test
        self.average_line = sum_result

    def plotimage(self):
        # draw picture
        length = self.af.shape[0]
        num_of_test = self.af.shape[1]
        x = [i for i in range(1, length+1)]
        average_line = [self.total_average_value_af for i in range(1,length+1)]

        fig, (ax1, ax2) = plt.subplots(1,2)
        if num_of_test > 0:
            ax1.plot(x, self.af[:,0], label='first', color='b')
        if num_of_test > 1:
            ax1.plot(x, self.af[:,1], label='second', color='cyan')
        if num_of_test > 2:
            ax1.plot(x, self.af[:,2], label='third', color='yellow')
        if num_of_test > 3:
            ax1.plot(x, self.af[:,3], label='fourth', color='g')
        ax1.set_title('divided result')

        ax2.plot(x, self.row_average_value_af, label='average_F', c='r')
        ax2.plot(x, average_line, label='average_line', c='purple')
        ax2.set_title('average result')

        ax1.set_xlabel('test fold')
        ax1.set_ylabel('Fscore')

        ax2.set_xlabel('test fold')
        ax2.set_ylabel('Fscore')
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper left')
        plt.savefig(self.name + '.pdf')



def set_para():
    global path
    global result_number
    global winner_number
    global record_file_name
    global result_dir_number

    argv = sys.argv[1:]
    for each in argv:
        para = each.split('=')
        if para[0] == 'path':
            path = para[1]
        if para[0] == 'result_number':
            result_number = int(para[1])
        if para[0] == 'winner_number':
            winner_number = int(para[1])
        if para[0] == 'record_file_name':
            record_file_name = para[1]
        if para[0] == 'result_dir_number':
            result_dir_number = int(para[1])







# -------------------------------------global parameters---------------------------------
result_number = 3
winner_number = 3
path = './1_year_result/'
result_dir_number = 1
record_file_name = 'result_' + str(result_number) + '_' + str(winner_number) + '.pdf'
total_record_number = 1
pairwise_vote_name = 'pairwise_vote'
# record_file_name = 'result_8_3.pdf'

# ----------------------------------set parameters--------------------------------------
set_para()

# ----------------------------------start processing---------------------------------


pairwise_vote_name = 'pairwise_vote'


# ijcai_bm_bm_name        = 'ijcai_bm_bm'
# ijcai_bm_both_name      = 'ijcai_bm_both'
# ijcai_bm_im_name        = 'ijcai_bm_im'
# ijcai_bm_normal_name    = 'ijcai_bm_normal'

# ijcai_both_bm_name      = 'ijcai_both_bm'
# ijcai_both_both_name    = 'ijcai_both_both'
# ijcai_both_im_name      = 'ijcai_both_im'
# ijcai_both_normal_name  = 'ijcai_both_normal'

# ijcai_im_bm_name      = 'ijcai_im_bm'
# ijcai_im_both_name    = 'ijcai_im_both'
# ijcai_im_im_name      = 'ijcai_im_im'
# ijcai_im_normal_name  = 'ijcai_im_normal'

# ijcai_normal_bm_name      = 'ijcai_normal_bm'
# ijcai_normal_both_name    = 'ijcai_normal_both'
# ijcai_normal_im_name      = 'ijcai_normal_im'
# ijcai_normal_normal_name  = 'ijcai_normal_normal'


pairwise_vote_record      = different_percent_datarecord(pairwise_vote_name, path, total_record_number)
# ijcai_bm_bm_record      = different_percent_datarecord(ijcai_bm_bm_name, path, total_record_number)
# ijcai_bm_both_record    = different_percent_datarecord(ijcai_bm_both_name, path, total_record_number)
# ijcai_bm_im_record      = different_percent_datarecord(ijcai_bm_im_name, path, total_record_number)
# ijcai_bm_normal_record  = different_percent_datarecord(ijcai_bm_normal_name, path, total_record_number)

# ijcai_both_bm_record      = different_percent_datarecord(ijcai_both_bm_name, path, total_record_number)
# ijcai_both_both_record    = different_percent_datarecord(ijcai_both_both_name, path, total_record_number)
# ijcai_both_im_record      = different_percent_datarecord(ijcai_both_im_name, path, total_record_number)
# ijcai_both_normal_record  = different_percent_datarecord(ijcai_both_normal_name, path, total_record_number)

# ijcai_im_bm_record      = different_percent_datarecord(ijcai_im_bm_name, path, total_record_number)
# ijcai_im_both_record    = different_percent_datarecord(ijcai_im_both_name, path, total_record_number)
# ijcai_im_im_record      = different_percent_datarecord(ijcai_im_im_name, path, total_record_number)
# ijcai_im_normal_record  = different_percent_datarecord(ijcai_im_normal_name, path, total_record_number)

# ijcai_normal_bm_record      = different_percent_datarecord(ijcai_normal_bm_name, path, total_record_number)
# ijcai_normal_both_record    = different_percent_datarecord(ijcai_normal_both_name, path, total_record_number)
# ijcai_normal_im_record      = different_percent_datarecord(ijcai_normal_im_name, path, total_record_number)
# ijcai_normal_normal_record  = different_percent_datarecord(ijcai_normal_normal_name, path, total_record_number)



# for record_number in range(1, total_record_number+1):
#     record_path = path + 'record_{0}/*.txt'.format(record_number)
#     print(record_path)
#     file_list = glob.glob(record_path)
#     file_list.sort()
#     for file_name in file_list:
#         print(file_name)
#         if file_name.find(ijcai_bm_bm_name) != -1:
#             ijcai_bm_bm_record.read_file(file_name)
#         if file_name.find(ijcai_bm_both_name) != -1:
#             ijcai_bm_both_record.read_file(file_name)
#         if file_name.find(ijcai_bm_im_name) != -1:
#             ijcai_bm_im_record.read_file(file_name)
#         if file_name.find(ijcai_bm_normal_name) != -1:
#             ijcai_bm_normal_record.read_file(file_name)

#         if file_name.find(ijcai_both_bm_name) != -1:
#             ijcai_both_bm_record.read_file(file_name)
#         if file_name.find(ijcai_both_both_name) != -1:
#             ijcai_both_both_record.read_file(file_name)
#         if file_name.find(ijcai_both_im_name) != -1:
#             ijcai_both_im_record.read_file(file_name)
#         if file_name.find(ijcai_both_normal_name) != -1:
#             ijcai_both_normal_record.read_file(file_name)

#         if file_name.find(ijcai_im_bm_name) != -1:
#             ijcai_im_bm_record.read_file(file_name)
#         if file_name.find(ijcai_im_both_name) != -1:
#             ijcai_im_both_record.read_file(file_name)
#         if file_name.find(ijcai_im_im_name) != -1:
#             ijcai_im_im_record.read_file(file_name)
#         if file_name.find(ijcai_im_normal_name) != -1:
#             ijcai_im_normal_record.read_file(file_name)

#         if file_name.find(ijcai_normal_bm_name) != -1:
#             ijcai_normal_bm_record.read_file(file_name)
#         if file_name.find(ijcai_normal_both_name) != -1:
#             ijcai_normal_both_record.read_file(file_name)
#         if file_name.find(ijcai_normal_im_name) != -1:
#             ijcai_normal_im_record.read_file(file_name)
#         if file_name.find(ijcai_normal_normal_name) != -1:
#             ijcai_normal_normal_record.read_file(file_name)


pairwise_vote_record.read_file_list()

# ijcai_normal_normal_record.read_file_list()
# ijcai_normal_bm_record.read_file_list()
# ijcai_normal_im_record.read_file_list()
# ijcai_normal_both_record.read_file_list()



# ijcai_bm_normal_record.read_file_list()
# ijcai_bm_bm_record.read_file_list()
# ijcai_bm_im_record.read_file_list()
# ijcai_bm_both_record.read_file_list()

# ijcai_im_normal_record.read_file_list()
# ijcai_im_bm_record.read_file_list()
# ijcai_im_im_record.read_file_list()
# ijcai_im_both_record.read_file_list()



# ijcai_both_normal_record.read_file_list()
# ijcai_both_bm_record.read_file_list()
# ijcai_both_im_record.read_file_list()
# ijcai_both_both_record.read_file_list()





pairwise_vote_record.calculate_average()
# ijcai_normal_normal_record.calculate_average()
# ijcai_normal_bm_record.calculate_average()
# ijcai_normal_im_record.calculate_average()
# ijcai_normal_both_record.calculate_average()



# ijcai_bm_normal_record.calculate_average()
# ijcai_bm_bm_record.calculate_average()
# ijcai_bm_im_record.calculate_average()
# ijcai_bm_both_record.calculate_average()

# ijcai_im_normal_record.calculate_average()
# ijcai_im_bm_record.calculate_average()
# ijcai_im_im_record.calculate_average()
# ijcai_im_both_record.calculate_average()



# ijcai_both_normal_record.calculate_average()
# ijcai_both_bm_record.calculate_average()
# ijcai_both_im_record.calculate_average()
# ijcai_both_both_record.calculate_average()










# ijcai_bm_bm_record.calculate_average_line()
# ijcai_bm_both_record.calculate_average_line()
# ijcai_bm_im_record.calculate_average_line()
# ijcai_bm_normal_record.calculate_average_line()

# ijcai_both_bm_record.calculate_average_line()
# ijcai_both_both_record.calculate_average_line()
# ijcai_both_im_record.calculate_average_line()
# ijcai_both_normal_record.calculate_average_line()

# ijcai_im_bm_record.calculate_average_line()
# ijcai_im_both_record.calculate_average_line()
# ijcai_im_im_record.calculate_average_line()
# ijcai_im_normal_record.calculate_average_line()

# ijcai_normal_bm_record.calculate_average_line()
# ijcai_normal_both_record.calculate_average_line()
# ijcai_normal_im_record.calculate_average_line()
# ijcai_normal_normal_record.calculate_average_line()





# ijcai_bm_bm_record.get_max()
# ijcai_bm_both_record.get_max()
# ijcai_bm_im_record.get_max()
# ijcai_bm_normal_record.get_max()

# ijcai_both_bm_record.get_max()
# ijcai_both_both_record.get_max()
# ijcai_both_im_record.get_max()
# ijcai_both_normal_record.get_max()

# ijcai_im_bm_record.get_max()
# ijcai_im_both_record.get_max()
# ijcai_im_im_record.get_max()
# ijcai_im_normal_record.get_max()

# ijcai_normal_bm_record.get_max()
# ijcai_normal_both_record.get_max()
# ijcai_normal_im_record.get_max()
# ijcai_normal_normal_record.get_max()


pairwise_vote_record.plotimage()

record = open('result_only.txt','w')
record.write(str(pairwise_vote_record.total_average_value_aauc)+'\n')
record.write(str(pairwise_vote_record.total_average_value_af)+'\n')
record.write(str(pairwise_vote_record.total_average_value_ap)+'\n')
record.write(str(pairwise_vote_record.total_average_value_ar)+'\n')
record.close()


# ijcai_bm_bm_record.plotimage()
# ijcai_bm_both_record.plotimage()
# ijcai_bm_im_record.plotimage()
# ijcai_bm_normal_record.plotimage()

# ijcai_both_bm_record.plotimage()
# ijcai_both_both_record.plotimage()
# ijcai_both_im_record.plotimage()
# ijcai_both_normal_record.plotimage()

# ijcai_im_bm_record.plotimage()
# ijcai_im_both_record.plotimage()
# ijcai_im_im_record.plotimage()
# ijcai_im_normal_record.plotimage()

# ijcai_normal_bm_record.plotimage()
# ijcai_normal_both_record.plotimage()
# ijcai_normal_im_record.plotimage()
# ijcai_normal_normal_record.plotimage()

# table_1 = '\\begin{table}[H]\n'
# table_1 += '\\centering\n'
# table_1 += '\\caption{the performance of different varienties of ijcai method}\n'
# table_1 += '\\label{tab:ChangingTrainData33}\n'
# table_1 += '\\begin{tabular}{|p{0.1\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|}\n'
# table_1 += '\\hline \multirow{2}{*}{Method} & \multicolumn{4}{|c|}{Original test} & \multicolumn{4}{|c|}{Border Majority} & \multicolumn{4}{|c|}{Informative Minority} & \multicolumn{4}{|c|}{Both of them}\\\\\n'
# table_1 += '\\cline{2-17} & Auc & F1 & Pre & Recall & Auc & F1 & Pre & Recall & Auc & F1 & Pre & Recall & Auc & F1 & Pre & Recall \\\\\n'
# table_1 += '\\hline IJCAI & {0:.3f} & {1:.3f} & {2:.3f}  &  {3:.3f} & {4:.3f} & {5:.3f} & {6:.3f} & {7:.3f} & {8:.3f} &  {9:.3f} & {10:.3f} &  {11:.3f}  & {12:.3f} & {13:.3f} & {14:.3f} & {15:.3f} \\\\\n'.format(ijcai_normal_normal_record.total_average_value_aauc, ijcai_normal_normal_record.total_average_value_af, ijcai_normal_normal_record.total_average_value_ap, ijcai_normal_normal_record.total_average_value_ar, ijcai_normal_bm_record.total_average_value_aauc, ijcai_normal_bm_record.total_average_value_af, ijcai_normal_bm_record.total_average_value_ap, ijcai_normal_bm_record.total_average_value_ar, ijcai_normal_im_record.total_average_value_aauc, ijcai_normal_im_record.total_average_value_af, ijcai_normal_im_record.total_average_value_ap, ijcai_normal_im_record.total_average_value_ar, ijcai_normal_both_record.total_average_value_aauc, ijcai_normal_both_record.total_average_value_af, ijcai_normal_both_record.total_average_value_ap, ijcai_normal_both_record.total_average_value_ar)
# table_1 += '\\hline Training with BM & {0:.3f} & {1:.3f} & {2:.3f}  &  {3:.3f} & {4:.3f} & {5:.3f} & {6:.3f} & {7:.3f} & {8:.3f} &  {9:.3f} & {10:.3f} &  {11:.3f}  & {12:.3f} & {13:.3f} & {14:.3f} & {15:.3f} \\\\\n'.format(ijcai_bm_normal_record.total_average_value_aauc, ijcai_bm_normal_record.total_average_value_af, ijcai_bm_normal_record.total_average_value_ap, ijcai_bm_normal_record.total_average_value_ar, ijcai_bm_bm_record.total_average_value_aauc, ijcai_bm_bm_record.total_average_value_af, ijcai_bm_bm_record.total_average_value_ap, ijcai_bm_bm_record.total_average_value_ar, ijcai_bm_im_record.total_average_value_aauc, ijcai_bm_im_record.total_average_value_af, ijcai_bm_im_record.total_average_value_ap, ijcai_bm_im_record.total_average_value_ar, ijcai_bm_both_record.total_average_value_aauc, ijcai_bm_both_record.total_average_value_af, ijcai_bm_both_record.total_average_value_ap, ijcai_bm_both_record.total_average_value_ar)
# table_1 += '\\hline Training with IM & {0:.3f} & {1:.3f} & {2:.3f}  &  {3:.3f} & {4:.3f} & {5:.3f} & {6:.3f} & {7:.3f} & {8:.3f} &  {9:.3f} & {10:.3f} &  {11:.3f}  & {12:.3f} & {13:.3f} & {14:.3f} & {15:.3f} \\\\\n'.format(ijcai_im_normal_record.total_average_value_aauc, ijcai_im_normal_record.total_average_value_af, ijcai_im_normal_record.total_average_value_ap, ijcai_im_normal_record.total_average_value_ar, ijcai_im_bm_record.total_average_value_aauc, ijcai_im_bm_record.total_average_value_af, ijcai_im_bm_record.total_average_value_ap, ijcai_im_bm_record.total_average_value_ar, ijcai_im_im_record.total_average_value_aauc, ijcai_im_im_record.total_average_value_af, ijcai_im_im_record.total_average_value_ap, ijcai_im_im_record.total_average_value_ar, ijcai_im_both_record.total_average_value_aauc, ijcai_im_both_record.total_average_value_af, ijcai_im_both_record.total_average_value_ap, ijcai_im_both_record.total_average_value_ar)
# table_1 += '\\hline Training wiht BM and IM & {0:.3f} & {1:.3f} & {2:.3f}  &  {3:.3f} & {4:.3f} & {5:.3f} & {6:.3f} & {7:.3f} & {8:.3f} &  {9:.3f} & {10:.3f} &  {11:.3f}  & {12:.3f} & {13:.3f} & {14:.3f} & {15:.3f} \\\\\n'.format(ijcai_both_normal_record.total_average_value_aauc, ijcai_both_normal_record.total_average_value_af, ijcai_both_normal_record.total_average_value_ap, ijcai_both_normal_record.total_average_value_ar, ijcai_both_bm_record.total_average_value_aauc, ijcai_both_bm_record.total_average_value_af, ijcai_both_bm_record.total_average_value_ap, ijcai_both_bm_record.total_average_value_ar, ijcai_both_im_record.total_average_value_aauc, ijcai_both_im_record.total_average_value_af, ijcai_both_im_record.total_average_value_ap, ijcai_both_im_record.total_average_value_ar, ijcai_both_both_record.total_average_value_aauc, ijcai_both_both_record.total_average_value_af, ijcai_both_both_record.total_average_value_ap, ijcai_both_both_record.total_average_value_ar)
# table_1 += '\\hline\n'

# table_1 += '\\end{tabular}\n'
# table_1 += '\\end{table}\n'




# table_2 = '\\begin{table}[H]\n'
# table_2 += '\\centering\n'
# table_2 += '\\caption{the performance of different varienties of ijcai method (AUC and F1}\n'
# table_2 += '\\label{tab:ChangingTrainData33}\n'
# table_2 += '\\begin{tabular}{|p{0.1\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|p{0.05\\textwidth}|}\n'
# table_2 += '\\hline \multirow{2}{*}{Method} & \multicolumn{2}{|c|}{Original test} & \multicolumn{2}{|c|}{Border Majority} & \multicolumn{2}{|c|}{Informative Minority} & \multicolumn{2}{|c|}{Both of them}\\\\\n'
# table_2 += '\\cline{2-9} & Auc & F1  & Auc & F1 & Auc & F1 & Auc & F1  \\\\\n'
# table_2 += '\\hline IJCAI & {0:.3f} & {1:.3f}  & {2:.3f} & {3:.3f} & {4:.3f} &  {5:.3f}  & {6:.3f} & {7:.3f} \\\\\n'.format(ijcai_normal_normal_record.total_average_value_aauc, ijcai_normal_normal_record.total_average_value_af, ijcai_normal_bm_record.total_average_value_aauc, ijcai_normal_bm_record.total_average_value_af, ijcai_normal_im_record.total_average_value_aauc, ijcai_normal_im_record.total_average_value_af, ijcai_normal_both_record
#     .total_average_value_aauc, ijcai_normal_both_record
# .total_average_value_af)
# table_2 += '\\hline Training with BM & {0:.3f} & {1:.3f}  & {2:.3f} & {3:.3f} & {4:.3f} &  {5:.3f}  & {6:.3f} & {7:.3f} \\\\\n'.format(ijcai_bm_normal_record.total_average_value_aauc, ijcai_bm_normal_record.total_average_value_af, ijcai_bm_bm_record.total_average_value_aauc, ijcai_bm_bm_record.total_average_value_af, ijcai_bm_im_record.total_average_value_aauc,ijcai_bm_im_record.total_average_value_af, ijcai_bm_both_record.total_average_value_aauc, ijcai_bm_both_record.total_average_value_af)
# table_2 += '\\hline Training with IM & {0:.3f} & {1:.3f}  & {2:.3f} & {3:.3f} & {4:.3f} &  {5:.3f}  & {6:.3f} & {7:.3f} \\\\\n'.format(ijcai_im_normal_record.total_average_value_aauc, ijcai_im_normal_record.total_average_value_af, ijcai_bm_bm_record.total_average_value_aauc, ijcai_bm_bm_record.total_average_value_af, ijcai_im_im_record.total_average_value_aauc, ijcai_im_im_record.total_average_value_af, ijcai_im_both_record.total_average_value_aauc, ijcai_im_both_record.total_average_value_af)
# table_2 += '\\hline Training wiht BM and IM & {0:.3f} & {1:.3f}  & {2:.3f} & {3:.3f} & {4:.3f} &  {5:.3f}  & {6:.3f} & {7:.3f} \\\\\n'.format(ijcai_both_normal_record.total_average_value_aauc, ijcai_both_normal_record.total_average_value_af, ijcai_both_bm_record.total_average_value_aauc, ijcai_both_bm_record.total_average_value_af, ijcai_both_im_record.total_average_value_aauc, ijcai_both_im_record.total_average_value_af, ijcai_both_both_record.total_average_value_aauc, ijcai_both_both_record.total_average_value_af)
# table_2 += '\\hline\n'

# table_2 += '\\end{tabular}\n'
# table_2 += '\\end{table}\n'

# record = open('result_table.txt','w')
# record.write(table_1)
# record.write(table_2)