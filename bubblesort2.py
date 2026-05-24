arreglo = [64,25,12,22,11]

def bububleSort(arreglo):
    n=len(arreglo)
    i=0
    while i < n:
        j=0
        while j < n-i-1:
            if arreglo[j] > arreglo[j+1]:
                arreglo[j], arreglo[j+1] = arreglo[j+1], arreglo[j]
            j+=1
        i+=1
    return arreglo