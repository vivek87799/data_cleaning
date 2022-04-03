#!/usr/bin/env python3

# Logical implementaion
# 1) Init the faust app
# 2) Create a model schema for the data to be received
# 3) Assign the topic and the value type as model schema created
# 4) declare a function to process the received data
#    - To check for non clean segments
#    - XML elements mid segment like (</x> <g>) [<, </, >]
#    - HTML tags like (&lt;br/&gt;) [&lt;, br/, &gt]
#    - markup text [%link_start%, %link_end%]
#    - more to be added by the customers
# 5) Persist the data

import asyncio
import re

from elasticsearch import AsyncElasticsearch
import faust

from typing import List
from config import Field, Parameters

# Models describe how messages are serialized:
# {"account_id": "3fae-...", amount": 3}
"""
'{"src": "Bitte Zahlungsmethode w\u00e4hlen", 
"target": "Veuillez choisir votre moyen de paiement", 
"tuid": "810297994"}'
"""
class TMXData(faust.Record, serializer=Field.JSON):
    src: str
    target: str
    tuid: str

class DataCleaning:
    def __init__(self, ):
        pass
    
    @classmethod
    def worker_node(cls, string: str, patterns: List[List])-> str:
        for pattern in patterns:
            for p in pattern:
                string = re.sub(p, '', string )
        return string
    
    
    @classmethod
    def run_manager(cls, data: TMXData, patterns: List[List])-> str:
        # Clean the src and target data
        data.src = cls.worker_node(data.src, patterns)
        data.target = cls.worker_node(data.target, patterns)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
    

class DataPersist:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
    
    async def __async__dat_persist(self, data: TMXData):
        return await self.es.index(
            index=Parameters.ES_INDEX,
            id=data.tuid,
            document={Field.SRC: data.src,
            Field.TARGET: data.target
            }
        )
    
    @classmethod
    def run_manager(cls, data: TMXData):
        return self.loop.run_until_complete(self.__async__dat_persist(data))


loop = asyncio.get_event_loop()
es = AsyncElasticsearch(Parameters.ES_BROKER)
async def data_persist(data: TMXData):
        await es.index(
            index=Parameters.ES_INDEX,
            id=data.tuid,
            document={Field.SRC: data.src,
            Field.TARGET: data.target
            }
        )

app = faust.App(
    Parameters.GROUP_ID,
    broker=Parameters.BROKERS,
    value_serializer=Field.RAW,
)

data_topic = app.topic(Parameters.TOPIC, value_type=TMXData)
tasks = []
@app.agent(data_topic)
async def clean_data(raw_data: str):
    async for data in raw_data:
        if data.src is not None and data.target is not None:
            print(f'Before: {data.src}')
            # TODO run src and target data in two separate threads
            DataCleaning.run_manager(data, Parameters.PATTERNS)
            tasks.append(asyncio.create_task(data_persist(data)))
            print(f'After: {data.src}')
            

if __name__ == '__main__':
    app.main()