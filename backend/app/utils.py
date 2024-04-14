def is_valid_isbn(isbn):

    isbn = isbn.replace("-", "").replace(" ", "")

    print(isbn)

    if len(isbn) not in (10, 13):
        return False

    if len(isbn) == 10:
        try:
            digits = [int(x) if x.isdigit() else 10 for x in isbn]
            check_sum = sum(weight * digit for weight, digit in enumerate(digits[::-1], start=1))
            return check_sum % 11 == 0
        except ValueError:
            return False

    elif len(isbn) == 13:
        try:
            if not isbn.startswith("978"):
                return False
            digits = [int(x) if x.isdigit() else 10 for x in isbn]

            check_sum = sum((3 if weight % 2 else 1) * digit for weight, digit in enumerate(digits))
            return check_sum % 10 == 0
        except ValueError:
            return False

    return False
