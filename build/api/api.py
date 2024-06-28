import pandas as pd
import pathway as pw
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt

class QueryInputSchema(pw.Schema):
    query: str

class DataInputSchema(pw.Schema):
    doc: str

def run(host, port):
    query, response_writer = pw.io.http.rest_connector(
        host = host,
        port = port,
        schema = QueryInputSchema,
        autocommit_duration_ms = 50,
    )

    dataset_csv = pw.io.csv.read(
        '../csv/',
        schema=DataInputSchema,
        mode="streaming"
    )

    

