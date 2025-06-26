# Versão atualizada com devolução e banco simulado embutido, com validações de uso incorreto restauradas

import time
import board
import busio
import digitalio
import wifi
import socketpool
import adafruit_requests
import json
from adafruit_pn532.i2c import PN532_I2C
from adafruit_character_lcd.character_lcd import Character_LCD_Mono
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets

# --- Função compatível com CircuitPython para data/hora ---
def obter_data_hora_str():
    t = time.localtime()
    return f"{t.tm_year}-{t.tm_mon:02}-{t.tm_mday:02} {t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}"

# --- Banco de dados simulado ---
banco_dados_locacoes = []

def uid_para_string(uid):
    return "-".join(str(b) for b in uid)

def registrar_locacao(nome_proj, nome_prof):
    banco_dados_locacoes.append({
        "dispositivo": nome_proj,
        "professor": nome_prof,
        "data_hora": obter_data_hora_str(),
        "timestamp": time.monotonic(),
        "status": "Locado"
    })

def registrar_devolucao(nome_proj):
    for registro in reversed(banco_dados_locacoes):
        if registro["dispositivo"] == nome_proj and registro["status"] == "Locado":
            tempo_agora = time.monotonic()
            tempo_locacao = registro.get("timestamp", tempo_agora)
            tempo_passado = tempo_agora - tempo_locacao
            if tempo_passado < 300:
                lcd.clear()
                lcd.message = "Confirmar\nDevolucao?"
                for _ in range(5):
                    led_vermelho.value = True
                    bip()
                    time.sleep(0.1)
                    led_vermelho.value = False
                    time.sleep(0.1)
                lcd.clear()
                lcd.message = "Aproxime\no projetor"
                tempo_confirm = time.monotonic()
                while (time.monotonic() - tempo_confirm) < 5:
                    confirm_uid = pn532.read_passive_target(timeout=0.5)
                    if confirm_uid:
                        confirm_nome = get_projetor_nome(list(confirm_uid))
                        if confirm_nome == nome_proj:
                            break
                        else:
                            lcd.clear()
                            lcd.message = "Tag incorreta\nDevolucao negada"
                            time.sleep(2)
                            return False
                else:
                    lcd.clear()
                    lcd.message = "Cancelado.\nRetorne depois"
                    time.sleep(2)
                    return False
            registro["status"] = "Devolvido"
            registro["data_hora"] = obter_data_hora_str()
            registro["timestamp"] = time.monotonic()
            payload = {
                "acao": "devolucao",
                "dispositivo": nome_proj,
                "professor": registro["professor"],
                "data_hora": registro["data_hora"]
            }
            mqtt_client.publish("db/test", json.dumps(payload))
            return True
    return False

def esta_locado(nome_proj):
    for registro in reversed(banco_dados_locacoes):
        if registro["dispositivo"] == nome_proj:
            return registro["status"] == "Locado"
    return False

print("Conectando ao Wi-Fi...")
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Conectado! IP:", wifi.radio.ipv4_address)
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)
time.sleep(2)

def connected(client, userdata, flags, rc):
    print("Conectado ao broker MQTT!")

def message(client, topic, message):
    print(f"Nova mensagem em {topic}: {message}")

mqtt_client = MQTT.MQTT(
    broker="10.0.0.176",
    port=1883,
    socket_pool=pool,
    client_id="leitor_rfid_1"
)
mqtt_client.on_connect = connected
mqtt_client.on_message = message

print("Conectando ao MQTT...")
for i in range(3):
    try:
        mqtt_client.connect()
        break
    except Exception as e:
        print(f"Erro na conexão MQTT ({i+1}/3): {e}")
        time.sleep(2)
else:
    raise RuntimeError("Falha ao conectar ao broker MQTT.")

lcd_rs = digitalio.DigitalInOut(board.GP0)
lcd_en = digitalio.DigitalInOut(board.GP1)
lcd_d4 = digitalio.DigitalInOut(board.GP2)
lcd_d5 = digitalio.DigitalInOut(board.GP3)
lcd_d6 = digitalio.DigitalInOut(board.GP4)
lcd_d7 = digitalio.DigitalInOut(board.GP5)
lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 16, 2)

lcd.clear()
lcd.message = "Iniciando..."
time.sleep(1)

i2c = busio.I2C(scl=board.GP7, sda=board.GP6)
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

