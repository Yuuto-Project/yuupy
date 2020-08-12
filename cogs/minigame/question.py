from marshmallow import Schema
from marshmallow_dataclass import dataclass
from typing import ClassVar, List, Type


@dataclass
class Question(object):
    type: str
    question: str
    answers: List[str]
    wrong: List[str]
    Schema: ClassVar[Type[Schema]] = Schema
