import re
from app.common.schemas.validator_types import Validator


class CPF(Validator):
    def validate(self, doc: str = "") -> bool:
        if len(doc) != 11:
            return False

        if self._check_repeated_digits(doc):
            return False

        return (
            self._generate_first_digit(doc) == doc[9]
            and self._generate_second_digit(doc) == doc[10]
        )

    def _generate_first_digit(self, doc: str) -> str:
        sum = 0

        for i in range(10, 1, -1):
            sum += int(doc[10 - i]) * i

        sum = (sum * 10) % 11

        if sum == 10:
            sum = 0

        return str(sum)

    def _generate_second_digit(self, doc: str) -> str:
        sum = 0

        for i in range(11, 1, -1):
            sum += int(doc[11 - i]) * i

        sum = (sum * 10) % 11

        if sum == 10:
            sum = 0

        return str(sum)

    def _check_repeated_digits(self, doc: str) -> bool:
        return len(set(doc)) == 1


class CNPJ(Validator):
    def __init__(self):
        self.weights_first = list(range(5, 1, -1)) + list(range(9, 1, -1))
        self.weights_second = list(range(6, 1, -1)) + list(range(9, 1, -1))

    def validate(self, doc: str = "") -> bool:
        if len(doc) != 14:
            return False

        for i in range(10):
            if doc.count(f"{i}") == 14:
                return False

        return (
            self._generate_first_digit(doc) == doc[12]
            and self._generate_second_digit(doc) == doc[13]
        )

    def _generate_first_digit(self, doc: str) -> str:
        sum = 0

        for i in range(12):
            sum += int(doc[i]) * self.weights_first[i]

        sum = sum % 11

        if sum < 2:
            sum = 0
        else:
            sum = 11 - sum

        return str(sum)

    def _generate_second_digit(self, doc: str) -> str:
        sum = 0

        for i in range(13):
            sum += int(doc[i]) * self.weights_second[i]

        sum = sum % 11

        if sum < 2:
            sum = 0
        else:
            sum = 11 - sum

        return str(sum)


class Document(Validator):
    @classmethod
    def validate(cls, doc: str) -> str:
        doc = re.sub("[^0-9]", "", doc)

        is_valid = False

        if len(doc) == 11:
            cpf = CPF()
            is_valid = cpf.validate(doc)
        elif len(doc) == 14:
            cnpj = CNPJ()
            is_valid = cnpj.validate(doc)

        if is_valid:
            return doc

        raise ValueError(f"Invalid document: {doc}")
