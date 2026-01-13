def paginate(fetch_items, fetch_total, **kwargs):
    """
    Generic pagination function.
    fetch_items: function to fetch items, should accept **kwargs like limit, offset, etc.
    fetch_total: function to fetch total count, should accept **kwargs like keyword, etc.
    Returns a dict with items, total, offset, limit, count (which is len(items))
    """
    items = fetch_items(**kwargs)
    total = fetch_total(**kwargs)
    offset = kwargs.get('offset', 0)
    limit = kwargs.get('limit', 10)
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }
