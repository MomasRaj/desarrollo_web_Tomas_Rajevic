package tarea4.com.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "comentario")
public class Comentario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 80)
    private String nombre;

    @Column(nullable = false, length = 300)
    private String texto;

    @Column(nullable = false)
    private LocalDateTime fecha;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;

    public Comentario() {
    }

    public Comentario(String nombre, String texto, LocalDateTime fecha) {
        this.nombre = nombre;
        this.texto = texto;
        this.fecha = fecha;
    }

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getTexto() {
        return texto;
    }

    public LocalDateTime getFecha() {
        return fecha;
    }

    public AvisoAdopcion getAviso() {
        return aviso;
    }
}