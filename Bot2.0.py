from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ChatAction
import requests, urllib
import csv

INPUT_TEXT=0

def start(update, context):

    update.message.reply_text("Hola,Bienvendio\n\nEsta es la linea de comandos que manejo hasta ahora\n/pokemon Buscar datos de un pokemon")

def pokemon_Command_Handler(update,context):

    update.message.reply_text("Enviame el nombre del pokemon a encontrar")

    return INPUT_TEXT

def send_imag(text,update,context):
    url='http://pokeapi.co/api/v2/pokemon/'
    pokename= text.lower()

    url2= url + pokename
    response= requests.get(url2)

    if response.status_code == 200:
        response2= requests.get(url2)
        payload2= response2.json()
        sprites= payload2.get('sprites', [])
        front_sprite=''

        update.message.reply_text(pokename.upper())
        if sprites:
            #Descargando Imagen
            front_sprite= sprites['front_default']
            imagen= open("./Sprite/Sprite.png", 'wb')
            imagen.write(urllib.request.urlopen(front_sprite).read())
            imagen.close()
        
        imagen2= "./Sprite/Sprite.png"
        chat= update.message.chat
        chat.send_action(
        	action=ChatAction.UPLOAD_PHOTO,
        	timeout=None
    	)
        
        chat.send_photo(
        	photo=open(imagen2, 'rb')
    	)
        
        get_pokemons(text,update,context)

    else:
        update.message.reply_text("Es muy probable que hayas escrito mal o el pokemon no este registrado, Te dare una lista seleccionada con ciertos criterios de busque para que identifiques el nombre de tu pokemon, esto puede tardar mas de 10 segundos.")
        
        csvFile = open("./DB/data.csv", "r")
        csvReader = csv.reader(csvFile, delimiter=",")
        res = [[str(n) for n in line] for line in csvReader]
        csvFile.close()

        lista=[]

        #Agregando a una lista simple
        for lista1 in res:
            for numero in lista1:
                lista.append(numero)

        #Busqueda dentro de la lista
        ocurrenciatotal=[0 for i in range(len(lista))]

        for z in range(len(lista)):
            aux2= z
            contador=0
            for c in pokename:
                if(len(lista[aux2]) <= len(pokename)+1):
                    ocurrencia= lista[aux2].count(c)    
                    contador= contador+ ocurrencia
            ocurrenciatotal[z]= contador
        
        nuevalista=[]
        maximo= max(ocurrenciatotal)
        for i in range(len(lista)):
            if (ocurrenciatotal[i]>= len(pokename)-1 and ocurrenciatotal[i]<= maximo):
                nuevalista.append(lista[i])
        
        f = open ('./DB/sugerencia.txt','w')
        for i in range(len(nuevalista)):
            f.write(nuevalista[i]+"\n")
        f.close()

        chat= update.message.chat
        chat.send_action(
        	action=ChatAction.UPLOAD_DOCUMENT,
        	timeout=None
    	)
        
        chat.send_document(
        	document=open('./DB/Sugerencia.txt', 'rb')
    	)

        update.message.reply_text("Dentro de ese archivo encontraras la lista de pokemons escogidos con cierto grado segun el nombre que digitaste, porfavor te invito a intentar de nuevo la busqueda /pokemon")
    

def get_pokemons(text,update,context):
    url='http://pokeapi.co/api/v2/pokemon/'
    pokename= text.lower()

    url2= url + pokename
    response= requests.get(url2)
    vacio1=[]
    vacio2=[]
    vacio3=[]



    if response.status_code == 200:
        response2= requests.get(url2)
        payload2= response2.json()
        types= payload2.get('types', [])
        abilities= payload2.get('abilities', [])
        stats= payload2.get('stats', [])
        tipo1=0
        habilidad=0
        stabs=0
        valor=0

        if types:
            for tipos in types:
                tipo1= tipos['type']
                vacio1.append(tipo1['name'])

        if abilities:
            for hiden in abilities:
                habilidad= hiden['ability']
                vacio2.append(habilidad['name'])

        if stats:
            for base in stats:
                valor= base['base_stat']
                stabs= base['stat']
                vacio3.append(stabs['name'])
                vacio3.append(valor)    

        update.message.reply_text("***Tipo***\n"+' - '.join(vacio1)+"\n***Habilidades***\n"+'  '.join(vacio2)+"\n***Stab Base***\n"+'  '.join(map(str,vacio3)))
        update.message.reply_text("No olvides que para seguir buscando debes ingresar antes el comando  :)")

def input_text(update, context):

    text= update.message.text

    send_imag(text,update,context)

    print(text)

    return ConversationHandler.END


if __name__ == '__main__':

    updater= Updater(token="659182708:AAGAMoJ3ZsK6bj9Qt4OzkbWpefkDRPi9s70", use_context=True)
    
    dp= updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('pokemon',pokemon_Command_Handler)
        ],
        states={
            INPUT_TEXT:[MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()