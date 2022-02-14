from pydantic import validate_arguments


@validate_arguments
def encrypt_password(password: str) -> str:
    return password + "abracadabra"

