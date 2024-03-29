from django.core.exceptions import ValidationError


def validate_title(title):
    allowed = ["-", "&", " ", "'", ",", ":"]
    for el in title:
        if not el.isalnum() and not el in allowed:
            raise ValidationError(f"Title can only contain letters, numbers and the following symbols: "
                                  f"{' '.join(el for el in allowed)}")