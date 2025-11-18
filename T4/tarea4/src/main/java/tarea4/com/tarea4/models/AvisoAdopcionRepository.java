package tarea4.com.tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.domain.Pageable;
import java.util.List;

public interface AvisoAdopcionRepository extends JpaRepository<AvisoAdopcion, Integer> {
    List<AvisoAdopcion> findAllByOrderByFechaIngresoDesc(Pageable pageable);
}
