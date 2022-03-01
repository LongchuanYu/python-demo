import select

def socket_listener(sock):
    inputs = sock
    r_list, w_list, e_list = select.select(inputs, [], inputs, 1)
    print(r_list)