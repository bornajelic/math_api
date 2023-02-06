from pydantic import BaseModel


class InputData(BaseModel):
    """Pydantic class used for type and validation checks

    Args:
        BaseModel (_type_): Child class of Pydantic Base Model

    Raises:
        ValueError: if any of the arguments are not float or int
    """

    x: float
    y: float


class ResponseModel(BaseModel):
    """Pydantic class used for type and validation checks. Represents a response model"""

    action: str
    x: float
    y: float
    answer: float
    cached: str


class AddData(InputData):
    @property
    def key(self) -> str:
        if self.x > self.y:
            # commutative operation: always set x to be less than y so that we can generate the same key
            # ex: 20 + 5  =  5 + 20
            return str(self.y) + "+" + str(self.x)
        return str(self.x) + "+" + str(self.y)


class MultiplyData(InputData):
    @property
    def key(self) -> str:
        if self.x > self.y:
            # commutative operation: always set x to be less than y so that we can generate the same key
            # ex: 20 * 5  =  5 * 20
            return str(self.y) + "*" + str(self.x)
        return str(self.x) + "*" + str(self.y)


class SubtractData(InputData):
    @property
    def key(self) -> str:
        return str(self.x) + "-" + str(self.y)


class DivideData(InputData):
    @property
    def key(self) -> str:
        return str(self.x) + "/" + str(self.y)
