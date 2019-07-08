import json
from settings import REDDIT_TLDR_TABLE_FROM_COMPETITION, ENGINE_PATH
from sqlalchemy import create_engine
import pandas as pd

class SplittingUpLargeJson():

    def __init__(self,
                 orig_json_path,
                 new_files_path,
                 table_name,
                 engine_path=ENGINE_PATH,
                 replace_init=True):
        self.new_files_path = new_files_path
        self.table_name = table_name
        self.orig_json_path = orig_json_path
        self.row_num = 0
        self.engine = create_engine(engine_path)
        self.replace_init = replace_init

    def save_row_to_json(self, row):
        new_fp = self.new_files_path + "_row_" + str(self.row_num) + ".json"
        with open(new_fp, "w") as fnew:
            json.dump(row, fnew)

    def save_row_to_db(self, row, replace):
        if replace:
            if_exists = "replace"
        else:
            if_exists = "append"
        df = pd.DataFrame([row])
        if replace:
            self.cols = df.columns
        else:
            df = df[self.cols]
        df.to_sql(self.table_name,
                  self.engine, if_exists=if_exists)

    def save_json_per_line(self):
        with open(self.orig_json_path, "r") as f:
            for line in f:
                row = json.loads(line)
                self.save_row_to_json(row)
                if self.row_num == 0:
                    replace = self.replace_init
                else:
                    replace = False
                self.save_row_to_db(row, replace)
                if self.row_num % 10000 == 0:
                    print("on row number = " + str(self.row_num))
                self.row_num += 1


if __name__ == "__main__":
    from settings import RAW_REDDIT_JSON_PATH
    json_splitter = SplittingUpLargeJson(
        "/scratch/gobi2/bparker/summarization_data/interim/reddit/tldr/corpus-webis-tldr-17/orig_one_large_json/corpus-webis-tldr-17.json",
        RAW_REDDIT_JSON_PATH,
        REDDIT_TLDR_TABLE_FROM_COMPETITION
    )
    json_splitter.save_json_per_line()
