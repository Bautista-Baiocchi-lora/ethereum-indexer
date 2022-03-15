

from db import DB
from tartiflette import Resolver

database_name = 'ethereum-indexer'
collection_name = '0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7-state'

db = DB()

def parse_id(doc):
    id = doc['_id'].split('_')
    doc['tx_hash'] = id[0]
    doc['tx_offset'] = id[1]

    del doc['_id']
    return doc

@Resolver("Query.lentEvents")
async def resolve_get_kongs(parent, args, ctx, info):
    """
    Get all lent events
    """

    result  = await db.get_N_items(database_name, collection_name, 10000)

    return list(map(parse_id, result))
