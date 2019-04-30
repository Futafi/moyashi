import difflib


def check_similarities(match_title: str, titles: str) -> list:
    """
    titleとtitleのリストを受け取りその類似度を返す。
    Parameters
    ----------
    match_title
    titles

    Returns
    -------

    """
    sim_rate_list = list()
    for title in titles:
        sim_rate_list.append(difflib.SequenceMatcher(None, match_title, title).ratio())
    return sim_rate_list
