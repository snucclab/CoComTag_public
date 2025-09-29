def gold_inds_to_one_hot(ind_list):
    sf_a = []
    sf_b = []
    sf_c = []
    sf_d = []
    sf_e = []
    sf_f = []
    sf_x = []

    for ind in ind_list:
        ind_a, ind_b, ind_c, ind_d, ind_e, ind_f, ind_x = 0, 0, 0, 0, 0, 0, 0
        for i in ind[0].strip("\"").replace(' ','').split(','):
            if i in ['a','b','c']:
                ind_a = 1
            if i in ['d','e']:
                ind_b = 1
            if i in ['f','g','h','i']:
                ind_c = 1
            if i in ['j','k']:
                ind_d = 1
            if i in ['l','m','n']:
                ind_e = 1
            if i in ['o','p','q']:
                ind_f = 1
            if i == 'x':
                ind_x = 1
            if i == '-':
                ind_x = 1
        sf_a.append(ind_a)
        sf_b.append(ind_b)
        sf_c.append(ind_c)
        sf_d.append(ind_d)
        sf_e.append(ind_e)
        sf_f.append(ind_f)
        sf_x.append(ind_x)

    return sf_a, sf_b, sf_c, sf_d, sf_e, sf_f, sf_x


def pred_inds_to_one_hot(pred_data):
    sf_a = []
    sf_b = []
    sf_c = []
    sf_d = []
    sf_e = []
    sf_f = []
    sf_x = []

    for ind in pred_data:
        # print(ind)
        ind_a, ind_b, ind_c, ind_d, ind_e, ind_f, ind_x = 0, 0, 0, 0, 0, 0, 0
        # labels = eval(ind)['category']
        # print(ind)
        labels = ind['category']
        if isinstance(labels, list):
            for l in labels:
                # print(l)
                i = l['category'].split(')')[0].strip('(').strip(')')
                if i in ['a','b','c']:
                    ind_a = 1
                if i in ['d','e']:
                    ind_b = 1
                if i in ['f','g','h','i']:
                    ind_c = 1
                if i in ['j','k']:
                    ind_d = 1
                if i in ['l','m','n']:
                    ind_e = 1
                if i in ['o','p','q']:
                    ind_f = 1
                if i == 'x':
                    ind_x = 1
                if i == '-':
                    ind_x = 1
        else:
            i = labels.split(')')[0].strip('(').strip(')')
            if i in ['a','b','c']:
                ind_a = 1
            if i in ['d','e']:
                ind_b = 1
            if i in ['f','g','h','i']:
                ind_c = 1
            if i in ['j','k']:
                ind_d = 1
            if i in ['l','m','n']:
                ind_e = 1
            if i in ['o','p','q']:
                ind_f = 1
            if i == 'x':
                ind_x = 1
            if i == '-':
                ind_x = 1
        sf_a.append(ind_a)
        sf_b.append(ind_b)
        sf_c.append(ind_c)
        sf_d.append(ind_d)
        sf_e.append(ind_e)
        sf_f.append(ind_f)
        sf_x.append(ind_x)

    return sf_a, sf_b, sf_c, sf_d, sf_e, sf_f, sf_x



def prepare_kappa(gold_label, pred_label):
    rater_11 = 0
    rater_10 = 0
    rater_01 = 0
    rater_00 = 0

    for (g,p) in zip(gold_label, pred_label):
        if g==1:
            if p==1:
                rater_11 += 1
            else:
                rater_10 += 1
        elif p==1:
            rater_01 += 1
        else:
            rater_00 += 1

    tp = rater_00 + rater_11
    total = rater_00 + rater_01 + rater_10 + rater_11
    # print(total)
    # assert(total == len(df))

    val1 = ((rater_11 + rater_01) * (rater_11 + rater_10)) / total
    val2 = ((rater_10 + rater_00) * (rater_01 + rater_00)) / total
    
    return rater_11, val1


def calcu_kappa(gold, pred):
    gold_inds = gold_inds_to_one_hot(gold)
    pred_inds = pred_inds_to_one_hot(pred)
    a_11, a_val1 = prepare_kappa(gold_inds[0], pred_inds[0])
    b_11, b_val1 = prepare_kappa(gold_inds[1], pred_inds[1])
    c_11, c_val1 = prepare_kappa(gold_inds[2], pred_inds[2])
    d_11, d_val1 = prepare_kappa(gold_inds[3], pred_inds[3])
    e_11, e_val1 = prepare_kappa(gold_inds[4], pred_inds[4])
    f_11, f_val1 = prepare_kappa(gold_inds[5], pred_inds[5])
    x_11, x_val1 = prepare_kappa(gold_inds[6], pred_inds[6])

    sum_a = a_11 + b_11 + c_11 + d_11 + e_11 + f_11 + x_11 
    sum_ef = a_val1 + b_val1 + c_val1 + d_val1 + e_val1 + f_val1 + x_val1 
    kappa =  (sum_a - sum_ef) / (len(gold_inds[0]) - sum_ef)

    return kappa


