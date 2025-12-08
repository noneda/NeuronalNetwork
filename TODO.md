# TODO LIST [ ]

- [ ] Domain Driven Design

## TODO Dominio -> @Sebaxsus
- [x] Service
- [x] Model
- [x] Repository

## TODO Model
- [x] Tablas usuario `userId, username, password (Bytes), predictId`
- [x] Tabla predicciones `idPred, predPrompt, predRes, fk userId` -> 
- [ ] **(Not Required)** Tabla gráficos `idGraf, GrafURL, fk idPred`

## TODO Repository ()
- [x] Reglas de Dominio para usuario (Validaciones de nombres de usuario y contraseñas).
- [x] Función de Hash para comparar el hash guardado en la DB.
- [ ] 

## TODO Service ()
- [ ] Implementar Salting al hashear las contraseñas para evitar que dos contraseñas iguales en distintos usuarios no generen el mismo hash.