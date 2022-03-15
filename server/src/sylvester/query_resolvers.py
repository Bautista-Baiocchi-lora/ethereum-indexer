from typing import Callable, Dict, Optional

import pymongo
from db import DB
from tartiflette import Resolver

database_name = 'ethereum-indexer'
collection_name = '0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a-state'

db = DB()


def _remove_event_field(doc): 
    del doc['event']
    return doc

def _cast_lend_event_fields(doc):
    doc['lendingID'] = int(doc['lendingID'])
    doc['lendAmount'] = int(doc['lendAmount'])
    doc['maxRentDuration'] = int(doc['maxRentDuration'])
    doc['paymentToken'] = int(doc['paymentToken'])
    return doc

def _cast_rented_event_fields(doc):
    doc['lendingID'] = int(doc['lendingID'])
    doc['rentingID'] = int(doc['rentingID'])
    doc['rentAmount'] = int(doc['rentAmount'])
    doc['rentDuration'] = int(doc['rentDuration'])
    doc['rentedAt'] = int(doc['rentedAt'])
    return doc

def _cast_stop_rent_event_fields(doc):
    doc['rentingID'] = int(doc['rentingID'])
    doc['stoppedAt'] = int(doc['stoppedAt'])
    return doc

def _cast_stop_lend_event_fields(doc):
    doc['lendingID'] = int(doc['lendingID'])
    doc['stoppedAt'] = int(doc['stoppedAt'])
    return doc
    
def _cast_rent_claimed_event_fields(doc):
    doc['rentingID'] = int(doc['rentingID'])
    doc['collectedAt'] = int(doc['collectedAt'])
    return doc

def _parse_id(doc):
    id = doc['_id'].split('_')
    doc['tx_hash'] = id[0]
    doc['tx_offset'] = id[1]

    del doc['_id']
    return doc

_transform_lend_event = lambda doc: _remove_event_field(_cast_lend_event_fields(_parse_id(doc)))

_transform_rent_event = lambda doc: _remove_event_field(_cast_rented_event_fields(_parse_id(doc)))

_transform_stop_rent_event = lambda doc: _remove_event_field(_cast_stop_rent_event_fields(_parse_id(doc)))

_transform_stop_lend_event = lambda doc: _remove_event_field(_cast_stop_lend_event_fields(_parse_id(doc)))

_transform_rent_claimed_event = lambda doc: _remove_event_field(_cast_rent_claimed_event_fields(_parse_id(doc)))

async def resolve_event(name: str, args: Dict, transformer: Callable, sort_by: Optional[str] = 'lendingID'):
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



@Resolver("Query.getLendEvents")
async def resolve_get_lent_events(parent, args, ctx, info):
    """
    Get all lent events
    """

    return await resolve_event('Lend', args, _transform_lend_event)


@Resolver("Query.getRentEvents")
async def resolve_get_rent_events(parent, args, ctx, info):
    """
    Get all rent events
    """

    return await resolve_event('Rent', args, _transform_rent_event)



@Resolver("Query.getStopRentEvents")
async def resolve_get_rent_events(parent, args, ctx, info):
    """
    Get all stop rent events
    """

    return await resolve_event('StopRent', args, _transform_stop_rent_event, sort_by = 'rentingID')


@Resolver("Query.getStopLendEvents")
async def resolve_get_rent_events(parent, args, ctx, info):
    """
    Get all stop lend events
    """

    return await resolve_event('StopLend', args, _transform_stop_lend_event)



@Resolver("Query.getRentClaimedEvents")
async def resolve_get_rent_events(parent, args, ctx, info):
    """
    Get all rent claimed events
    """

    return await resolve_event('RentClaimed', args, _transform_rent_claimed_event, sort_by = 'rentingID')
