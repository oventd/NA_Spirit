exm_list =[]

exemples = [{"1":"apple"}, {"2":"banana"}, {"3":"cherry"},{"4":"cherry"},{"5":"cherry"},{"6":"cherry"}]
for exemple in exemples:
    for keys,values in exemple.items():
        exm_list.append(values)

print(exm_list)