
def rank_candidates(candidate_results: list[dict]) -> list[dict]:
    """
    Rank candidates based on their overall evaluation scores.

    Candidates with equal scores receive the same rank.
    The next rank is skipped accordingly (e.g., 1, 1, 3).
    """

    if not candidate_results:
        return []

    # Sort candidates by overall score in descending order.
    sorted_candidates = sorted(
        candidate_results,
        key=lambda candidate: candidate.get("overall_score", 0),
        reverse=True
    )

    ranked_candidates = []
    previous_score = None
    current_rank = 0

    for position, candidate in enumerate(sorted_candidates, start=1):
        score = candidate.get("overall_score", 0)

        # Assign the same rank to candidates with equal scores.
        if score != previous_score:
            current_rank = position

        ranked_candidate = candidate.copy()
        ranked_candidate["rank"] = current_rank

        ranked_candidates.append(ranked_candidate)
        previous_score = score

    return ranked_candidates
