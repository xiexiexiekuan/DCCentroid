import numpy
import csv


# 生成某区间内可重复的一定数量的随机数的方法
def random_cut_data(max_number, random_set_num=2000):
    random_split_list = []
    # print('max_number: ', max_number)
    # numpy.random.seed(0)  # 设置随机数种子
    for i in range(random_set_num):
        # randint(a, b)生成一个a<=且<b的数
        random_range = numpy.random.randint(10, 200)
        if random_range > max_number:
            random_range = max_number
        # 有放回的随机抽样，一次抽取size个数表示
        # replace代表抽样之后还放不放回去，False那么一次挑选出来的数都不一样，True有可能会出现重复的，因为前面的抽的放回去了
        # 每个基因集合的基因可以重复，但是单个基因集合不应该重复，此处应该为False
        random_split_list.append(numpy.random.choice(range(0, max_number), size=random_range, replace=False))
    # numpy.random.seed()  # 种子重置
    # 新的numpy版本将-创建不同长度或形状的列表或元组的功能-弃用
    return numpy.array(random_split_list, dtype=object)


# 根据已知基因集合进行集合划分
def known_gene_set(gene_id, file_name):
    c_data = csv.reader(open(file_name, 'r'))
    g_set = []
    for var in c_data:
        g_set.append(numpy.array(var[0].split('\t'))[2:].astype('int32'))  # 数据分割，取出编号
    gene_symbol_set = numpy.array(g_set, dtype=object)  # 基因编号集合
    # print(gene_symbol_set)

    gene_subscript_set = []  # 基因下标集合
    for index_set, gene_set_ in enumerate(gene_symbol_set):
        gene_subscript_set_current = []  # 当前基因下标集合
        # print('len: ', len(gene_set_))
        # print(gene_set_)
        for index, i in enumerate(gene_set_):  # 遍历一个基因集合
            find_index = numpy.where(gene_id == i)[0]  # 找到一个基因编号对应的下角标
            if len(find_index) > 0:  # 若未找到，则为空列表，长度为0
                # print('添加基因下角标：', find_index[0])
                gene_subscript_set_current.append(find_index[0])  # 将找到的下角标保存
            else:
                # print('删除基因编号：', i)
                pass  # 如果没有找到，就跳过该基因，不予保存
        if 10 <= len(gene_subscript_set_current) <= 200:
            # print(len(gene_subscript_set_current))
            gene_subscript_set.append(numpy.array(gene_subscript_set_current, dtype=object).astype('int32'))
        else:
            # print('基因集合过小，予以删除：gene_symbol_set[', index_set, ']')
            pass  # 将基因集合的基因数量大于等于10的留下。较小的基因集合意义不大
    gene_subscript_set = numpy.array(gene_subscript_set, dtype=object)

    return gene_subscript_set
