from data.tldr.make_tldr_helpers import tl_dr, get_all_tldr, iter_tldr, botlist
from data.tldr.clean_tldr_python import clean_tldr_text

VALID_TLDRS = ["tl dr", "tl;dr", "tldr", "tl:dr", "tl/dr", "tl; dr", "tl,dr", "tl, dr", "tl-dr", "tl'dr", "tl: dr", "tl.dr", "tl ; dr", "tl_dr", "tldr;dr", "tl ;dr",
               "tl\"dr", "tl/ dr", "tld:dr", "tl;;dr", "tltl;dr", "tl~dr", "tl / dr", "tl :dr", "tl - dr", "tl\\dr", "tl. dr", "tl:;dr", "tl|dr", "tl;sdr", "tll;dr", "tl : dr", "tld;dr"]


def get_tldr_and_clean_text(subm):
    cleaned_dict = clean_tldr_text(subm.selftext)
    cleaned_text = cleaned_dict["clean_text_for_tldr"]
    all_tldrs = get_all_tldr(cleaned_text)
    content_and_summary = iter_tldr(cleaned_text)
    if content_and_summary is not None:
        content = content_and_summary[0]
        summary = content_and_summary[1]
    else:
        content = summary = None
    # TODO: check how well this works on shorted TLDR posts (when content in link)
    tldr_dict = {
        "is_bot": subm.author in botlist,
        "tldr_preset": tl_dr(cleaned_text),
        "num_tldrs": len(all_tldrs),
        "tldr_content": content,
        "tldr_summary": summary,
        "is_invalid_tldr_pattern":  all([tldr in VALID_TLDRS
                                         for tldr in all_tldrs])
    }
    tldr_dict.update(cleaned_dict)
    return tldr_dict
