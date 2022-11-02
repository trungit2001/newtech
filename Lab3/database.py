import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, ForeignKey, Float, DateTime
from sqlalchemy.sql import text

from settings import DEFAULT_DB_URI, TECH_TAXI_DB_URI, DB_NAME
from utils import load_data


def init_conn(
    db_uri: str = DEFAULT_DB_URI,
    echo: bool = True
):
    engine = create_engine(db_uri, echo=echo)
    metadata = MetaData()

    return engine, metadata


def create_db_tech_taxi(engine, metadata: MetaData) -> dict:
    tai_xe = Table("tai_xe", metadata,
        Column("matx", String(10), primary_key=True, nullable=False),
        Column("hoten", String(64)),
        Column("sdt", String(12)),
        Column("diem", Float),
        Column("lxe", String(10))
    )
    kh = Table("kh", metadata,
        Column("makh", String(10), primary_key=True, nullable=False),
        Column("hoten", String(64)),
        Column("sdt", String(12))
    )
    dat_xe = Table("dat_xe", metadata,
        Column("madx", String(10), primary_key=True, nullable=False),
        Column("makh", String(10), ForeignKey("kh.makh"), nullable=False),
        Column("ddi", String(128)),
        Column("dden", String(128)),
        Column("lxe", String(10)),
        Column("kc", Float),
        Column("gia", Float),
        Column("tgdat", DateTime)
    )
    doi_xe = Table("doi_xe", metadata,
        Column("madx", String(10), ForeignKey("dat_xe.madx"), primary_key=True, nullable=False),
        Column("matx", String(10), ForeignKey("tai_xe.matx"), primary_key=True, nullable=False),
        Column("tgbdau", DateTime),
        Column("tgkthuc", DateTime, default=None),
        Column("kqua", String(20), default=None)
    )
    chuyen_di = Table("chuyen_di", metadata,
        Column("macd", String(10), primary_key=True, nullable=False),
        Column("madx", String(10), ForeignKey("doi_xe.madx"), nullable=False),
        Column("matx", String(10), ForeignKey("doi_xe.matx"), nullable=False),
        Column("tgdi", DateTime),
        Column("tgden", DateTime, default=None),
        Column("gia", Float, default=None),
        Column("htttoan", String(20), default=None),
        Column("diem", Float, default=None)
    )
    metadata.create_all(engine)
    tables = {
        "tai_xe": tai_xe,
        "kh": kh,
        "dat_xe": dat_xe,
        "doi_xe": doi_xe,
        "chuyen_di": chuyen_di
    }

    return tables


def insert_data_to_db(db_url, tables: dict[Table]):
    engine, _ = init_conn(db_url, echo=False)
    conn = engine.connect()
    tbs_ordered = ["tai_xe", "kh", "dat_xe", "doi_xe", "chuyen_di"]

    for tb_name in tbs_ordered:
        data = load_data(os.path.join("./data", tb_name + ".csv"))
        conn.execute(tables[tb_name].insert(), data)


def sql_query(db_url, query: str):
    try:
        engine, _ = init_conn(db_url, echo=False)
        conn = engine.connect()
        query = text(query)

        print("[INFO] Starting query on db")
        results = conn.execute(query).fetchall()
        
        return results
    except Exception as e:
        print("[ERROR] Detail:", e)
    finally:
        print("[INFO] Close connection")
        conn.close()

    return None
    

def run_pipeline():
    try:
        print("[INFO] Check exist db")
        if os.path.exists(DB_NAME):
            print("[WARNING] Delete exist db!")
            check = input("Confirm delete? (y/N): ")
            if check in ["y", "Y"]:
                os.remove(DB_NAME)
                print("[INFO] Deleted db!")
            
        print("[INFO] Initialize the tech taxi db")
        engine, metadata = init_conn(TECH_TAXI_DB_URI, echo=False)
        tables = create_db_tech_taxi(engine, metadata)
        print("[INFO] Database created")

        print("[INFO] Start inserting data into db")
        insert_data_to_db(TECH_TAXI_DB_URI, tables)
        print("[INFO] Finished inserting data into db")

    except Exception as e:
        print("[ERROR] Detail:", e)


if __name__ == "__main__":
    run_pipeline()