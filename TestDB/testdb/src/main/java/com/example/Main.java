package com.example;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import org.postgresql.ds.PGSimpleDataSource;


public class Main {
    public static void main(String[] args) throws Exception {
        DataSource ds = creaDataSource();
        Connection conn = ds.getConnection();
        
        try{
          //getAllStudents(conn);//filterSubjects(conn);
            //insertStudent(conn, 4, "Juan", 20);
            filterSubjects(conn,100);
        } catch (SQLException e) {
            System.out.println("Comienza reporte");
            e.printStackTrace();
            System.out.println("Termina reporte");   
        }
        
    }

    private static DataSource creaDataSource() {
        PGSimpleDataSource ds = new PGSimpleDataSource();
        ds.setServerName("cornelius.db.elephantsql.com");
        ds.setDatabaseName("zdmcnqcr");
        ds.setUser("zdmcnqcr");
        ds.setPassword("XBadbsEmaLsWTet1jwyTARTA07wU45vh");
        return ds;
    }

    private static void getAllStudents(Connection conn) throws SQLException {
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM estudiante");
        ResultSet rs = ps.executeQuery();
        while (rs.next()) {
            System.out.printf("id: %d nombre: %s edad: %d\n", rs.getInt("id"), rs.getString("nombre"), rs.getInt("edad"));
        }
    }

    private static void filterSubjects(Connection conn,Integer creditos) throws SQLException {
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM asignatura WHERE creditos <= ?");
        ps.setInt(1, creditos);
        ResultSet rs = ps.executeQuery();
        while (rs.next()) {
            System.out.println(rs.getString("id") + rs.getString("nombre") + rs.getString("creditos"));
        }
    }

    private static void insertStudent(Connection conn,Integer id, String nombre, Integer edad) throws SQLException {
        PreparedStatement ps = conn.prepareStatement("INSERT INTO estudiante (id, nombre, edad) VALUES (?, ?, ?)");
        ps.setInt(1, id);
        ps.setString(2, nombre);
        ps.setInt(3,edad);
        ps.executeUpdate();
    }

}