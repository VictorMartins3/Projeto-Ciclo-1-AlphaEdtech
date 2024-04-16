from ocr_service import ocr

def verificar_versao_cnh(results):
    keywords = ['driver', 'driving', 'license', 'permiso', 'conducc', 'nacionalid', 'permis', 'conduire', '4a', '4b', '4c', '4d']
    textos = [texto for _, texto, _ in results]
    for keyword in keywords:
        if any(keyword in palavra.lower() for palavra in textos):
            return 'new'
    return 'old' 

def keypoints(version):
    if version == 'new':
        key_points = {
            'nome': (210, 230),
            'rg': (510, 410),
            'cpf': (520, 470),
            'nascimento': (510, 290),
            'numero': (0, 104),
            'registro': (740, 470),
            }
    else:
        key_points = {
            'nome': (200, 200),
            'rg': (570, 260),
            'cpf': (570, 350),
            'nascimento': (870, 350),
            'numero': (0, 104),
            'registro': (270, 700),
            }
    return key_points

def valida_nome(imagem, top_left, w, h, texto):
    # Divide a string pelos espaços em branco
    partes = texto.strip().split()
    # Conta o número de palavras na string
    quantidade_nomes = len(partes)
    # Verifica se tem mais de um nome
    if quantidade_nomes > 2:
        return texto #teoricamente pegou o nome completo
    elif quantidade_nomes == 2:
        nova_roi = imagem[top_left[1]-10:top_left[1]+h+10, top_left[0]:top_left[0]+2*w]
    else:
        nova_roi = imagem[top_left[1]-10:top_left[1]+h+10, top_left[0]:top_left[0]+5*w]
    resultado_nome = ocr(nova_roi)
    nome_completo = ' '.join([nome for _, nome, confianca in resultado_nome if confianca > 0.3])
    return nome_completo

def valida_rg(imagem, top_left, w, h, texto):   
    if texto[-1].isalpha():
        return texto
    else:
        nova_roi = imagem[top_left[1]-10:top_left[1]+h+10, top_left[0]:top_left[0]+460]
        resultado_rg = ocr(nova_roi)
        resultado_rg = ' '.join([caracter for _, caracter, confianca in resultado_rg if confianca > 0.3])
    return resultado_rg

def valida_cpf(imagem, top_left, w, h, n_cpf):
    tamanho = len(''.join(char for char in n_cpf if char.isdigit()))
    if tamanho == 11:
        return n_cpf.replace(" ", "") #teoricamente pegou o cpf completo
    else:
        nova_roi = imagem[top_left[1]-10:top_left[1]+h+10, top_left[0]:top_left[0]+280]
        resultado_cpf = ocr(nova_roi)
        cpf_completo = '.'.join([digito for _, digito, confianca in resultado_cpf if confianca > 0.3])
        return cpf_completo.replace(" ", "")