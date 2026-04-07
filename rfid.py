import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from datetime import datetime

LED_VERDE = 18    
LED_VERMELHO = 23 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_VERDE, GPIO.OUT)
GPIO.setup(LED_VERMELHO, GPIO.OUT)

reader = SimpleMFRC522()

colaboradores = {
    482200016945: {"nome": "Gabriel", "acesso": True},
    48532257410: {"nome": "Ricardo", "acesso": False}
}

estado_sala = {}        
tempo_acumulado = {}    
tentativas_negadas = {} 
tentativas_invasao = 0

def acender_verde():
    GPIO.output(LED_VERDE, True)
    time.sleep(5)
    GPIO.output(LED_VERDE, False)

def acender_vermelho_fixo():
    GPIO.output(LED_VERMELHO, True)
    time.sleep(5)
    GPIO.output(LED_VERMELHO, False)

def piscar_vermelho_invasao():
    for _ in range(10):
        GPIO.output(LED_VERMELHO, True)
        time.sleep(0.2)
        GPIO.output(LED_VERMELHO, False)
        time.sleep(0.2)

def formatar_tempo(segundos_totais):
    horas = int(segundos_totais // 3600)
    minutos = int((segundos_totais % 3600) // 60)
    segundos = int(segundos_totais % 60)
    return f"{horas}h {minutos}min {segundos}s"

print(">>> Sistema de Controle de Acesso Iniciado...")

try:
    while True:
        uid, _ = reader.read()
        agora = datetime.now()

        if uid in colaboradores:
            p = colaboradores[uid]
            nome = p["nome"]

            if p["acesso"]:
                if uid not in estado_sala:
                    estado_sala[uid] = {"dentro": False, "ja_entrou_hoje": False, "entrada": None}

                if not estado_sala[uid]["dentro"]:
                    if not estado_sala[uid]["ja_entrou_hoje"]:
                        print(f"Bem-vindo, {nome}")
                        estado_sala[uid]["ja_entrou_hoje"] = True
                    else:
                        print(f"Bem-vindo de volta, {nome}")
                    
                    estado_sala[uid]["dentro"] = True
                    estado_sala[uid]["entrada"] = agora
                    acender_verde()

                else:
                    hora_entrada = estado_sala[uid]["entrada"]
                    duracao = (agora - hora_entrada).total_seconds()
                    tempo_acumulado[uid] = tempo_acumulado.get(uid, 0) + duracao
                    
                    estado_sala[uid]["dentro"] = False
                    print(f"{nome} saiu da sala.")
                    print(f"Tempo permanecido na sala: {formatar_tempo(duracao)}")
                    acender_verde()

            else:
                print(f"Você não tem acesso a este projeto, {nome}")
                tentativas_negadas[nome] = tentativas_negadas.get(nome, 0) + 1
                acender_vermelho_fixo()

        else:
            print("Identificação não encontrada!")
            tentativas_invasao += 1
            piscar_vermelho_invasao()

        time.sleep(1) 

except KeyboardInterrupt:
    print("\n\n" + "="*40)
    print("        RELATÓRIO FINAL DE ACESSO")
    print("="*40)

    print("\nTEMPO TOTAL DE PERMANÊNCIA:")
    if not tempo_acumulado:
        print("Nenhum registro de permanência finalizado.")
    for uid, total in tempo_acumulado.items():
        n = colaboradores[uid]["nome"]
        print(f"- {n}: {formatar_tempo(total)}")

    print("\nCOLABORADORES NÃO AUTORIZADOS (TENTATIVAS):")
    for nome_bloqueado, qtd in tentativas_negadas.items():
        print(f"- {nome_bloqueado}: {qtd} vez(es)")

    print(f"\nTOTAL DE TENTATIVAS DE INVASÃO: {tentativas_invasao}")
    print("="*40)

    GPIO.cleanup()
    print("Sistema encerrado com sucesso.")