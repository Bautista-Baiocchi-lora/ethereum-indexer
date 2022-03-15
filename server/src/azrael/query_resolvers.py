

from typing import Callable, Dict, Optional

import pymongo
from db import DB
from tartiflette import Resolver

database_name = 'ethereum-indexer'
collection_name = '0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7-state'

db = DB()

def _remove_event_field(doc): 
    del doc['event']
    return doc

def _cast_lent_event_fields(doc):
    doc['lendingId'] = int(doc['lendingId'])
    doc['lentAmount'] = int(doc['lentAmount'])
    doc['maxRentDuration'] = int(doc['maxRentDuration'])
    doc['paymentToken'] = int(doc['paymentToken'])
    return doc

def _cast_rented_event_fields(doc):
    doc['lendingId'] = int(doc['lendingId'])
    doc['rentDuration'] = int(doc['rentDuration'])
    doc['rentedAt'] = int(doc['rentedAt'])
    return doc

def _cast_returned_event_fields(doc):
    doc['lendingId'] = int(doc['lendingId'])
    doc['returnedAt'] = int(doc['returnedAt'])
    return doc

def _cast_lending_stopped_event_fields(doc):
    doc['lendingId'] = int(doc['lendingId'])
    doc['stoppedAt'] = int(doc['stoppedAt'])
    return doc

def _cast_collateral_claimed_event_fields(doc):
    doc['lendingId'] = int(doc['lendingId'])
    doc['claimedAt'] = int(doc['claimedAt'])
    return doc
    
def _parse_id(doc):
    id = doc['_id'].split('_')
    doc['tx_hash'] = id[0]
    doc['tx_offset'] = id[1]

    del doc['_id']
    return doc

_transform_lent_event = lambda doc: _remove_event_field(_cast_lent_event_fields(_parse_id(doc)))

_transform_rented_event = lambda doc: _remove_event_field(_cast_rented_event_fields(_parse_id(doc)))

_transform_returned_event = lambda doc: _remove_event_field(_cast_returned_event_fields(_parse_id(doc)))

_transform_lending_stopped_event = lambda doc: _remove_event_field(_cast_lending_stopped_event_fields(_parse_id(doc)))

_transform_collateral_claimed_event = lambda doc: _remove_event_field(_cast_collateral_claimed_event_fields(_parse_id(doc)))

async def resolve_event(name: str, args: Dict, transformer: Callable, sort_by: Optional[str] = 'lendingId'):
    """
    Resolve event
    """

    limit = args['limit']
    order = pymongo.ASCENDING if args['ascending'] else pymongo.DESCENDING

    query  = {'event': name}
    sort = [(sort_by, order)]

    # lendingId is stored as a String but we want to sort it as a number
    collation = {'locale': 'en', 'numericOrdering': True}

    options = {'query': query, 'sort': sort, 'collation': collation}

    result  = await db.get_all_items(database_name, collection_name, limit, options)

    return list(map(transformer, result))

@Resolver("Query.getLentEvents")
async def resolve_get_lent_events(parent, args, ctx, info):
    """
    Get all lent events
    """

    return await resolve_event('Lent', args, _transform_lent_event)



@Resolver("Query.getRentedEvents")
async def resolve_get_rented_events(parent, args, ctx, info):
    """
    Get all rented events
    """
    return await resolve_event('Rented', args, _transform_rented_event)


@Resolver("Query.getReturnedEvents")
async def resolve_get_rented_events(parent, args, ctx, info):
    """
    Get all returned events
    """

    return await resolve_event('Returned', args, _transform_returned_event)


@Resolver("Query.getLendingStoppedEvents")
async def resolve_get_rented_events(parent, args, ctx, info):
    """
    Get all lending stopped events
    """

    return await resolve_event('LendingStopped', args, _transform_lending_stopped_event)


@Resolver("Query.getCollateralClaimedEvents")
async def resolve_get_rented_events(parent, args, ctx, info):
    """
    Get all collateral claimed events
    """

    return await resolve_event('CollateralClaimed', args, _transform_collateral_claimed_event)
