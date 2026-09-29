# Notas de investigacion

Separa siempre las observaciones de las interpretaciones.

## Registro

| Fecha | Tema | Hecho observado | Fuente o forma de verificar | Supuesto derivado | Confianza |
| --- | --- | --- | --- | --- | --- |
| 2026-09-29 | Punto de partida | El dominio candidato es `quasarchain.crypto` | Confirmado por el encargo | El nombre puede admitir varias categorias de producto | baja |
| 2026-09-29 | Capacidades del dominio | La documentacion de Unstoppable Domains presenta APIs de usuario, gestion programatica y un MCP para dominios | [docs.unstoppabledomains.com](https://docs.unstoppabledomains.com/) | El dominio puede servir como identidad o punto de coordinacion, sujeto a compatibilidad tecnica concreta | media |
| 2026-09-29 | Identidad blockchain | Ethereum distingue cuentas controladas por usuarios de cuentas de contrato; una wallet es la interfaz para interactuar con ellas | [ethereum.org/accounts](https://ethereum.org/en/developers/docs/accounts/) | Un producto de confianza debe separar identidad, custodia y autorizacion | alta |
| 2026-09-29 | Revision academica | Surveys y papers recientes convergen en identidad portable, credenciales verificables, procedencia y auditoria como usos plausibles de blockchain alrededor de IA; los trabajos sobre agentes con DID/VC siguen siendo tempranos | [academic-paper-review.md](academic-paper-review.md); DOI y enlaces abiertos registrados en el documento | Priorizar Trust Layer y Agent Passport; tratar pagos autonomos y reputacion como fases posteriores | media |
| 2026-09-29 | Marca y monetizacion | El analisis local identifica que `quasarchain.crypto` comunica verificabilidad, pero tambien puede sugerir una blockchain o token | [domain-and-monetization.md](domain-and-monetization.md); hipotesis H-001 a H-003 | Vender reduccion de riesgo y tiempo de auditoria; validar SaaS por organizacion antes de cobrar por uso | baja |
| 2026-09-30 | Nueva linea educativa | La computacion cuantica puede aportar un caso educativo de procedencia y reproducibilidad de circuitos, sin demostrar por si sola la correccion cientifica del resultado | [quantum-learning-plan.md](quantum-learning-plan.md); laboratorio Bell pendiente | Estudiar primero simuladores, parametros, hashes y recibos firmados antes de usar hardware cuantico | baja |
| 2026-09-30 | Laboratorio Bell | IBM documenta que aplicar H al qubit 0 y CNOT con control en 0 produce un estado Bell; los resultados se obtienen muestreando muchas ejecuciones | [IBM Quantum: Hello world](https://quantum.cloud.ibm.com/docs/guides/hello-world); reproducido localmente en `src/quasar_verifier/quantum_lab.py` | En el simulador ideal solo deben aparecer `00` y `11`; esto no valida hardware ni la interpretacion cientifica | alta |
| 2026-09-30 | Framework cuántico | Qiskit 2.5.2 funciona en Python 3.12.10 con `BasicSimulator`; con 1024 shots y semilla 7 produjo `00: 517` y `11: 507` | [qiskit_lab.py](../src/quasar_verifier/qiskit_lab.py); prueba `tests/test_qiskit_lab.py` | La semilla no fija la misma secuencia aleatoria entre frameworks; comparar soporte de resultados y parámetros, no conteos exactos | alta |
| 2026-09-30 | Entorno de ruido | Qiskit Aer 0.17.2 con error simétrico independiente de lectura del 5% produjo `00: 456`, `01: 53`, `10: 50` y `11: 465` en 1024 shots con semilla 7 | [qiskit_lab.py](../src/quasar_verifier/qiskit_lab.py); prueba `tests/test_qiskit_lab.py` | El ruido de lectura introduce resultados discordantes; esto es un modelo de simulación y no una medición de hardware | alta |

## Preguntas abiertas

- Quien es la audiencia inicial?
- Que problema concreto se quiere resolver?
- Que significa "chain" en el posicionamiento: infraestructura, trazabilidad, comunidad o solo marca?
- Hay restricciones regulatorias, geograficas o de custodia?
- Que recursos, capacidades tecnicas y canales de distribucion estan disponibles?
