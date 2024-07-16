# a = True and False or True
# print(a)

def make_list_modifiers():
    lst = []

    def modify_list_1():
        lst.append(1)

    def modify_list_2():
        lst.append(2)

    def get_list():
        return lst

    return modify_list_1, modify_list_2, get_list


ml1, ml2, gl = make_list_modifiers()
print(ml1, ml2, gl)
print(gl())
print(gl())
ml1()
print(gl())
ml1()
print(gl())
