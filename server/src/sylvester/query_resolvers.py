from typing import Callable, Dict, List, Optional

import pymongo
from db import DB
from tartiflette import Resolver

from sylvester.event import (LendEvent, RentClaimedEvent, RentEvent,
                             StopLendEvent, StopRentEvent, SylvesterEvent)

database_name = 'ethereum-indexer'
collection_name = '0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a-state'

db = DB()

# TODO: This method is almost identical to one inside azrael.query_resolver
async def resolve_event(name: str, args: Dict, transformer: Callable, sort_by: Optional[str] = 'lendingID'
    ) -> List[SylvesterEvent]:
    """
    Resolves Sylveser v1 event graphql query generically.

    Args:
        name (str): name of the event
        args (Dict): Graphql function parameters specified in query
        transformer (Callable): Callable function that map a mongodb doc to Sylvester v1 event
        sort_by (Optional[str]): Index to sort mongodv results by. Defaults to 'lendingId'

    Returns:
        List[Event]: List of Sylvester v1 events.
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



@Resolver("Query.getLendEvents")
async def resolve_get_lend_events(parent, args, ctx, info) -> List[LendEvent]:
    """
    Resolves 'getLendEvents' graphql query for the Graphql Engine.

    Returns:
        List[LendEvent]: Event instance compatible with LendEvent Sylvester v1 Graphql schema.
    """

    return await resolve_event('Lend', args, LendEvent.from_doc)


@Resolver("Query.getRentEvents")
async def resolve_get_rent_events(parent, args, ctx, info) -> List[RentEvent]:
    """
    Resolves 'getRentEvents' graphql query for the Graphql Engine.

    Returns:
        List[RentEvent]: Event instance compatible with RentEvent Sylvester v1 Graphql schema.
    """

    return await resolve_event('Rent', args, RentEvent.from_doc)



@Resolver("Query.getStopRentEvents")
async def resolve_get_stop_rent_events(parent, args, ctx, info) -> List[StopRentEvent]:
    """
    Resolves 'getStopRentEvents' graphql query for the Graphql Engine.

    Returns:
        List[StopRentEvent]: Event instance compatible with StopRent Sylvester v1 Graphql schema.
    """

    return await resolve_event('StopRent', args, StopRentEvent.from_doc, sort_by = 'rentingID')


@Resolver("Query.getStopLendEvents")
async def resolve_get_stop_lend_events(parent, args, ctx, info) -> List[StopLendEvent]:
    """
    Resolves 'getStopLendEvents' graphql query for the Graphql Engine.

    Returns:
        List[StopRentEvent]: Event instance compatible with StopLend Sylvester v1 Graphql schema.
    """

    return await resolve_event('StopLend', args, StopLendEvent.from_doc)



@Resolver("Query.getRentClaimedEvents")
async def resolve_get_rent_claimed_events(parent, args, ctx, info) -> List[RentClaimedEvent]:
    """
    Resolves 'getRentClaimedEvents' graphql query for the Graphql Engine.

    Returns:
        List[RentClaimedEvent]: Event instance compatible with RentClaimed Sylvester v1 Graphql schema.
    """

    return await resolve_event('RentClaimed', args, RentClaimedEvent.from_doc, sort_by = 'rentingID')