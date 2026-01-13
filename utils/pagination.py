def paginate(fetch_items, fetch_total, **kwargs):
    """
    Generic pagination function.
    fetch_items: function to fetch items, should accept **kwargs like limit, offset, etc.
    fetch_total: function to fetch total count, should accept search params but not limit/offset.
    Returns a dict with items, total, offset, limit, count (which is len(items))
    """
    items = fetch_items(**kwargs)
    # Remove limit and offset for fetch_total as they don't need them
    total_kwargs = {k: v for k, v in kwargs.items() if k not in ('limit', 'offset')}
    total = fetch_total(**total_kwargs)
    offset = kwargs.get('offset', 0)
    limit = kwargs.get('limit', 10)
    return {
        "items": items,
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }
