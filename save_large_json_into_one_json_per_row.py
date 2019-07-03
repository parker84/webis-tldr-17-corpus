import json


def save_json_per_line(path, new_files_path):
    row_num = 1
    with open(path, "r") as f:
        for line in f:
            row = json.loads(line)
            new_fp = new_files_path + "_row_" + str(row_num) + ".json"
            with open(new_fp, "w") as fnew:
                json.dump(row, fnew)
            row_num += 1
            if row_num % 10000 == 0:
                print("on row number = " + str(row_num))


if __name__ == "__main__":
    from settings import RAW_REDDIT_JSON_PATH
    save_json_per_line( 
        "/scratch/gobi1/bparker/summarization_data/interim/reddit/tldr/corpus-webis-tldr-17.json",
        RAW_REDDIT_JSON_PATH
    )
