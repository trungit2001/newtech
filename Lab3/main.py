from database import sql_query
from settings import TECH_TAXI_DB_URI
from query_stmt import queries, schemas
from utils import print_table

def main():
    for cau, unzip_obj in enumerate(zip(queries, schemas), start=1):
        query, schema = unzip_obj
        print("[INFO] == Cau {} ==".format(cau))
        res = sql_query(TECH_TAXI_DB_URI, query)
        print_table(res, schema)

    
if __name__ == "__main__":
    main()