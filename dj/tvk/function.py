def imns_to_choice(imns_list):
    rez = []
    for i_imns in imns_list:
        buf = (i_imns.id, i_imns.number)
        rez.append(buf)
    return rez