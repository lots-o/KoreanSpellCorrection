from dataclasses import dataclass


@dataclass
class GrammarCorrectionColumn:
    """
    국립 국어원 맞춤법 교정 말뭉치 v1.0
    """

    id: str = ""
    original_form: str = ""
    corrected_form: str = ""


@dataclass
class NewsPaperColumn:
    """
    국립 국어원 신문 말뭉치 v2.0
    """

    id: str = ""
    form: str = ""
