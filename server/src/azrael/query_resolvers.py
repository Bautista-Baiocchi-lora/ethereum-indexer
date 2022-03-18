from typing import Callable, Dict, List, Optional

import pymongo
from db import DB
from tartiflette import Resolver

from azrael.event import (CollateralClaimed, Event, LendingStopped, LentEvent,
                          RentedEvent, ReturnedEvent)

database_name = 'ethereum-indexer'
collection_name = '0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7-state'

db = DB()

async def resolve_event(name: str, args: Dict, transformer: Callable, sort_by: Optional[str] = 'lendingId') -> List[Event]:
    """
    Resolves Azrael v1 event graphql query generically.

    Args:
        name (str): name of the event
        args (Dict): Graphql function parameters specified in query
        transformer (Callable): Callable function that map a mongodb doc to Azrael v1 event
        sort_by (Optional[str]): Index to sort mongodv results by. Defaults to 'lendingId'

    Returns:
        List[Event]: List of Azrael v1 events.
    """

    limit = args['limit']
    order = pymongo.ASCENDING if args['ascending'] else pymongo.DESCENDING

    query  = {'event': name}
    sort = [(sort_by, order)]

    # lendingId is stored as a String but we want to sort it as a number
    collation = {'locale': 'en', 'numericOrdering': True}

    options = {'query': query, 'sort': sort, 'collation': collation}

    results  = await db.get_all_items(database_name, collection_name, limit, options)

    return list(map(transformer, results))

@Resolver("Query.getLentEvents")
async def resolve_get_lent_events(parent, args, ctx, info) -> List[LentEvent]:
    """
    Resolves 'getLentEvents' graphql query for the Graphql Engine.

    Returns:
        List[LentEvent]: Event instance compatible with LentEvent Graphql schema.
    """

    return await resolve_event('Lent', args, LentEvent.from_doc)



@Resolver("Query.getRentedEvents")
async def resolve_get_rented_events(parent, args, ctx, info) -> List[RentedEvent]:
    """
    Resolves 'getRentedEvents' graphql query for the Graphql Engine.

    Returns:
        List[RentedEvent]: Event instance compatible with RentedEvent Graphql schema.
    """

    return await resolve_event('Rented', args, RentedEvent.from_doc)


@Resolver("Query.getReturnedEvents")
async def resolve_get_rented_events(parent, args, ctx, info) -> List[ReturnedEvent]:
    """
    Resolves 'getReturnedEvents' graphql query for the Graphql Engine.

    Returns:
        List[ReturnedEvent]: Event instance compatible with ReturnedEvent Graphql schema.
    """

    return await resolve_event('Returned', args, ReturnedEvent.from_doc)


@Resolver("Query.getLendingStoppedEvents")
async def resolve_get_rented_events(parent, args, ctx, info) -> List[LendingStopped]:
    """
    Resolves 'getLendingStoppedEvents' graphql query for the Graphql Engine.

    Returns:
        List[LendingStopped]: Event instance compatible with LendingStopped Graphql schema.
    """

    return await resolve_event('LendingStopped', args, LendingStopped.from_doc)


@Resolver("Query.getCollateralClaimedEvents")
async def resolve_get_rented_events(parent, args, ctx, info) -> List[CollateralClaimed]:
    """
    Resolves 'getCollateralClaimedEvents' graphql query for the Graphql Engine.

    Returns:
        List[CollateralClaimed]: Event instance compatible with CollateralClaimed Graphql schema.
    """

    return await resolve_event('CollateralClaimed', args, CollateralClaimed.from_doc)
