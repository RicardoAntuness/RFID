# 📡 Sistema de Leitura RFID com Raspberry Pi

## 📖 Sobre o Projeto

Este projeto tem como objetivo implementar um sistema de leitura de **RFID (Radio Frequency Identification)** utilizando uma **Raspberry Pi** em conjunto com o módulo **MFRC522**.

A aplicação permite identificar tags RFID, capturando o ID e possíveis dados armazenados, podendo ser utilizada em diversos cenários como controle de acesso e automação.

---

## 🚀 Tecnologias Utilizadas

- Python  
- Raspberry Pi  
- Módulo RFID MFRC522  
- Comunicação SPI  

---

## ⚙️ Como Funciona

O sistema realiza a leitura de cartões RFID através do módulo MFRC522.

- O método `read()` fica em execução contínua aguardando a aproximação de uma tag  
- Ao detectar, retorna:
  - ID do cartão  
  - Dados armazenados (se houver)  

Também é possível utilizar:

- `read_id_no_block()` → leitura do ID sem bloquear o sistema  

---

## 🔌 Configuração do Ambiente

### 1. Ativar SPI na Raspberry Pi

```bash
sudo raspi-config
