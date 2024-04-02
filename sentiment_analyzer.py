import boto3
import sys
import re

text= "oneLineText.txt"
text2="analysis.txt"


def analyzer(texto):
    
    def analyze_conversation(textoU):
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

        # Lee el contenido del archivo
        conversation = textoU

        # Dividimos el contenido del archivo en turnos de cliente y vendedor
        turns = conversation.split('Cliente: ')[1:]

        print("Ha ingresado a analysis with process")
        respuesta = ""
        for turn in turns:
            print( turn.split('Vendedor: '))
            client_turn, agent_turn = turn.split('Vendedor: ')

            client_sentiment = comprehend.detect_sentiment(Text=client_turn, LanguageCode='es')['Sentiment']
            client_emotion = comprehend.detect_sentiment(Text=client_turn, LanguageCode='es')['SentimentScore']

            agent_sentiment = comprehend.detect_sentiment(Text=agent_turn, LanguageCode='es')['Sentiment']
            agent_emotion = comprehend.detect_sentiment(Text=agent_turn, LanguageCode='es')['SentimentScore']

            

            respuesta += "Cliente Turno: "+ client_turn + "\n"
            respuesta += "Sentimiento del Cliente: " + client_sentiment + "\n"
            respuesta += "Emoción del Cliente: " + max(client_emotion, key=client_emotion.get) + "\n"
            respuesta += "Sentimiento del Vendedor: "+ agent_sentiment+ "\n"
            respuesta += "Emoción del Vendedor: "+ max(agent_emotion, key=agent_emotion.get)+ "\n"
            respuesta += "--------------------------------------------------" + "\n"
            
        return respuesta

    def unificar_lineas(texto):
        contenido_unificado = re.sub(r'\s+', ' ', texto)
        return contenido_unificado
            
        
        
    oneLineText = unificar_lineas(texto)
    
    return analyze_conversation(oneLineText)
    
