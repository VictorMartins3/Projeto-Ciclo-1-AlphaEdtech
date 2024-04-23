from services.ocr_service import ocr
import re


def valida_nome_rg(imagem, top_left, w, h, texto):
    # Divide a string pelos espaços em branco
    partes = texto.strip().split()
    # Conta o número de palavras na string
    quantidade_nomes = len(partes)
    # Verifica se tem mais de um nome
    if quantidade_nomes > 2:
        return texto.upper() 
    elif quantidade_nomes == 2:
        nova_roi = imagem[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 3 * w
        ]
    else:
        nova_roi = imagem[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 5 * w
        ]
    resultado_nome = ocr(nova_roi)
    nome_completo = " ".join(
        [nome for _, nome, confianca in resultado_nome if confianca > 0.3]
    )
    return nome_completo.upper()


def valida_rg(imagem, top_left, w, h, texto):
    if texto[-1].isalpha():
        rg = re.findall(r'\d', texto)
        rg = ''.join(rg)
        return rg
    else:
        if len(texto) >= 9:
            return texto.replace(" ","")
        else:
            nova_roi = imagem[
                top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 310
            ]
            resultado_rg = ocr(nova_roi)
            texto = "".join(
                [caracter for _, caracter, confianca in resultado_rg if confianca > 0.3]
            )
            return texto.replace(" ","")


def valida_cpf_rg(imagem, top_left, w, h, n_cpf):
    tamanho = len("".join(char for char in n_cpf if char.isdigit()))
    if tamanho == 11:
        return formatar_cpf(n_cpf)
    else:
        nova_roi = imagem[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] - 100 : top_left[0] + 300
        ]
        resultado_cpf = ocr(nova_roi)
        cpf_completo = ".".join(
            [digito for _, digito, confianca in resultado_cpf if confianca > 0.3]
        )
        return formatar_cpf(cpf_completo) if len(cpf_completo) >= 11 else cpf_completo


def formatar_cpf(cpf):
    if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return cpf
    else:
        cpf_numeros = re.sub(r'\D', '', cpf)
        cpf_formatado = '{}.{}.{}-{}'.format(cpf_numeros[:3], cpf_numeros[3:6], cpf_numeros[6:9], cpf_numeros[9:])
        return cpf_formatado


def valida_data_rg(imagem, top_left, w, h, data):
    data = data.replace(" ","")
    if re.search(r'\b[A-Z]{3}\b', data) and data.count('/') == 2:
        data = ajustar_data(data)

    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(pattern, data):
        return data
    else:
        tamanho = len(data)
        if tamanho < 10:     
            nova_roi = imagem[
                top_left[1] - 10 : top_left[1] + h + 10, top_left[0]: top_left[0] + 300
            ]
            resultado_data = ocr(nova_roi)
            data = "".join([caracter for _, caracter, confianca in resultado_data if confianca > 0.3])
            return data
        else:
            return data
            
def ajustar_data(data):
    meses = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04', 'MAI': '05', 'JUN': '06',
        'JUL': '07', 'AGO': '08', 'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'}
    
    dia, mes_abreviado, ano = data.split('/')
    mes_numerico = meses[mes_abreviado.upper()]
    nova_data = f"{dia}/{mes_numerico}/{ano}"
    return nova_data