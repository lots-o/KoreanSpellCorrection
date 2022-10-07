import re
import random

import soynlp.hangle as hangle
from g2pk import G2p

# 초성
onset_list = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

# 중성
nucleus_list = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

# 종성
coda_list = [
    " ",
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

# 자음
consonant_list = [
    "ㄱ",
    "ㄲ",
    "ㄳ",
    "ㄴ",
    "ㄵ",
    "ㄶ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㄺ",
    "ㄻ",
    "ㄼ",
    "ㄽ",
    "ㄾ",
    "ㄿ",
    "ㅀ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅄ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

# 모음
vowel_list = [
    "ㅏ",
    "ㅐ",
    "ㅑ",
    "ㅒ",
    "ㅓ",
    "ㅔ",
    "ㅕ",
    "ㅖ",
    "ㅗ",
    "ㅘ",
    "ㅙ",
    "ㅚ",
    "ㅛ",
    "ㅜ",
    "ㅝ",
    "ㅞ",
    "ㅟ",
    "ㅠ",
    "ㅡ",
    "ㅢ",
    "ㅣ",
]

# 중성 동음이자(Heterograph)
nucleus_sim_syl_dict = {
    "ㅔ": ("ㅐ",),
    "ㅐ": ("ㅔ",),
    "ㅖ": ("ㅒ",),
    "ㅒ": ("ㅖ",),
    "ㅚ": ("ㅞ", "ㅙ"),
    "ㅞ": ("ㅚ", "ㅙ"),
    "ㅙ": ("ㅚ", "ㅞ"),
}


# 종성 동음이자(Heterograph)
coda_sim_syl_dict = {
    "ㅂ": ("ㅍ",),
    "ㅍ": ("ㅂ",),
    "ㅅ": ("ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㅆ": ("ㅅ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㄷ": ("ㅅ", "ㅆ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㅌ": ("ㅅ", "ㅆ", "ㄷ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㅈ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅊ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㅊ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅎ", "ㄱ", "ㄲ", "ㅋ"),
    "ㅎ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㄱ", "ㄲ", "ㅋ"),
    "ㄱ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄲ", "ㅋ"),
    "ㄲ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㅋ"),
    "ㅋ": ("ㅅ", "ㅆ", "ㄷ", "ㅌ", "ㅈ", "ㅊ", "ㅎ", "ㄱ", "ㄲ"),
}

# TODO
def punctuation_noise():
    pass


def grapheme_to_phoneme_noise(sent: str, noise_ratio: float = 0.3, *args, **kwargs) -> str:
    """
    텍스트를 읽었을 때 생길 수 있는 발음 노이즈
    """
    if random.random() < noise_ratio:
        g2p = G2p()
        return g2p(sent, *args, **kwargs)

    else:
        return sent


# TODO
def heuristic_noise():
    pass


def sim_syllable_noise(sent: str, syl: str = "nucleus", noise_ratio: float = 0.3) -> str:
    """
    문장 각 문자의 중성 or 종성의 동음이자(Heterograph) 노이즈.
    """
    assert syl in ["nucleus", "coda"]

    noise_sent = ""

    for ch in sent:
        if hangle.character_is_complete_korean(ch) and random.random() < noise_ratio:
            onset, nucleus, coda = hangle.decompose(ch)

            if syl == "nucleus":  # 중성 noise
                sim_syl = nucleus_sim_syl_dict.get(nucleus, False)
                if sim_syl:
                    idx = random.randint(0, len(sim_syl) - 1)
                    nucleus = sim_syl[idx]

            else:  # 종성 노이즈
                sim_syl = coda_sim_syl_dict.get(coda, False)
                if sim_syl:
                    idx = random.randint(0, len(sim_syl) - 1)
                    coda = sim_syl[idx]

            noise_sent += hangle.compose(onset, nucleus, coda)

        else:
            noise_sent += ch

    return noise_sent


def spacing_noise(sent: str, noise_ratio: float = 0.3) -> str:
    """
    랜덤하게 공백 추가/삭제 노이즈
    """
    noise_sent = ""
    doublespace_pattern = "\s+"

    for ch in sent:
        if random.random() < noise_ratio:
            if ch == " " and random.random() < noise_ratio:  # 공백 제거
                noise_sent += ""

            else:  # 공백 추가
                noise_sent += " " + ch
        else:
            noise_sent += ch

    noise_sent = re.sub(doublespace_pattern, " ", noise_sent).strip()

    return noise_sent
