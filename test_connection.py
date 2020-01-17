import pypyodbc

connection = pypyodbc.connect(driver='{SQL Server}',
                              server='MACIEJEWSKI3\SQLEXPRESS',
                              database='CyberScouter',
                              uid='scout',
                              pwd='2qrobot!')

curr = connection.cursor()
curr1 = connection.cursor()
curr2 = connection.cursor()

curr.execute('SELECT EventID FROM [Current Event Analysis] WHERE Team = 1023')
rows = curr.fetchall()
for row in rows:
    print('row = %r' % (row,))

curr1.execute('UPDATE [Current Event Analysis] SET EventID=0 WHERE Team = 1023 and AnalysisTypeID = 1 and EventID = 22;')
curr1.commit()
