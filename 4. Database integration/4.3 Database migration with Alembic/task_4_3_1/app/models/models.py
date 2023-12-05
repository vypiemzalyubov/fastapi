from sqlalchemy import MetaData, Table, Column, Integer, String, Float

metadata = MetaData()

product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("price", Float),
    Column("count", Integer),
    Column("description", String)
)
