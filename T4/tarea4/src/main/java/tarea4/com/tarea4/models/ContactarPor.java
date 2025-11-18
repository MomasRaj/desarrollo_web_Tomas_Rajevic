package tarea4.com.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "contactar_por")
public class ContactarPor {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false, length = 50)
    private String nombre;

    @Column(nullable = false, length = 150)
    private String identificador;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", nullable = false)
    private AvisoAdopcion aviso;

    public ContactarPor() {
    }

    public ContactarPor(String nombre, String identificador) {
        this.nombre = nombre;
        this.identificador = identificador;
    }

    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getIdentificador() {
        return identificador;
    }

    public AvisoAdopcion getAviso() {
        return aviso;
    }
}