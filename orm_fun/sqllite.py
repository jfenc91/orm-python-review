import sqlite3

# connecting to the database
connection = sqlite3.connect("../chinook.db")



crsr = connection.cursor()
ret = crsr.execute("SELECT * FROM customers").fetchone()

# ret = crsr.execute("SELECT COUNT(DISTINCT Company) FROM customers").fetchone()
# ret = crsr.execute("SELECT COUNT(DISTINCT ArtistId) FROM albums").fetchone()
# ret = crsr.execute("SELECT COUNT(ArtistId) FROM albums").fetchone()

# top 10 artists by id
ret = crsr.execute("""SELECT ArtistId, COUNT(*) FROM albums 
                   GROUP BY ArtistId ORDER BY COUNT(*) DESC""").fetchmany(10)


# All artist names with more than 10 albums
ret = crsr.execute("""
        SELECT a.Name
        FROM artists AS a 
        INNER JOIN (SELECT * FROM albums GROUP BY ArtistID HAVING COUNT(*) > 10) AS e
        ON a.ArtistId=e.ArtistId
    """).fetchall()


# Artist names, album count ordered desc by total albums
ret = crsr.execute("""
        SELECT a.Name, e.Ct
        FROM artists AS a 
        INNER JOIN (SELECT ArtistId,COUNT(*) AS Ct FROM albums GROUP BY ArtistID) AS e
        ON a.ArtistId=e.ArtistId
        ORDER BY e.Ct DESC
    """).fetchall()



print(ret)