def paginate(offset: int, limit: int, count: int):
    limit = limit or 10

    next_offset = offset + limit
    next_limit = limit

    if next_offset >= count:
        next_offset = None

    prev_offset = offset - limit
    prev_limit = limit

    if prev_offset < 0:
        prev_limit += prev_offset
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