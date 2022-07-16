import sqlite3

#function to add a new row to a table and return the id
def addRow(conn, sql):
    #first execute the sql to add a row
    conn.execute(sql)

    #now get the id of the last row entered
    sql = "SELECT last_insert_rowid()"

    #format that id so it is a plain int
    id = conn.execute(sql).fetchone()[0]

    #return the id
    return id


