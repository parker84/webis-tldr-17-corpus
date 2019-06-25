from data.tldr.clean_tldr_helpers import clean_text, check_english

def clean_tldr_text(text):
    cleaned = clean_text(text)
    return {
        "len_of_tldr_cleaned_text": len(cleaned.split(" ")),
        "is_english": check_english(cleaned),
        "clean_text_for_tldr": cleaned
    }
