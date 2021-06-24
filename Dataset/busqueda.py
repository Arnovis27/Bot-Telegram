import csv

csvFile = open("./DB/data.csv", "r")
csvReader = csv.reader(csvFile, delimiter=",")
res = [[str(n) for n in line] for line in csvReader]
csvFile.close()

pokename=[]

#Agregando a una lista simple
for lista1 in res:
    for numero in lista1:
        pokename.append(numero)

#print(pokename)

#Busqueda dentro de la lista
palabra= "nidorino"
cadena= ["rotom","arceus","moltres","zubat","lugia","aredactyl-mega","nidorino","nidorina"]
ocurrenciatotal=[0 for i in range(len(cadena))]


for z in range(len(cadena)):
    aux2= z
    contador=0
    for c in palabra:
        if(len(cadena[aux2])<= len(palabra)+1):
            ocurrencia= cadena[aux2].count(c)    
            contador= contador+ ocurrencia

    ocurrenciatotal[z]= contador
print(cadena,ocurrenciatotal)

nuevalista=[]
maximo= max(ocurrenciatotal)

for i in range(len(cadena)):
    if (ocurrenciatotal[i]>= len(palabra)-1 and ocurrenciatotal[i]<= maximo):
        nuevalista.append(cadena[i])

print(nuevalista[1][0])

