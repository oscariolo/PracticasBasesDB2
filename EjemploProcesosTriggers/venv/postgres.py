import psycopg2

# Establish a connection to the PostgreSQL database
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

# Create a cursor object to execute SQL statements
cur = conn.cursor()

# #drop log table
# drop_table_sql = "DROP TABLE IF EXISTS asignatura_logs;"
# cur.execute(drop_table_sql)

# # Create a table for logs of changes in asignatura table
# log_table_sql = """
# CREATE TABLE asignatura_logs (
#     id SERIAL PRIMARY KEY,
#     asignatura_id INTEGER,
#     nombre VARCHAR(10),
#     creditos INT,
#     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """
# cur.execute(log_table_sql)
# Create a procedure
procedure_sql = """
CREATE OR REPLACE FUNCTION agregar_log_asignatura()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO asignatura_logs (asignatura_id, nombre, creditos)
    VALUES (NEW.id, OLD.nombre, OLD.creditos);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
cur.execute(procedure_sql)

drop_trigger_sql = """
DROP TRIGGER IF EXISTS trigger_detectar_cambio ON asignatura;
"""
cur.execute(drop_trigger_sql)

# Create a trigger
trigger_sql = """
CREATE TRIGGER trigger_detectar_cambio
AFTER UPDATE ON asignatura
FOR EACH ROW
EXECUTE FUNCTION agregar_log_asignatura();
"""
cur.execute(trigger_sql)

# Commit the changes and close the connection
conn.commit()

#update a row
cur.execute("UPDATE asignatura SET id = 1, nombre = 'Bcambiado4' WHERE id = 1;")

conn.commit()
#print logs
cur.execute("SELECT * FROM asignatura_logs;")
rows = cur.fetchall()
for row in rows:
    print(row)



cur.close()
conn.close()