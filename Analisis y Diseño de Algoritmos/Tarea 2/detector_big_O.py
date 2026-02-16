def detector_big_O(codigo):

    lineas = codigo.split('\n')

    max_niveles = 0

    tiene_log = False


    for linea in lineas:

        contenido = linea.strip()

        espacios = len(linea) - len(linea.lstrip())

        nivel = espacios // 4



        if "for " in contenido and "range(n" in contenido:

            if nivel + 1 > max_niveles:

                max_niveles = nivel + 1



        if "while " in contenido and "n" in contenido:

            max_niveles = 1



        if "n = n // 2" in contenido or "n //= 2" in contenido:

            tiene_log = True
            

        if "while" in codigo and "// 2" in codigo and ("low =" in codigo or "high =" in codigo):
            return "O(log n)"




    if max_niveles == 0:

        return "O(1)"



    if tiene_log:

        return "O(log n)"



    if max_niveles == 1:

        return "O(n)"



    if max_niveles == 2:

        return "O(n^2)"



    return "O(n^" + str(max_niveles) + ")"

mi_codigo = """
def binarySearch(listData, value):
    low = 0
    high = len(listData) - 1

    while low <= high:
        mid = (low + high) // 2

        if listData[mid] == value:
            return mid
        elif listData[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return -1

"""

print("Resultado:", detector_big_O(mi_codigo))