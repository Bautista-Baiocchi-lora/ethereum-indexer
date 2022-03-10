

from db import client
from tartiflette import Resolver


@Resolver("Query.kongsByAddress")
async def resolve_get_kongs(parent, args, ctx, info):
    """
    Gets all kong ids for a given address
    """


    wallet_address = args['address']
    collection = client['ethereum-indexer']['0xEf0182dc0574cd5874494a120750FD222FdB909a-state']

    result  = await collection.find_one({"_id": 1})
    return result[wallet_address]



@Resolver("Query.kongHolders")
async def resolve_get_kongs(parent, args, ctx, info):    
    collection = client['ethereum-indexer']['0xEf0182dc0574cd5874494a120750FD222FdB909a-state']

    result  = await collection.find_one({"_id": 1})

    del result['_id'] # remove index
    return list(result.keys())
