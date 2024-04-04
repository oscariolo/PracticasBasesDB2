import mysql.connector

class DataBaseMySQL:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='mysql01-basesdedatoscap1.a.aivencloud.com',
            port=17983,
            user = 'avnadmin',
            password = 'AVNS_sOEGdTLpIQxr-z-1ru6',
            database = 'universidad'
        )
        self.cur = self.conn.cursor()

    def ejecutar_query(self, query):
        self.cur.execute(query)
        self.conn.commit()
        self.cur.close()
        
    def crear_tabla_log_estudiantes(self):
        query = """
        CREATE TABLE IF NOT EXISTS log_estudiantes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            estudiante_id INT,
            nombre VARCHAR(100),
            edad INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.ejecutar_query(query)
    
    def crear_procedimiento_agregar_log_estudiante(self):
        query = """
        CREATE PROCEDURE agregar_log_estudiante(id INT, nombre_anterior VARCHAR(100), edad_anterior INT)
        BEGIN
            INSERT INTO log_estudiantes (estudiante_id, nombre, edad)
            VALUES (id, nombre_anterior, edad_anterior);
        END;
        """
        self.ejecutar_query(query)
    
    def crear_trigger_detectar_cambio_estudiante(self):
        query = """
        CREATE TRIGGER trigger_detectar_cambio_estudiante
        AFTER UPDATE ON estudiantes
        FOR EACH ROW
        CALL agregar_log_estudiante(NEW.id, OLD.nombre, OLD.edad); 
        """ #en vez de ejecutar la funcion se llama con CALL
        self.ejecutar_query(query)
    
    def insertEstudiante(self ,id, nombre, edad):
        self.cur.execute("prepare insertEstudiante as "
                    "insert into estudiantes(id, nombre, edad)"
                    "values($1, $2, $3)")
        self.cur.execute("execute insertEstudiante(%s, %s, %s)", (id, nombre, edad))
        self.conn.commit()
        self.cur.close()
    
    def actualizarEstudiante(self, id, nombre, edad):
        self.cur.execute("update estudiantes set nombre = %s, edad = %s where id = %s", (nombre, edad, id))
    
    def mostrarEstudiantes(self):
        self.cur.execute("select * from estudiantes")
        rows = self.cur.fetchall()
        print(rows)
    
    def mostrar_log_Estudiantes(self):
        self.cur.execute("select * from log_estudiantes")
        rows = self.cur.fetchall()
        print(rows)
    
    def drop_trigger_procedure(self):
        query = """
        DROP TRIGGER IF EXISTS trigger_detectar_cambio_estudiante;
        DROP PROCEDURE IF EXISTS agregar_log_estudiante;
        """
        self.ejecutar_query(query)

if __name__ == '__main__':
    db = DataBaseMySQL()
    #db.crear_procedimiento_agregar_log_estudiante()
    #db.crear_trigger_detectar_cambio_estudiante()
    db.mostrarEstudiantes()
    db.actualizarEstudiante(1, "Sebastian", 20)
    db.mostrarEstudiantes()
    db.mostrar_log_Estudiantes()
    db.conn.commit()
    db.cur.close()
    
    

    