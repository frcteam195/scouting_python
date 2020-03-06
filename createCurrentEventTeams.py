import mysql.connector as mariaDB

conn = mariaDB.connect(user='admin',
                       passwd='Einstein195',
                       host='frcteam195.cmdlvflptajw.us-east-1.rds.amazonaws.com',
                       database='team195_scouting')
cursor = conn.cursor()
cursor.execute("DELETE FROM CurrentEventTeams")
conn.commit()


cursor.execute("SELECT BlueAllianceTeams.Team FROM BlueAllianceTeams")
for team in cursor.fetchall():
    query = "INSERT INTO CurrentEventTeams (Team) VALUES (" + team[0] + ");"
    print(query)
    cursor.execute(query)
    conn.commit()
