package tarea4.com.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "nota")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "aviso_id", nullable = false)
    private AvisoAdopcion aviso;

    @Column(nullable = false)
    private Integer nota;

    public Nota() {
    }

    public Nota(Integer nota) {
        this.nota = nota;
    }

    public Integer getId() {
        return id;
    }

    public AvisoAdopcion getAviso() {
        return aviso;
    }

    public Integer getNota() {
        return nota;
    }

    public void setAviso(AvisoAdopcion aviso) {
        this.aviso = aviso;
    }
}
