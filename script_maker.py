from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def make_script(transcription_text):

    api_key = "yNsYFbqGaPPc2h0uYUUM6Ug1oNlhVLKC"
    # model = "mistral-large-latest"
    model = "open-mistral-7b"
    client = MistralClient(api_key=api_key)

    # with open("elGas2.txt", "r", encoding="utf-8") as file:
    #     contenido_archivo = file.read()
    #
    # formato_entrada = contenido_archivo.strip()

    formato_entrada = transcription_text

    ejemplo_1 = """Cliente: Voy a retirarme de este plan de datos, ustedes no sirven para nada, me estresa tener que llamar a toda hora, quisiera llorar. Esperaba mucho más de su empresa, estoy inconforme. Vendedor: Lamento mucho escuchar eso, señor. Permítame revisar su contrato y ver qué podemos hacer para mejorar su experiencia. Cliente: Sabe, ahorrece sus palabras ya me dió enojo, no quiero nada. Ya mismo deme el retiro de la suscripción. Vendedor: Usted no me viene a tratar asi, me respeta y no me grite. Conozco su frustración, señor. Haré todo lo posible para resolver este problema lo antes posible. Cliente: Espero que así sea, porque de lo contrario, no dudaré en tomar medidas legales. Vendedor: Por supuesto, haré todo lo posible para evitar que eso suceda."""

    ejemplo_2 = """Vendedor: Hola, gracias por comunicarte con nombreEmpresa, ¿en qué puedo ayudarle?"""

    ejemplo_3 = """Vendedor : Buenos días, se ha comunicado con nombreEmpresa, ¿cómo podemos ayudarle?"""

    ejemplo_4 = """Vendedor: Nos complace que se haya comunicado con nosotros """

    ejemplo_5 = """Vendedor: Buen día soy  pepito perez  soy asesor comercial de nombreEmpresa"""

    ejemplo_6 = """Vendedor: Hola soy  melissa, cómo se encuentra hoy?"""

    ejemplo_7 = """Vendedor:  Soy catalina de soporte tecnico..."""

    contexto = """Solamente me comunico en español, jamás redacto en otro idioma,  yo soy un transcriptor de diálogos que convierte un texto a guión, ya que puedo leer un texto e identificar perfectamente cuando habla un Cliente y cuando habla un Vendedor. Para hacer esto me baso en identificar al vendedor como la persona quien menciona el nombre de una empresa al iniciar la conversación. El dialogo del vendedor suele ser como los siguientes ejemplos""" + "\n" + ejemplo_2 + "\n" + ejemplo_3 + "\n" + ejemplo_4 + "\n" + ejemplo_5 + "\n" + ejemplo_6 + "\n" + ejemplo_7 + "\n" + """Si el texto dice mi número de cédula es, mi número de dirección es, la dirección es, entonces se trata de un cliente. EL Cliente es la persona que está pidiendo ayuda y el Vendedor es la persona que está brindando asistencia o multiples opciones de asesoría; el Cliente está preguntando sobre la política de devoluciones de la empresa, se queja del servicio, hace reclamaciones, pide descuentos de dinero; el Cliente está expresando su satisfacción o insatisfacción con un producto o servicio; el Cliente está solicitando ayuda para realizar una compra, solicita ayuda para soporte técnico, para emergencias, informa sobre daños en el servicio y en los productos. El tono de voz y el lenguaje utilizado de Cliente puede estar frustrado, enojado o ansioso, y puede utilizar un lenguaje emocional y directo. El Vendedor por otra parte se mantiene en un tono de voz profesional y utiliza un lenguaje claro y conciso para brindar información y soluciones. El Cliente puede proporcionar información sobre su cuenta, sus datos, su nombre, su producto o su situación personal, mientras que el Vendedor puede solicitar información adicional o esta misma para brindar asistencia adecuada He recibido el siguiente texto de un diálogo entre dos personas, identificadas como Cliente y la otra como Vendedor. Por ejemplo en este texto: """ + "\n\n" + formato_entrada + """\n\nMi único objetivo es generar un guión con dos hablantes identificados como Vendedor y Cliente sin modificar ninguna palabra del texto original ni alterar su orden y sin generar saltos de línea, solo indicar cuando habla el Vendedor y cuando habla el Cliente pero todos en una sola línea de texto. \n\nUn Ejemplo del texto guión generado sería:""" + "\n" + ejemplo_1 + "\n" + "Como se puede ver, en ninguna parte del guión hay saltos de línea "

    prompt = contexto

    messages = [ChatMessage(role="user", content=prompt)]

    chat_response = client.chat(
        model=model,
        response_format={"type": "text"},
        messages=messages,
    )

    with open("singleParagraph.txt", "w", encoding="utf-8") as file:
        file.write(chat_response.choices[0].message.content.strip())

    with open('singleParagraph.txt', 'r') as file:
        little_paragraph = file.read()

    return little_paragraph
