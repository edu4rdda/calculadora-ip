import streamlit as st
import ipaddress

#streamlit run calculadora_ip.py

#separação de octetos
def separar_octetos(endereco):
    octetos = endereco.split(".")

    if len(octetos) != 4:
        return "O endereço deve conter precisamente 4 octetos"

    for octeto in octetos:
        if not octeto.isdigit():
            return "Deve ser números"
        if not 0 <= int(octeto) <= 255:
            return "Deve ser um número entre 0 e 255"
    
    return octetos

#calcular endereço, primeiro, último e broadcast
def calculo_principal(completa):
    endereco_rede = completa.network_address
    broadcast = completa.broadcast_address
    hosts = list(completa.hosts())
    primeira_host = hosts[0]
    ultima_host = hosts[-1]

    return endereco_rede, broadcast, primeira_host, ultima_host

#privado e publico + tipo da classe
def c_classe(octeto1):
    if 0 <= octeto1 <= 127:
        classe = "Classe A"  
    elif 128 <= octeto1 <= 191:
        classe = "Classe B"
    elif 192 <= octeto1 <= 223:
        classe = "Classe C"
    elif 224 <= octeto1 <= 239:
        classe = "Classe D"
    elif 140 <= octeto1 <= 255:
        classe = "Classe E"
    else:
        classe = "Inválido"

    if octeto1 == 10 or octeto1 == 172 or octeto1 == 192:
        tipo = "Privado"
    else:
        tipo = "Público"

    return classe, tipo

#sub-redes geradas
def calculo_subredes(mascara):
    if mascara < 24:
        geradas  = 2 ** (24 - mascara)
    else:
        geradas = 2 ** (mascara - 24)

    return geradas

#hosts por sub-redes
def calculo_hosts(mascara):
    h = 32 - mascara
    hosts = (2 ** h) - 2
    return hosts

st.title("Calculadora IP")

endereco = st.text_input("Digite o Endereço IP (ex.: 192.168.0.1)")
mascara = st.number_input("Digite a Máscara de Sub-rede (ex.: 25)", value=1, step=1, max_value=32, min_value=1)

# Criando o botão de cálculo
calcular = st.button("Calcular")

if calcular and endereco:
    redes = [["Parâmetro", "Valor"]]
    octetos = separar_octetos(endereco)
    if isinstance(octetos, list):
        completa = ipaddress.IPv4Network(f"{endereco}/{mascara}", strict=False)
        octeto1 = int(octetos[0])
        classe, tipo = c_classe(octeto1)
        endereco_rede, broadcast, primeira_host, ultima_host = calculo_principal(completa)
        redes.append(["Endereço IP", endereco])
        redes.append(["Máscara de Sub-rede", mascara])
        redes.append(["Endereço de Rede", endereco_rede])
        redes.append(["Primeiro Host", primeira_host])
        redes.append(["Último Host", ultima_host])
        redes.append(["Endereço de Broadcast", broadcast])
        redes.append(["Classe do Endereço", classe])
        redes.append(["Número de Sub-redes", calculo_subredes(mascara)])
        redes.append(["Hosts por Sub-redes", calculo_hosts(mascara)])
        redes.append(["Endereço Público/Privado", tipo])
    else:
        redes.append(["Erro", octetos])
    st.table(redes)
