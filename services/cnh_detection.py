from services.cnh_posprocessing import *
from services.ocr_service import extract_roi, crop_rotate, ocr


def cnh_detection(aligned, results):
    """
    Extract information from aligned document image for Brazilian Driver's License (CNH).

    Args:
        aligned: Aligned document image after preprocessing.
        results: OCR results containing detected text and associated bounding boxes.

    Returns:
        cnh_data: Dictionary containing extracted CNH information.
    """
    cnh_data = {}

    # Extract CNH version
    cnh_data["versao"] = check_cnh_version(results)
    key_points = cnh_keypoints(cnh_data["versao"])

    # Extract name from CNH
    roi_name, tp_name, width_name, height_name, name = extract_roi(
        aligned, results, key_points["name"], data_type="varchar"
    )
    cnh_data["nome"] = validate_cnh_name(aligned, tp_name, width_name, height_name, name)

    # Extract RG from CNH
    roi_rg, tp_rg, width_rg, height_rg, rg = extract_roi(
        aligned, results, key_points["rg"]
    )
    cnh_data["rg"], cnh_data["emissor"], cnh_data["uf"] = validate_cnh_rg(
        aligned, tp_rg, width_rg, height_rg, rg
    )

    # Extract CPF from CNH
    roi_cpf, tp_cpf, width_cpf, height_cpf, cpf = extract_roi(
        aligned, results, key_points["cpf"]
    )
    cnh_data["cpf"] = validate_cnh_cpf(aligned, tp_cpf, width_cpf, height_cpf, cpf)

    # Extract birth date from CNH
    roi_birth_date, tp_birth_date, width_birth_date, height_birth_date, birth_date = extract_roi(
        aligned, results, key_points["birth"]
    )
    cnh_data["data de nascimento"] = validate_cnh_birth_date(
        aligned, tp_birth_date, width_birth_date, height_birth_date, birth_date
    )

    # Extract registration number from CNH
    (
        roi_registration,
        tp_registration,
        width_registration,
        height_registration,
        cnh_data["registro"],
    ) = extract_roi(aligned, results, key_points["registration"])

    # Extract side number from CNH
    roi_number = crop_rotate(aligned)
    cutting_result = ocr(roi_number)
    (
        side_number,
        tp_side,
        width_side,
        height_side,
        cnh_data["verificador"],
    ) = extract_roi(roi_number, cutting_result, key_points["number"])

    return cnh_data
