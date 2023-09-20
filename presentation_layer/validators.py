from presentation_layer.errors import (InvalidChoiceNumberError,
                                       InvalidChoiceTypeError,
                                       InvalidNumberTypeError)


def validate_choice(choice: str, start: int, stop: int) -> None:
    """To validate a user choice."""

    if not choice.isdigit():
        raise InvalidChoiceTypeError("Your choice must be an integer.")
    if int(choice) not in range(start, stop + 1):
        raise InvalidChoiceNumberError(
            f"Invalid number of choice. Your choice should be from {start} to {stop}."
        )


def validate_contract_number(data: str) -> None:
    """To validate a contract number."""

    if not data.isdigit():
        raise InvalidNumberTypeError("The number of contract must be an integer.")
