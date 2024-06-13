from fastapi import HTTPException
from typing import List, Dict
from peewee import ModelSelect
from operator import attrgetter
from models.discussion import Discussion

def get_filters(filters: dict, query: ModelSelect, model: Discussion):
    filter_keys = list(filters.keys())
    for filter_key in filter_keys:
        filter_value = filters[filter_key]
        if isinstance(filter_value, bool):
            if filter_value:
                query = query.where(attrgetter(filter_key)(model))
            else:
                query = query.where(~attrgetter(filter_key)(model))
        elif isinstance(filter_value, (str, int)):
            if filter_value != "":
                attribute = getattr(model, filter_key)
                query = query.where(attrgetter(filter_key)(model) == filter_value)
        elif isinstance(filter_value, (list, tuple)):
            attribute = getattr(model, filter_key)
            query = query.where(attrgetter(filter_key)(model) << filter_value)
        elif filter_value is None:
            query = query.where(attrgetter(filter_key)(model) == filter_value)
    return query

def get_all_discussions(filters: Dict) -> List[Discussion]:
    try:
        query = Discussion.select()
        if filters:
            query = get_filters(filters, query, Discussion)
        return list(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
