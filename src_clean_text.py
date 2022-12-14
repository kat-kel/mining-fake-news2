from sentence_splitter import SentenceSplitter


domains_not_currently_supported = ["perma.cc", "t.me"]

def clean_text(list_of_texts:list[dict]):
    raw_texts = remove_invalid_text(list_of_texts)
    return split_sentences(raw_texts)


def remove_invalid_text(list_of_texts:list[dict]):
    valid_texts = []
    for d in list_of_texts:
        if not "! d o c t y p e h t m l" in d["message"][:24]\
            and not any(domain == d["domain"] for domain in domains_not_currently_supported):
            valid_texts.append(d["message"])
    return valid_texts


def split_sentences(source_sentences:list[str]):
    splitter = SentenceSplitter(language="fr")
    return [splitter.split(post) for post in source_sentences]
