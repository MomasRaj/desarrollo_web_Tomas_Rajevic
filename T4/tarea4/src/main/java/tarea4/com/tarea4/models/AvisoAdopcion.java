package tarea4.com.tarea4.models;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "aviso_adopcion")
public class AvisoAdopcion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "fecha_ingreso", nullable = false)
    private LocalDateTime fechaIngreso;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "comuna_id", nullable = false)
    private Comuna comuna;

    @Column(length = 100)
    private String sector;

    @Column(nullable = false, length = 200)
    private String nombre;

    @Column(nullable = false, length = 100)
    private String email;

    @Column(length = 15)
    private String celular;

    @Column(nullable = false, length = 20)
    private String tipo;

    @Column(nullable = false)
    private Integer cantidad;

    @Column(nullable = false)
    private Integer edad;

    @Column(name = "unidad_medida", nullable = false, length = 2)
    private String unidadMedida;

    @Column(name = "fecha_entrega", nullable = false)
    private LocalDateTime fechaEntrega;

    @Column(length = 500)
    private String descripcion;



    @OneToMany(mappedBy = "aviso", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private List<Nota> notas;

    public AvisoAdopcion() {
    }

    public AvisoAdopcion(LocalDateTime fechaIngreso, String nombre, String email, String tipo, 
                         Integer cantidad, Integer edad, String unidadMedida, LocalDateTime fechaEntrega) {
        this.fechaIngreso = fechaIngreso;
        this.nombre = nombre;
        this.email = email;
        this.tipo = tipo;
        this.cantidad = cantidad;
        this.edad = edad;
        this.unidadMedida = unidadMedida;
        this.fechaEntrega = fechaEntrega;
    }

    public Integer getId() {
        return id;
    }

    public LocalDateTime getFechaIngreso() {
        return fechaIngreso;
    }

    public Comuna getComuna() {
        return comuna;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public String getTipo() {
        return tipo;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public Integer getEdad() {
        return edad;
    }

    public String getUnidadMedida() {
        return unidadMedida;
    }

    public LocalDateTime getFechaEntrega() {
        return fechaEntrega;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public List<Nota> getNotas() {
        return notas;
    }

    public Double getPromedioNotas() {
        if (notas == null || notas.isEmpty()) {
            return null;
        }
        return notas.stream()
                .mapToInt(Nota::getNota)
                .average()
                .orElse(0.0);
    }
}
