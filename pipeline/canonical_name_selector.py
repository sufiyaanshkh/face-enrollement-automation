from collections import Counter


def select_canonical_name(items):
    """Suggest a canonical name from cleaned filename variants.

    Longer multi-word names receive a modest preference, but ambiguous clusters
    are returned with all variants so they can be reviewed.
    """
    names = [item.get('cleaned_name', '').strip() for item in items]
    names = [name for name in names if name]

    if not names:
        return 'UNKNOWN_PERSON', [], True

    counts = Counter(names)
    scores = {}
    for name, frequency in counts.items():
        words = len(name.split())
        scores[name] = frequency * 10 + words * 3 + len(name) * 0.05

    ranked = sorted(scores, key=scores.get, reverse=True)
    canonical = ranked[0]
    variants = sorted(counts)

    # Different variants are useful, but automatic naming should be reviewed
    # whenever the cluster contains substantially different names.
    needs_name_review = len(variants) > 1
    return canonical, variants, needs_name_review
