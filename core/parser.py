import os
import json
import glob

from dataclasses import asdict

from log import logged
from dataclass import GrammarCorrectionColumn, NewsPaperColumn


@logged
class CorpusKoreanJsonParser:
    def __init__(self, input_dir: str, output_dir: str) -> None:
        self.input_dir = input_dir
        self._create_output_dir(output_dir)
        self._load_data()

    def _load_data(self) -> None:

        self.__log.info(f"Parsing input dir:: {self.input_dir}")
        input_paths = os.path.join(self.input_dir, "*.json")
        self.__log.info(f"Load data :: {input_paths}")
        self.fname2file = dict()

        for input_path in glob.glob(input_paths):
            _, fname = os.path.split(input_path)
            self.fname2file[fname] = open(input_path, "r")

    def _create_output_dir(self, output_dir) -> None:
        self.output_dir = os.path.join(output_dir, os.path.split(self.input_dir)[1])
        if not os.path.exists(self.output_dir):
            self.__log.info(f"Create parsing output dir :: {self.output_dir }")
            os.makedirs(self.output_dir)
        else:
            self.__log.info(f"Output dir exists :: {self.output_dir }")

    def __del__(self):
        self.__log.info("Closing file object ")
        for file in self.fname2file.values():
            file.close()

    def run(self) -> None:
        raise NotImplementedError


@logged
class GrammarCorrectionJsonParser(CorpusKoreanJsonParser):
    """
    국립 국어원 맞춤법 교정 말뭉치 v1.0 에서 utterance 또는 paragraph 정보만 파싱
    - NIKL_SC_2021_v1.0
        - MXSC2102112091.json  -> utterance
        - EXSC2102112091.json  -> paragraph
    """

    def run(self) -> None:

        for fname, f in self.fname2file.items():
            output_path = os.path.join(self.output_dir, fname)
            writer = open(output_path, "w")
            count = 0

            json_data = json.load(f)
            for row in json_data["document"]:
                for target in row["paragraph"] if row.get("paragraph", None) else row["utterance"]:
                    data = GrammarCorrectionColumn(
                        id=target["id"],
                        original_form=target["original_form"],
                        corrected_form=target["corrected_form"],
                    )
                    json.dump(asdict(data), writer, ensure_ascii=False)  # ensure_ascii =  한글 unicode
                    writer.write("\n")
                    count += 1

            writer.close()
            self.__log.info(f"Parsing data :: {fname}:: |data| = {count}")


@logged
class NewsPaperJsonParser(CorpusKoreanJsonParser):
    """
    국립 국어원 신문 말뭉치 v2.0 에서 paragraph 정보만 파싱
    - NIKL_NEWSPAPER_v2.0
        - NIRW1900000001.json ~ NIRW1900000030.json
        - NLRW1900000001.json ~ NLRW1900000161.json
        - NPRW1900000001.json ~ NPRW1900000069.json
        - NWRW1800000001.json ~ NWRW1800000056.json
        - NWRW1900000001.json ~ NWRW1900000060.json
        - NZRW1900000001.json
    """

    def run(self) -> None:

        for fname, f in self.fname2file.items():
            output_path = os.path.join(self.output_dir, fname)
            writer = open(output_path, "w")
            count = 0

            json_data = json.load(f)
            for row in json_data["document"]:
                for target in row["paragraph"]:
                    data = NewsPaperColumn(
                        id=target["id"],
                        form=target["form"],
                    )
                    json.dump(asdict(data), writer, ensure_ascii=False)  # ensure_ascii =  한글 unicode
                    writer.write("\n")
                    count += 1
            writer.close()
            self.__log.info(f"Parsing data :: {fname}:: |data| = {count}")


if __name__ == "__main__":

    grammar_input_dir = "./data/raw/NIKL_SC_2021_v1.0"
    news_input_dir = "./data/raw/NIKL_NEWSPAPER_v2.0"
    output_dir = "./data/parsing"

    GrammarCorrectionJsonParser(grammar_input_dir, output_dir).run()
    NewsPaperJsonParser(news_input_dir, output_dir).run()
