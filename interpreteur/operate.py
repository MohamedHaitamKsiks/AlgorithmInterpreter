

def operate_without_bar(operation) :
    #remove spaces
    operation = operation.replace(" ","")
    #replace - by +(-
    operation = operation.replace("-","+-")
    operation.startswith("0+")
    #split by *
    numbers = operation.split("+")

    #calculate
    result = 0
    for i in numbers :
        #mult
        i_mult = 1
        numbers_in_i = i.split("*")
        for j in numbers_in_i :
            #div
            numbers_in_j = j.split("/")
            numbers_in_j.append("1")
            j_div = float(numbers_in_j[0])
            for k in numbers_in_j[1:] :
                j_div/=float(k)
            i_mult*=j_div
        result+=i_mult

    return result

def operate(operation) :
    result = ""
    #remove spaces
    operation = operation.replace(" ","")
    #replace - by +(-
    operation = operation.replace("-","+-")

    while "(" in operation:
        op = list()
        for i in operation :
            op.append(i)
        op.reverse()

        start = len(operation) - op.index('(')
        op.reverse()
        end = op.index(")",start)

        opr1 = operation[start-1:end+1]
        opr2 = operation[start:end]

        operation = operation.replace(opr1,str(operate_without_bar(opr2)))

    return operate_without_bar(operation)
