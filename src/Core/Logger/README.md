# **Clase Singleton con métodos estáticos**

## **Declaraciòn en Codigo**

```python
Logger.log("Mensaje normal")
Logger.info("Información")
Logger.success("Éxito")
Logger.warning("Advertencia")
Logger.error("Error")
Logger.start("Inicio de servicio")
```

### **✅ Colores ANSI:**

- **BLANCO** → `Logger.log()` - Mensajes normales
- **AZUL** → `Logger.info()` - Información
- **VERDE** → `Logger.success()` y `Logger.start()` - Éxitos e inicios
- **AMARILLO** → `Logger.warning()` - Advertencias
- **ROJO** → `Logger.error()` - Errores
- **GRIS** → Timestamps

### **✅ Timestamps automáticos**

Cada mensaje tiene formato: `[2024-12-04 15:30:45.123] [NIVEL] mensaje`
