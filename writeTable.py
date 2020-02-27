import mysql.connector as mariaDB
import json
import sys


class dumpTable(object):
    def __init__(self, file, table):
        # Connection to AWS Testing database - use when you would destroy tables with proper data
        # conn = mariaDB.connect(user='admin',
        #                        passwd='Einstein195',
        #                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
        #                        database='team195_scouting')

        # Connection to AWS database with proper data
        self.conn = mariaDB.connect(user='admin',
                                    passwd='Einstein195',
                                    host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')

        self.cursor = self.conn.cursor()

        while table is None:
            table = input("Enter table name ('?' for list of tables, 'q' to quit): ")
            if len(table) == 0:
                table = None
            elif table == "?":
                self._run_query("USE team195_scouting")
                self._run_query("SHOW TABLES")
                for row in self.cursor.fetchall():
                    print(row[0])
                table = None
            elif table.lower() == 'q':
                return

        self.dump(table)

    def _run_query(self, query):
        self.cursor.execute(query)

    def dump(self, table):
        self._run_query("SELECT * FROM team195_scouting." + table + ";")
        columns = [column[0] for column in self.cursor.description]
        print(columns)
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))

        with open(table + '.json', 'w') as outfile:
            print(results)
            json.dump(results, outfile, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    table = None
    if len(sys.argv) > 1:
        table = sys.argv[1]
    mydumpTable = dumpTable(table)