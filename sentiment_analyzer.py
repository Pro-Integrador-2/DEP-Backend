import boto3
import sys
import re


def analyzer():
    def analyze_conversation(file_path):
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

        # Lee el contenido del archivo
        with open(file_path, 'r') as file:
            conversation = file.read()

        # Dividimos el contenido del archivo en turnos de cliente y vendedor
        turns = conversation.split('Cliente: ')[1:]

        with open("analysis.txt", "w") as output_file:  # Abrir el archivo para escritura
            for turn in turns:
                client_turn, agent_turn = turn.split('Vendedor: ')

                client_sentiment = comprehend.detect_sentiment(Text=client_turn, LanguageCode='es')['Sentiment']
                client_emotion = comprehend.detect_sentiment(Text=client_turn, LanguageCode='es')['SentimentScore']

                agent_sentiment = comprehend.detect_sentiment(Text=agent_turn, LanguageCode='es')['Sentiment']
                agent_emotion = comprehend.detect_sentiment(Text=agent_turn, LanguageCode='es')['SentimentScore']

                sys.stdout = output_file

                print("Cliente Turno: ", client_turn)
                print("Sentimiento del Cliente: ", client_sentiment)
                print("Emoción del Cliente: ", max(client_emotion, key=client_emotion.get))

                print("Vendedor Turno: ", agent_turn)
                print("Sentimiento del Vendedor: ", agent_sentiment)
                print("Emoción del Vendedor: ", max(agent_emotion, key=agent_emotion.get))

                print("--------------------------------------------------")

    def unificar_lineas(archivo_entrada, archivo_salida):
        with open(archivo_entrada, 'r') as f:
            contenido = f.read()

        contenido_unificado = re.sub(r'\s+', ' ', contenido)

        with open(archivo_salida, 'w') as f:
            f.write(contenido_unificado)

    archivo_entrada = 'singleParagraph.txt'
    archivo_salida = 'oneLineText.txt'
    unificar_lineas(archivo_entrada, archivo_salida)
    analyze_conversation("oneLineText.txt")
