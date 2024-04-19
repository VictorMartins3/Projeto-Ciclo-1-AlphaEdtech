from services.rg_posprocessing import *
from services.ocr_service import extract_roi

def rg_detection(aligned, resultados):
    dados_rg = {}

    key_points = {
            'nome': (100, 180),
            'rg': (230, 100),
            'cpf': (100, 615),
            'nascimento': (840, 440),
            }

    roi_nome, tp_nome, largura_nome, altura_nome, nome = extract_roi(aligned, resultados, key_points['nome'])
    dados_rg['nome'] = valida_nome_rg(aligned, tp_nome, largura_nome, altura_nome, nome)

    roi_rg, tp_rg, largura_rg, altura_rg, rg = extract_roi(aligned, resultados, key_points['rg'])    
    dados_rg['rg'] = valida_rg(aligned, tp_rg, largura_rg, altura_rg, rg)

    roi_cpf, tp_cpf, largura_cpf, altura_cpf, cpf = extract_roi(aligned, resultados, key_points['cpf'])    
    dados_rg['cpf'] = valida_cpf_rg(aligned, tp_cpf, largura_cpf, altura_cpf, cpf)

    roi_data, tp_data, largura_data, altura_data, data= extract_roi(aligned, resultados, key_points['nascimento'])
    dados_rg['data de nascimento']  = valida_data_rg(aligned, tp_data, largura_data, altura_data, data)

    return dados_rg