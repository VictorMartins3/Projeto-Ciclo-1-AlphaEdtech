from services.ocr_service import ocr
import re


def validate_rg_name(image, top_left, w, h, text):
    """
    Validate the extracted name from an RG (identity card).

    Args:
        image: Document image.
        top_left: Top-left corner coordinates of the name region.
        w: Width of the name region.
        h: Height of the name region.
        text: Extracted text containing the name.

    Returns:
        validated_name: Validated and formatted name.
    """
    # Split the text by whitespace
    parts = text.strip().split()
    # Count the number of words in the text
    num_names = len(parts)
    # Check if there are more than two names
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
    result_name = ocr(new_roi)
    full_name = " ".join(
        [name for _, name, confidence in result_name if confidence > 0.3]
    )
    return full_name.upper()


def validate_rg(image, top_left, w, h, text):
    """
    Validate the extracted RG (identity card) number.

    Args:
        image: Document image.
        top_left: Top-left corner coordinates of the RG region.
        w: Width of the RG region.
        h: Height of the RG region.
        text: Extracted text containing the RG number.

    Returns:
        validated_rg: Validated and formatted RG number.
    """
    if text[-1].isalpha():
        rg = re.findall(r'\d', text)
        rg = ''.join(rg)
        return rg
    else:
        if len(text) >= 9:
            return text.replace(" ","")
        else:
            new_roi = image[
                top_left[1] - 10 : top_left[1] + h + 10, top_left[0] : top_left[0] + 310
            ]
            result_rg = ocr(new_roi)
            text = "".join(
                [char for _, char, confidence in result_rg if confidence > 0.3]
            )
            return text.replace(" ","")


def validate_cpf_rg(image, top_left, w, h, cpf_number):
    """
    Validate and format the extracted CPF (Brazilian ID number) or RG (identity card) number.

    Args:
        image: Document image.
        top_left: Top-left corner coordinates of the CPF/RG region.
        w: Width of the CPF/RG region.
        h: Height of the CPF/RG region.
        cpf_number: Extracted CPF/RG number.

    Returns:
        validated_number: Validated and formatted CPF/RG number.
    """
    size = len("".join(char for char in cpf_number if char.isdigit()))
    if size == 11:
        return format_cpf(cpf_number)
    else:
        new_roi = image[
            top_left[1] - 10 : top_left[1] + h + 10, top_left[0] - 100 : top_left[0] + 300
        ]
        result_cpf = ocr(new_roi)
        full_cpf = ".".join(
            [digit for _, digit, confidence in result_cpf if confidence > 0.3]
        )
        return format_cpf(full_cpf) if len(full_cpf) >= 11 else full_cpf


def format_cpf(cpf):
    """
    Format the CPF (Brazilian ID number) to the standard format.

    Args:
        cpf: CPF number.

    Returns:
        formatted_cpf: Formatted CPF number.
    """
    if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return cpf
    else:
        numbers_only = re.sub(r'\D', '', cpf)
        formatted_cpf = '{}.{}.{}-{}'.format(numbers_only[:3], numbers_only[3:6], numbers_only[6:9], numbers_only[9:])
        return formatted_cpf


def validate_birth_date_rg(image, top_left, w, h, date):
    """
    Validate the birth date extracted from an RG (Brazilian ID card).

    Args:
        image: Image containing the RG.
        top_left: Coordinates of the top-left corner of the region of interest.
        w: Width of the region of interest.
        h: Height of the region of interest.
        date: Extracted birth date.

    Returns:
        validated_date: Validated birth date.
    """
    date = date.replace(" ","")
    if re.search(r'\b[A-Z]{3}\b', date) and date.count('/') == 2:
        date = format_date(date)

    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(pattern, date):
        return date
    else:
        length = len(date)
        if length < 10:     
            new_roi = image[
                top_left[1] - 10 : top_left[1] + h + 10, top_left[0]: top_left[0] + 300
            ]
            result_date = ocr(new_roi)
            date = "".join([char for _, char, confidence in result_date if confidence > 0.3])
            return date
        else:
            return date

            
def format_date(date):
    """
    Adjust the date format from an abbreviated month to a numeric month.

    Args:
        date: Date string to be adjusted.

    Returns:
        adjusted_date: Date string with the format 'dd/mm/yyyy'.
    """
    months = {
        'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04', 'MAI': '05', 'JUN': '06',
        'JUL': '07', 'AGO': '08', 'SET': '09', 'OUT': '10', 'NOV': '11', 'DEZ': '12'}
    
    day, month_abbreviated, year = date.split('/')
    numeric_month = months[month_abbreviated.upper()]
    adjusted_date = f"{day}/{numeric_month}/{year}"
    return adjusted_date