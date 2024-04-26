from services.ocr_service import ocr
from services.rg_posprocessing import format_cpf
import re

def check_cnh_version(results):
    keywords = [
        "driver",
        "driving",
        "license",
        "permiso",
        "conducc",
        "nacionalidade",
        "conduire",
        "4a",
        "4b",
        "4c",
        "4d",
    ]
    texts = [text for _, text, _ in results]
    for keyword in keywords:
        if any(keyword in word.lower() for word in texts):
            return "new"
    return "old"


def cnh_keypoints(version):
    if version == "new":
        key_points = {
            'name': (210, 230),
            'rg': (510, 410),
            'cpf': (520, 470),
            'birth': (510, 290),
            'number': (0, 104),
            'registration': (740, 470),
        }
    else:
        key_points = {
            'name': (200, 200),
            'rg': (550, 280),
            'cpf': (550, 380),
            'birth': (880, 380),
            'number': (0, 104),
            'registration': (230, 750),
        }
    return key_points


def validate_cnh_name(image, top_left, w, h, text):
    """
    Validate the extracted name from CNH.

    Args:
        image: Aligned document image after preprocessing.
        top_left: Top-left corner coordinates of the extracted name region.
        w: Width of the extracted name region.
        h: Height of the extracted name region.
        text: Extracted text containing the name.

    Returns:
        validated_name: Validated and formatted name string.
    """
    # Split the string by whitespaces
    parts = text.strip().split()
    # Count the number of words in the string
    num_names = len(parts)
    # Check if there is more than one name
    if num_names > 2:
        return text.upper()
    elif num_names == 2:
        new_roi = image[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 3 * w
        ]
    else:
        new_roi = image[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 5 * w
        ]
    name_result = ocr(new_roi)
    full_name = " ".join(
        [name for _, name, _ in name_result]
    )
    return full_name.upper()


def validate_cnh_rg(image, top_left, w, h, text):
    """
    Validate the extracted RG and issuer from CNH.

    Args:
        image: Aligned document image after preprocessing.
        top_left: Top-left corner coordinates of the extracted RG region.
        w: Width of the extracted RG region.
        h: Height of the extracted RG region.
        text: Extracted text containing the RG and issuer information.

    Returns:
        rg: Validated RG number string.
        issuer: Issuer information string.
        state: State abbreviation string.
    """
    if text[-1].isalpha():
        pass
    else:
        new_roi = image[
            top_left[1] : top_left[1] + h + 10, top_left[0] : top_left[0] + 460
        ]
        rg_result = ocr(new_roi)
        text = " ".join(
            [character for _, character, confidence in rg_result if confidence > 0.3]
        )
    rg = re.findall(r'\d+', text)
    rg = ''.join(rg)
    issuer_state = re.findall(r'[a-zA-Z]+', text)
    if len(issuer_state) == 1:
        issuer, state = issuer_state[0][:-2], issuer_state[0][-2:]
    else:
        issuer, state = issuer_state[0], issuer_state[1]
    return rg, issuer, state


def validate_cnh_cpf(image, top_left, w, h, cpf_number):
    """
    Validate the extracted CPF from CNH.

    Args:
        image: Aligned document image after preprocessing.
        top_left: Top-left corner coordinates of the extracted CPF region.
        w: Width of the extracted CPF region.
        h: Height of the extracted CPF region.
        cpf_number: Extracted CPF number.

    Returns:
        validated_cpf: Validated and formatted CPF string.
    """
    size = len("".join(char for char in cpf_number if char.isdigit()))
    if size == 11:
        return format_cpf(cpf_number)
    else:
        new_roi = image[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 270
        ]
        cpf_result = ocr(new_roi)
        full_cpf = ".".join(
            [digit for _, digit, confidence in cpf_result if confidence > 0.3]
        )
        return format_cpf(full_cpf) if len(full_cpf) >= 11 else full_cpf


def validate_cnh_birth_date(image, top_left, w, h, date):
    """
    Validate the extracted birth date from CNH.

    Args:
        image: Aligned document image after preprocessing.
        top_left: Top-left corner coordinates of the extracted birth date region.
        w: Width of the extracted birth date region.
        h: Height of the extracted birth date region.
        date: Extracted birth date string.

    Returns:
        validated_date: Validated and formatted birth date string.
    """
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    
    if re.match(pattern, date):
        return date
    else:
        parts = date.strip().split()
        quantity = len(parts)
    
    if quantity > 1:
        if re.match(pattern, parts[0]):
            return parts[0]
        elif re.match(pattern, parts[-1]):
            return parts[-1]
    else:
        new_roi = image[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] :
        ]
        date_result = ocr(new_roi)
        date = "".join([character for _, character, confidence in date_result if confidence > 0.3])
        date = re.sub(r'[^0-9\/]', '', date)
        if len(date) > 10:
            return date[len(date)-10:]
        else:
            return date
