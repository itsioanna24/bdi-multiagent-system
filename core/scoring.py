# Scoring utility for evaluating relevance of research papers

def compute_score(item, keyword):
    """
    Computes a relevance score for a given paper.

    WHY:
    - Provides more flexible filtering than binary keyword matching
    - Keeps logic reusable and separate from agent behaviour
    """

    score = 0

    # Normalise text
    summary = item.get("summary", "").lower()
    title = item.get("title", "").lower()
    keyword = keyword.lower()

    # Strong signal: keyword in summary
    if keyword in summary:
        score += 2

    # Secondary signal: keyword in title
    if keyword in title:
        score += 1

    # Bonus: multiple occurrences in summary
    if summary.count(keyword) > 1:
        score += 1

    return score