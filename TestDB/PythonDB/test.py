import psycopg2


DB_NAME = "zdmcnqcr"
DB_USER = "zdmcnqcr"
DB_PASS = "XBadbsEmaLsWTet1jwyTARTA07wU45vh"
DB_HOST = "cornelius.db.elephantsql.com"
DB_PORT = "5432"
conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
print("Database connected successfully")

cur = conn.cursor()  # creating a cursor

# executing queries to create table
def selectEstudiante(cur,nombre):
    cur.execute("prepare selectEstudiante as"
                 "select * from estudiante where nombre = $1")
    cur.execute("execute selectEstudiante(%s)", (nombre,))
    
    rows = cur.fetchall()
    print(rows)

def insertEstudiante(cur, id, nombre, edad):
    cur.execute("prepare insertEstudiante as "
                 "insert into estudiante(id, nombre, edad)"
                 "values($1, $2, $3)")
    cur.execute("execute insertEstudiante(%s, %s, %s)", (id, nombre, edad))

def allEstudiantes(cur):
    cur.execute("select * from estudiante")
    rows = cur.fetchall()
    print(rows)

def deleteEstudiante(cur,id):
    cur.execute("prepare deleteEstudiante as "
                 "delete from estudiante where id >= $1")
    cur.execute("execute deleteEstudiante(%s)", (id,))

deleteEstudiante(cur, 3)
insertEstudiante(cur, 3, "Juan", 20)
allEstudiantes(cur)




