from django.core.exceptions import ValidationError

def validate_imei(value: str):
    """
    Validate IMEI using Luhn algorithm.
    Must be 15 digits and pass checksum.
    """
    if not value.isdigit() or len(value) != 15:
        raise ValidationError("IMEI must be 15 digits")

    digits = [int(d) for d in value]
    total = 0
    for i, d in enumerate(digits[:-1]):  # last digit is checksum
        if i % 2 == 1:  # double every 2nd digit
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check_digit = (10 - (total % 10)) % 10

    if check_digit != digits[-1]:
        raise ValidationError("Invalid IMEI checksum")
