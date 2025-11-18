package tarea4.com.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "foto")
public class Foto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "ruta_archivo", nullable = false, length = 300)
    private String rutaArchivo;

    @Column(name = "nombre_archivo", nullable = false, length = 300)
    private String nombreArchivo;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", nullable = false)
    private AvisoAdopcion aviso;

    public Foto() {
    }

    public Foto(String rutaArchivo, String nombreArchivo) {
        this.rutaArchivo = rutaArchivo;
        this.nombreArchivo = nombreArchivo;
    }

    public Integer getId() {
        return id;
    }

    public String getRutaArchivo() {
        return rutaArchivo;
    }

    public String getNombreArchivo() {
        return nombreArchivo;
    }

    public AvisoAdopcion getAviso() {
        return aviso;
    }
}