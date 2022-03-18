from typing import Dict, List

from db import DB
from tartiflette import Resolver

database_name = 'ethereum-indexer'
collection_name = '0xEf0182dc0574cd5874494a120750FD222FdB909a-state'

db = DB()

@Resolver("Query.kongsByAddress")
async def resolve_get_kongs(parent, args, ctx, info) -> Dict:
    """
    Resolves 'kongsByAddress' graphql query for the Graphql Engine.

    Returns:
        Dict: Mapping of kong id to wallet address, compatible with RKL Graphql schema.
    """
    wallet_address = args['address']

    result  = await db.get_item(1, database_name, collection_name)
    return result[wallet_address]



@Resolver("Query.kongHolders")
async def resolve_get_kongs(parent, args, ctx, info) -> List[str]:    
    """
    Resolves 'kongHolders' graphql query for the Graphql Engine.

    Returns:
        List[str]: List of wallet addresses that are kong holders, compatible with RKL Graphql schema.
    """

    result  = await db.get_item(1, database_name, collection_name)

    del result['_id'] # remove index
    return list(result.keys())
