from posprocessing import *
from ocr_service import extract_roi, crop_rotate, ocr
from preprocessing import preprocess

aligned = preprocess(image_path)  #carregar imagem vinda do streamlit

resultados = ocr(aligned)

if doc_type == 'cnh':  #seleção realizada no streamlit do tipo de documento para upload
    dados = {}

    versao = verificar_versao_cnh(resultados)
    key_points = keypoints(versao)

    roi_nome, tp_nome, largura_nome, altura_nome, nome = extract_roi(aligned, resultados, key_points['nome'])
    dados['nome'] = valida_nome(aligned, tp_nome, largura_nome, altura_nome, nome)

    roi_rg, tp_rg, largura_rg, altura_rg, rg = extract_roi(aligned, resultados, key_points['rg'])    
    dados['rg'] = valida_rg(aligned, tp_rg, largura_rg, altura_rg, rg)

    roi_cpf, tp_cpf, largura_cpf, altura_cpf, cpf = extract_roi(aligned, resultados, key_points['cpf'])    
    dados['cpf'] = valida_cpf(aligned, tp_cpf, largura_cpf, altura_cpf, cpf)

    roi_data, tp_data, largura_data, altura_data, dados['data de nascimento'] = extract_roi(aligned, resultados, key_points['nascimento'])

    roi_registro, tp_registro, largura_registro, altura_registro, dados['registro'] = extract_roi(aligned, resultados, key_points['registro']) 

    roi_numero = crop_rotate(aligned)
    resultado_corte = ocr(roi_numero)
    nmr_lateral, tp_lateral, largura_lateral, altura_lateral, dados['numero verificador'] = extract_roi(roi_numero, resultado_corte, key_points['numero'])