def calcu_kappa_subfacet(gold, pred):
    gold_inds = gold_inds_to_one_hot(gold)
    pred_inds = pred_inds_to_one_hot_subfacet(pred)
    a_11, a_val1 = prepare_kappa(gold_inds[0], pred_inds[0])
    b_11, b_val1 = prepare_kappa(gold_inds[1], pred_inds[1])
    c_11, c_val1 = prepare_kappa(gold_inds[2], pred_inds[2])
    d_11, d_val1 = prepare_kappa(gold_inds[3], pred_inds[3])
    e_11, e_val1 = prepare_kappa(gold_inds[4], pred_inds[4])
    f_11, f_val1 = prepare_kappa(gold_inds[5], pred_inds[5])
    x_11, x_val1 = prepare_kappa(gold_inds[6], pred_inds[6])

    sum_a = a_11 + b_11 + c_11 + d_11 + e_11 + f_11 + x_11
    sum_ef = a_val1 + b_val1 + c_val1 + d_val1 + e_val1 + f_val1 + x_val1
    kappa =  (sum_a - sum_ef) / (len(gold_inds[0]) - sum_ef)

    return kappa


def pred_inds_to_one_hot_subfacet(pred_data):
    sf_a = []
    sf_b = []
    sf_c = []
    sf_d = []
    sf_e = []
    sf_f = []
    sf_x = []

    for labels in pred_data:
        # print(ind)
        ind_a, ind_b, ind_c, ind_d, ind_e, ind_f, ind_x = 0, 0, 0, 0, 0, 0, 0
       
        i = labels[0].split(')')[0].strip('(').strip(')')
        if i == 'a':
            ind_a = 1
        if i == 'b':
            ind_b = 1
        if i == 'c':
            ind_c = 1
        if i == 'd':
            ind_d = 1
        if i == 'e':
            ind_e = 1
        if i == 'f':
            ind_f = 1
        if i == 'x':
            ind_x = 1
        if i == '-':
            ind_x = 1
        
        sf_a.append(ind_a)
        sf_b.append(ind_b)
        sf_c.append(ind_c)
        sf_d.append(ind_d)
        sf_e.append(ind_e)
        sf_f.append(ind_f)
        sf_x.append(ind_x)

    return sf_a, sf_b, sf_c, sf_d, sf_e, sf_f, sf_x


def gold_inds_to_one_hot_facet(ind_list):
    sf_a = []
    sf_b = []
    sf_c = []
    sf_x = []

    for ind in ind_list:
        ind_a, ind_b, ind_c, ind_x = 0, 0, 0, 0
        for i in ind[0].strip("\"").replace(' ','').split(','):
            if i in ['a','b','c','d','e']:
                ind_a = 1
            if i in ['f','g','h','i','j','k']:
                ind_b = 1
            if i in ['l','m','n','o','p','q']:
                ind_c = 1
            if i == 'x':
                ind_x = 1
            if i == '-':
                ind_x = 1
        sf_a.append(ind_a)
        sf_b.append(ind_b)
        sf_c.append(ind_c)
        sf_x.append(ind_x)

    return sf_a, sf_b, sf_c, sf_x


def pred_inds_to_one_hot_facet(pred_data):
    sf_a = []
    sf_b = []
    sf_c = []
    sf_x = []

    for ind in pred_data:
        # print(ind)
        ind_a, ind_b, ind_c, ind_x = 0, 0, 0, 0
        # labels = eval(ind)['category']
        # print(ind)
        labels = ind['category']
        if isinstance(labels, list):
            for l in labels:
                # print(l)
                i = l['category'].split(')')[0].strip('(').strip(')')
                if i == 'a':
                    ind_a = 1
                if i == 'b':
                    ind_b = 1
                if i == 'c':
                    ind_c = 1
                if i == 'x':
                    ind_x = 1
                if i == '-':
                    ind_x = 1
        else:
            i = labels.split(')')[0].strip('(').strip(')')
            if i == 'a':
                ind_a = 1
            if i == 'b':
                ind_b = 1
            if i == 'c':
                ind_c = 1
            if i == 'x':
                ind_x = 1
            if i == '-':
                ind_x = 1
        sf_a.append(ind_a)
        sf_b.append(ind_b)
        sf_c.append(ind_c)
        sf_x.append(ind_x)

    return sf_a, sf_b, sf_c, sf_x


def calcu_kappa_facet(gold, pred):
    gold_inds = gold_inds_to_one_hot_facet(gold)
    pred_inds = pred_inds_to_one_hot_facet(pred)
    a_11, a_val1 = prepare_kappa(gold_inds[0], pred_inds[0])
    b_11, b_val1 = prepare_kappa(gold_inds[1], pred_inds[1])
    c_11, c_val1 = prepare_kappa(gold_inds[2], pred_inds[2])
    d_11, d_val1 = prepare_kappa(gold_inds[3], pred_inds[3])

    sum_a = a_11 + b_11 + c_11 + d_11 
    sum_ef = a_val1 + b_val1 + c_val1 + d_val1 
    kappa =  (sum_a - sum_ef) / (len(gold_inds[0]) - sum_ef)

    return kappa

