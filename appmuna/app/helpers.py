def split_list (list_dt,n_length):
    return [list_dt[i:i+n_length] for i in range(0, len(list_dt), n_length)]