# Plan de aprendizaje: computacion cuantica y Trust Layer

Fecha de inicio: 2026-09-30.

## Objetivo

Construir conocimiento practico suficiente para diseñar demos educativas y evaluar con rigor oportunidades alrededor de computacion cuantica, agentes de IA y evidencia verificable.

No se busca afirmar especializacion academica. Se busca poder leer documentacion tecnica, ejecutar experimentos, explicar sus limites y registrar resultados reproducibles.

## Ruta de aprendizaje

### Etapa 1: fundamentos cuanticos

Dominar:

- bits, qubits y notacion de Dirac;
- superposicion y medicion;
- fase y amplitudes;
- puertas X, H, Z, S y T;
- entrelazamiento y estados Bell;
- circuitos y mediciones;
- diferencia entre simulador y hardware;
- ruido, decoherencia y numero de shots.

Ejercicio minimo: construir un circuito Bell, explicar sus probabilidades y ejecutarlo varias veces con una semilla fija.

### Etapa 2: programacion

Elegir un framework principal, inicialmente Qiskit o Cirq, y aprender:

- crear circuitos;
- transpilar;
- ejecutar en simulador;
- configurar shots y seed;
- inspeccionar resultados;
- serializar el circuito;
- capturar version del SDK y del backend.

Ejercicio minimo: producir el mismo resultado desde dos versiones del circuito y explicar cualquier diferencia.

### Etapa 3: reproducibilidad

Registrar para cada experimento:

- identidad del autor;
- circuito y hash;
- framework y version;
- backend y configuracion;
- shots y semilla;
- modelo de ruido;
- resultado bruto;
- resultado resumido;
- timestamp;
- errores y transformaciones.

Ejercicio minimo: modificar una puerta del circuito y demostrar que cambia el hash y que el manifiesto anterior ya no describe el experimento nuevo.

### Etapa 4: Trust Layer

Aplicar el verificador existente a experimentos cuanticos:

- manifiesto firmado de experimento;
- identidad del circuito;
- permisos para usar simulador o hardware;
- limite de shots o coste;
- aprobacion humana para backends reales;
- recibo verificable de ejecucion;
- revocacion de un experimento o credencial.

Ejercicio minimo: crear un Quantum Experiment Passport y mostrarlo en la consola local.

### Etapa 5: agentes de IA para quantum computing

Estudiar riesgos especificos:

- generacion de circuitos incorrectos;
- interpretacion erronea de resultados;
- consumo involuntario de recursos de hardware;
- cambios de version del transpiler;
- fuga de datos en problemas del usuario;
- exceso de confianza en una salida probabilistica.

Ejercicio minimo: permitir que un agente proponga un circuito, pero exigir verificacion, limite de recursos y aprobacion antes de ejecutarlo.

## Fuentes iniciales

- Documentacion oficial de Qiskit o Cirq.
- IBM Quantum Learning para fundamentos y circuitos.
- Nielsen y Chuang, *Quantum Computation and Quantum Information*, como referencia teorica.
- Documentacion del backend o simulador utilizado en cada experimento.
- Literatura sobre reproducibilidad cientifica, procedencia de datos y credenciales verificables.
- Documentacion del propio verificador en `docs/mvp-trust-layer.md`.

Las fuentes deben registrarse en `docs/research-notes.md` con fecha, afirmacion concreta y forma de verificacion.

## Metodo de estudio

Para cada concepto seguir este ciclo:

1. Leer una fuente primaria o documentacion oficial.
2. Explicarlo con palabras propias.
3. Ejecutar un ejemplo minimo.
4. Cambiar una variable y observar el resultado.
5. Registrar el resultado y la limitacion.
6. Convertir el aprendizaje en un test o manifiesto cuando sea posible.

No considerar aprendido un concepto solo por poder repetir su definicion.

## Primer laboratorio

### Pregunta

¿Puede un recibo firmado demostrar que un circuito Bell concreto fue ejecutado con determinados parametros?

### Experimento

- Circuito: dos qubits en estado Bell.
- Backend inicial: simulador local.
- Shots: 1024.
- Semilla: fija para reproducibilidad.
- Salida: conteo de resultados `00` y `11`.
- Evidencia: circuito serializado, hash, version del framework, parametros y resultado.

### Que demuestra

- Que el registro describe una ejecucion concreta.
- Que una modificacion del circuito altera el hash.
- Que otra persona puede repetir el experimento bajo los mismos parametros.

### Que no demuestra

- Que el circuito sea util para un problema real.
- Que el resultado sea correcto fuera del modelo del simulador.
- Que el hardware futuro produzca la misma distribucion.
- Que una firma garantice la veracidad cientifica de la interpretacion.

## Criterios de progreso

- **Nivel 1:** explicar y ejecutar un circuito Bell.
- **Nivel 2:** reproducirlo y registrar sus parametros.
- **Nivel 3:** detectar alteraciones mediante hash y firma.
- **Nivel 4:** controlar permisos y costes de ejecucion.
- **Nivel 5:** evaluar un agente que genera o ejecuta circuitos sin confundir integridad con correccion.

## Regla de rigor

Separar siempre:

- hecho observado;
- interpretacion;
- hipotesis;
- limitacion;
- fuente de verificacion.
