from services.cnh_posprocessing import *
from services.ocr_service import extract_roi, crop_rotate, ocr

def cnh_detection(aligned, resultados):
    dados_cnh = {}

    dados_cnh['versao'] = verificar_versao_cnh(resultados)
    key_points = cnh_keypoints(dados_cnh['versao'])
    
    roi_nome, tp_nome, largura_nome, altura_nome, nome = extract_roi(aligned, resultados, key_points['nome'], data_type = 'varchar')
    dados_cnh['nome'] = valida_nome_cnh(aligned, tp_nome, largura_nome, altura_nome, nome)

    roi_rg, tp_rg, largura_rg, altura_rg, rg = extract_roi(aligned, resultados, key_points['rg'])    
    dados_cnh['rg'], dados_cnh['emissor'], dados_cnh['uf'] = valida_rg_cnh(aligned, tp_rg, largura_rg, altura_rg, rg)

    roi_cpf, tp_cpf, largura_cpf, altura_cpf, cpf = extract_roi(aligned, resultados, key_points['cpf'])    
    dados_cnh['cpf'] = valida_cpf_cnh(aligned, tp_cpf, largura_cpf, altura_cpf, cpf)

    roi_data, tp_data, largura_data, altura_data, data= extract_roi(aligned, resultados, key_points['nascimento'])
    dados_cnh['data de nascimento']  = valida_data_cnh(aligned, tp_data, largura_data, altura_data, data)

    roi_registro, tp_registro, largura_registro, altura_registro, dados_cnh['registro'] = extract_roi(aligned, resultados, key_points['registro']) 

    roi_numero = crop_rotate(aligned)
    resultado_corte = ocr(roi_numero)
    nmr_lateral, tp_lateral, largura_lateral, altura_lateral, dados_cnh['numero verificador'] = extract_roi(roi_numero, resultado_corte, key_points['numero'])

    return dados_cnh