lcd.clear()
lcd.message = "Aproxime um\nprojetor!"

projetores_uid = {
    "Projetor 1": [0xF3, 0x6D, 0x6A, 0xF7],
    "Projetor 2": [0x33, 0x9E, 0x85, 0xA5],
    "Projetor 3": [0xF3, 0xDA, 0xFD, 0xA5]
}
professores_uid = {
    "Henrique": [0xD3, 0x64, 0xD6, 0xEE],
    "Neto": [0xD3, 0xF7, 0xB9, 0xEE],
}

projetores_locados = []
ultimo_uid_lido = None
tempo_ultimo_uid = 0
INTERVALO_REPETICAO = 1.0

buzzer = digitalio.DigitalInOut(board.GP10)
buzzer.direction = digitalio.Direction.OUTPUT
led_verde = digitalio.DigitalInOut(board.GP11)
led_verde.direction = digitalio.Direction.OUTPUT
led_vermelho = digitalio.DigitalInOut(board.GP12)
led_vermelho.direction = digitalio.Direction.OUTPUT

def match_uid(a, b): return a[:4] == b[:4]
def copiar_uid(src): return src[:4]
def tem_uid(uid): return any(byte != 0 for byte in uid)
def limpar_uid(): return [0, 0, 0, 0]
def print_uid(uid): print(" ".join(f"{b:02X}" for b in uid))
def bip():
    buzzer.value = True
    time.sleep(0.1)
    buzzer.value = False
def uid_na_lista(uid, lista):
    return any(match_uid(uid, item) for item in lista)
def get_professor_nome(uid):
    for nome, prof_uid in professores_uid.items():
        if match_uid(uid, prof_uid): return nome
    return None
def get_projetor_nome(uid):
    for nome, proj_uid in projetores_uid.items():
        if match_uid(uid, proj_uid): return nome
    return None

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    agora = time.monotonic()
    mqtt_client.loop()

    if uid:
        uid = list(uid)
        if uid == ultimo_uid_lido and (agora - tempo_ultimo_uid) < INTERVALO_REPETICAO:
            continue
        ultimo_uid_lido = uid
        tempo_ultimo_uid = agora
        lcd.clear()
        bip()
        led_vermelho.value = True

        nome_proj = get_projetor_nome(uid)
        nome_prof = get_professor_nome(uid)

        if not nome_proj and not nome_prof:
            lcd.message = "Cartao\nDesconhecido!"
            for _ in range(3): bip(); time.sleep(0.1)
            lcd.clear()
            lcd.message = "Tente novamente"
            time.sleep(2)
            led_vermelho.value = False
            continue

        if nome_proj:
            if esta_locado(nome_proj):
                registrar_devolucao(nome_proj)
                lcd.message = f"{nome_proj}\nDevolvido!"
                print(f"Devolvido: {nome_proj}")
            elif uid_na_lista(uid, projetores_locados):
                lcd.message = f"{nome_proj}\nJa adicionado!"
                for _ in range(2): bip(); time.sleep(0.1)
            else:
                projetores_locados.append(copiar_uid(uid))
                lcd.message = f"{nome_proj}\nAguardando prof"
                print(f"Adicionado: {nome_proj}")
            time.sleep(2)
            lcd.clear()
            lcd.message = "Aproxime outro\nprojetor ou prof"
            led_vermelho.value = False
            continue

        if nome_prof and not projetores_locados:
            lcd.message = "Nenhum projetor\nfoi identificado!"
            for _ in range(5): bip(); time.sleep(0.1)
            lcd.clear()
            lcd.message = "Aproxime um\nprojetor!"
            time.sleep(2)
            led_vermelho.value = False
            continue

        if nome_prof:
            for proj_uid in projetores_locados:
                nome_proj = get_projetor_nome(proj_uid)
                registrar_locacao(nome_proj, nome_prof)
                payload = {
                    "acao": "locacao",
                    "professor_uid": uid_para_string(uid),
                    "projetores": [uid_para_string(u) for u in projetores_locados],
                    "data_hora": obter_data_hora_str()
                }
            mqtt_client.publish("db/test", json.dumps(payload))
            lcd.message = "Locacao\nRegistrada!"
            print(f"Locacao por {nome_prof}")
            time.sleep(2)
            projetores_locados.clear()
            lcd.clear()
            lcd.message = "Aproxime um\nprojetor!"
            led_vermelho.value = False