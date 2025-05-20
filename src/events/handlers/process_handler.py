message_received = []

def handle_message(payload):
    message_received.append(payload)
    print("✅ Callback executado com mensagem:", payload)

def handle_message_test(payload):
    message_received.append(payload)
    print("procesando no banco de dados: ", payload)