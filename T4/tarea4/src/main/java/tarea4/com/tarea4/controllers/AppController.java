package tarea4.com.tarea4.controllers;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import tarea4.com.tarea4.models.AvisoAdopcion;
import tarea4.com.tarea4.models.AvisoAdopcionRepository;
import tarea4.com.tarea4.models.Nota;
import tarea4.com.tarea4.models.NotaRepository;

@Controller
public class AppController {
    private final AvisoAdopcionRepository avisoAdopcionRepository;
    private final NotaRepository notaRepository;
    
    public AppController(AvisoAdopcionRepository avisoAdopcionRepository, NotaRepository notaRepository) {
        this.avisoAdopcionRepository = avisoAdopcionRepository;
        this.notaRepository = notaRepository;
    }
    
    @GetMapping("/")
    public String indexRoute(Model model) {
        List<AvisoAdopcion> avisos = avisoAdopcionRepository.findAllByOrderByFechaIngresoDesc(PageRequest.of(0, 5));
        model.addAttribute("avisos", avisos);
        return "listado";
    }

    @PostMapping("/evaluar")
    public ResponseEntity<String> evaluarAviso(@RequestBody Map<String, Object> payload) {
        Integer avisoId = Integer.valueOf(payload.get("aviso_id").toString());
        Integer notaValor = Integer.valueOf(payload.get("nota").toString());
        
        if (notaValor < 1 || notaValor > 7) {
            return ResponseEntity.badRequest().body("Nota debe estar entre 1 y 7");
        }
        
        Optional<AvisoAdopcion> avisoOpt = avisoAdopcionRepository.findById(avisoId);
        
        if (avisoOpt.isEmpty()) {
            return ResponseEntity.badRequest().body("Aviso no encontrado");
        }
        
        Nota nota = new Nota(notaValor);
        nota.setAviso(avisoOpt.get());
        notaRepository.save(nota);
        
        return ResponseEntity.ok("Nota guardada exitosamente");
    }
}
