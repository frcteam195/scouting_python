import mysql.connector as mariaDB

class dumpTable(object):
    def __init__(self, table):
        # Connection to AWS Testing database - use when you would destroy tables with proper data
        # conn = mariaDB.connect(user='admin',
        #                        passwd='Einstein195',
        #                        host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
        #                        database='team195_scouting')

        # Connection to AWS database with proper data
        self.conn = mariaDB.connect(user='admin',
                                    passwd='Einstein195',
                                    host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                                    database='team195_scouting')

        self.cursor = self.conn.cursor()
        self.dump(Matches)

    def _run_query(self,query):
        self.cursor.execute(query)

    def dump(self,table):
        self._run_query("SELECT * FROM team195_scouting." + arg + ";")
        columns = [column[0] for column in cursor.description]
        print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        with open('data2.json', 'w') as outfile:
            print(results)
            json.dump(results, outfile, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    mydumpTable = dumpTable(object)