from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def make_actions(analisis):

    api_key = "yNsYFbqGaPPc2h0uYUUM6Ug1oNlhVLKC"
    model = "mistral-large-latest"
    #model = "open-mistral-7b"
    client = MistralClient(api_key=api_key)

    

    formato_entrada = analisis

    ejemplo_1 = """Después de analizar la conversación entre el cliente y el vendedor, se detecta que el cliente expresó cierta frustración y decepción con respecto a nuestro producto/servicio. Como empresa, es crucial abordar estas emociones de manera proactiva y resolver cualquier problema que pueda haber surgido. En primer lugar, debemos contactar al cliente para expresar nuestra comprensión de sus preocupaciones y disculparnos por cualquier inconveniente que haya experimentado. Luego, ofreceremos soluciones específicas para abordar sus necesidades y resolver cualquier problema pendiente. Además, es importante seguir el progreso de la resolución del problema y garantizar una comunicación abierta y transparente con el cliente en todo momento. Esto ayudará a restaurar la confianza del cliente en nuestra empresa y demostrar nuestro compromiso con la satisfacción del cliente."""

    contexto = """Contexto: Solamente me comunico en español y soy un asistente virtual empresarial para una compañía de servicios. He recibido el resultado de un análisis de sentimientos sobre una conversación entre un cliente y un vendedor. Basándome en este análisis que recibo como entrada y que tiene el siguiente formato:""" + "\n" + formato_entrada + """\nMi único objetivo es generar un único texto corto que indique cómo la empresa debería abordar la situación del cliente y qué acciones tomar a continuación. \n\nEjemplo del texto generado, sería:""" + "\n" + ejemplo_1

    prompt = contexto.strip()

    messages = [ChatMessage(role="user", content=prompt)]

    chat_response = client.chat(
        model=model,
        response_format={"type": "text"},
        messages=messages,
    )

    return chat_response.choices[0].message.content.strip()
