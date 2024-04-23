import re
import bcrypt


# Validations:
def validate_email(email):
    pattern = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.match(pattern, email)


def validate_username(username):
    pattern = "^[a-zA-Z0-9]*$"
    return re.match(pattern, username)


def validate_password(password):
    return len(password) >= 6


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


def validate_name(nome):
    if 10 < len(nome) < 100:
        # Verifica se todos os caracteres são letras, espaços ou acentuações
        if all(char.isalpha() or char.isspace() for char in nome):
            return True
    return False


def validate_cpf(cpf: str) -> bool:
    # Verifica a formatação do CPF
    if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números ou se todos são iguais
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    # Validação dos dígitos verificadores
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    return True