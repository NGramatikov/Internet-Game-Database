from django.core.exceptions import ValidationError


def validate_name(name):
    allowed = ["-", "&", " ", "!", "?", "'", ".", ",", ":"]

    for el in name:
        if not el.isalnum() and not el in allowed:
            raise ValidationError(f"Name can only contain letters, numbers and the following symbols: "
                                  f"{' '.join(el for el in allowed)}")
