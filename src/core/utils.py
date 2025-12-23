def paginate(offset: int, limit: int, count: int):
    # Normalize limit
    limit = limit or 10

    # NEXT
    next_offset = offset + limit
    next_limit = limit

    if next_offset >= count:
        next_offset = None

    # PREVIOUS
    prev_offset = offset - limit
    prev_limit = limit

    if prev_offset < 0:
        prev_limit += prev_offset  # shrink limit
        prev_offset = 0

    if offset == 0:
        prev_offset = None
        prev_limit = None

    return {
        "next": (
            {"offset": next_offset, "limit": next_limit}
        ),
        "previous": (
            {"offset": prev_offset, "limit": prev_limit}
        ),
    }