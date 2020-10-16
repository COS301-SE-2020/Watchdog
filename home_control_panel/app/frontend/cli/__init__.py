from pprint import pprint


def debug(obj, header=None, footer=None):
    if header is not None:
        print('-------\t'+str(header)+'\t--------------')
    if type(obj) is str:
        print('\t'+str(obj))
    else:
        pprint(obj, indent=4)
    if footer is not None:
        print('-------\t'+str(footer)+'\t--------------')
