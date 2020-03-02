import cmd
import sys
import mysql.connector as mariaDB
import json

class ScoutingCLI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'Scouting> '

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt
        The default from Cmd is to execute the previous command again!
        This method returns control to the parent menu and does nothing on main menu
        """
        if self.prompt != 'main':
            print("No arguments entered. Exiting!")
            return True

    def do_dump(self, arg):
        print("Dumping DB table:", arg)

        # This bit of code create a dictionary named results with dynamic columns from the DB along with data records
        conn = mariaDB.connect(user='admin',
                               passwd='Einstein195',
                               host='frcteam195testinstance.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                               database='team195_scouting')
        cursor = conn.cursor()
        query = "SELECT * FROM team195_scouting." + arg + ";"
        result = cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        print(columns)
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))

        with open('../data.json', 'w') as outfile:
            print(results)
            json.dump(results, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    def help_dump(self):
        print("syntax: dump [DB_Table_Name]"),
        print("example: dump MatchScouting")
        print("-- dumps a DB Table to a JSON file")

    def do_quit(self, arg):
        sys.exit(1)

    def help_quit(self):
        print("syntax: quit"),
        print("-- terminates the application")

    # shortcuts
    do_q = do_quit

    #
    # try it out


cli = ScoutingCLI()
cli.cmdloop()