from services.rg_posprocessing import *
from services.ocr_service import extract_roi

def rg_detection(aligned, results):
    """
    Detect and extract information from RG (identity card).

    Args:
        aligned: Aligned document image after preprocessing.
        results: OCR results containing text and bounding boxes.

    Returns:
        rg_data: Extracted RG information including name, RG number, CPF, and birth date.
    """
    rg_data = {}

    key_points = {
            'name': (100, 180),
            'rg': (230, 100),
            'cpf': (100, 615),
            'birth_date': (840, 440),
            }

    roi_name, tl_name, width_name, height_name, name = extract_roi(aligned, results, key_points['name'], data_type='varchar')
    rg_data['nome'] = validate_rg_name(aligned, tl_name, width_name, height_name, name)

    roi_rg, tl_rg, width_rg, height_rg, rg_number = extract_roi(aligned, results, key_points['rg'])    
    rg_data['rg'] = validate_rg(aligned, tl_rg, width_rg, height_rg, rg_number)

    roi_cpf, tl_cpf, width_cpf, height_cpf, cpf = extract_roi(aligned, results, key_points['cpf'])    
    rg_data['cpf'] = validate_cpf_rg(aligned, tl_cpf, width_cpf, height_cpf, cpf)

    roi_birth_date, tl_birth_date, width_birth_date, height_birth_date, birth_date = extract_roi(aligned, results, key_points['birth_date'])
    rg_data['data de nascimento'] = validate_birth_date_rg(aligned, tl_birth_date, width_birth_date, height_birth_date, birth_date)

    return rg_data
