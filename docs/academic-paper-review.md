# Revision de papers academicos

Fecha de corte: 2026-09-29.

## Objetivo

Evaluar que lineas de `quasarchain.crypto` tienen mejor fundamento academico y mejor relacion entre valor potencial, viabilidad de MVP y riesgo. La revision no trata el numero de citas como prueba de que una idea funcione: se usa como señal de madurez junto con el tipo de estudio, la evidencia experimental y la distancia respecto al producto.

## Resultado ejecutivo

La mejor oportunidad es una **capa de confianza para agentes** que combine:

1. Identidad criptografica portable y credenciales verificables.
2. Manifiestos firmados de capacidades, version, permisos y caducidad.
3. Registro verificable de ejecuciones y procedencia.
4. Politicas de autorizacion y revocacion fuera de la cadena, con anclaje de evidencia cuando aporte valor.

La evidencia es mas fuerte para identidad, procedencia, auditoria y trust management que para pagos autonomos. Por eso el primer producto no deberia custodiar fondos, emitir un token propio ni presentar una reputacion numerica como garantia de seguridad.

## Papers prioritarios

| Paper | Tipo y señal | Aporte util | Limite para el producto | Prioridad |
| --- | --- | --- | --- | --- |
| Salah, Rehman, Nizamuddin y Al-Fuqaha (2019), [Blockchain for AI: Review and Open Research Challenges](https://doi.org/10.1109/ACCESS.2018.2890507) | Revision, IEEE Access, alta citacion | Ordena como blockchain puede aportar integridad, pagos, logs y gobernanza a sistemas de IA; explicita escalabilidad, privacidad e interoperabilidad | Es una agenda de investigacion, no una validacion de un producto de agentes | Alta |
| Mazzocca et al. (2025), [A Survey on Decentralized Identifiers and Verifiable Credentials](https://doi.org/10.1109/COMST.2025.3543197) | Survey reciente en IEEE Communications Surveys & Tutorials; version abierta en [arXiv](https://arxiv.org/abs/2402.02455) | Resume DID, VC, SSI, amenazas, implementaciones, regulacion y barreras de adopcion | No resuelve por si solo la identidad operativa ni el comportamiento de un agente | Muy alta |
| Rodriguez Garzon et al. (2026), [AI Agents with Decentralized Identifiers and Verifiable Credentials](https://doi.org/10.5220/0014234400004052) | Paper de conferencia; version abierta en [arXiv](https://arxiv.org/abs/2511.02841) | Propone agentes con identidad persistente, atestaciones de terceros y dialogo multiagente verificable; reporta viabilidad de prototipo | Evidencia temprana, pocas citas y control de seguridad del agente LLM aun limitado | Muy alta, como pista |
| Schardong y Custodio (2022), [Self-Sovereign Identity: A Systematic Review, Mapping and Taxonomy](https://doi.org/10.3390/s22155641) | Revision sistematica, Sensors | Da taxonomia y mapa de retos de SSI: interoperabilidad, privacidad, gobernanza y adopcion | SSI puede introducir complejidad de wallets, recuperacion y correlacion de identidades | Alta |
| Han et al. (2023), [Accounting and auditing with blockchain technology and artificial Intelligence: A literature review](https://doi.org/10.1016/j.accinf.2022.100598) | Revision de literatura, International Journal of Accounting Information Systems | Conecta ledger compartido, validacion multi-actor, trazabilidad y auditoria continua; tambien advierte cautela de adopcion | El dominio es auditoria, no agentes; el beneficio depende de datos y controles previos fiables | Alta |
| Rahman et al. (2020), [Secure and Provenance Enhanced Internet of Health Things Framework](https://doi.org/10.1109/ACCESS.2020.3037474) | Framework con implementacion y pruebas, IEEE Access | Combina blockchain, procedencia, reputacion, smart contracts, federated learning y privacidad diferencial | Caso healthcare especifico y arquitectura costosa; no prueba una reputacion general de agentes | Alta para procedencia |
| Yu et al. (2013), [A Survey of Multi-Agent Trust Management Systems](https://doi.org/10.1109/ACCESS.2013.2259892) | Survey fundacional, IEEE Access | Aporta modelos de reputacion basados en observacion, auto-vigilancia y teoria de juegos | Es anterior a LLM, wallets y credenciales verificables; no asumir que sus scores sean transferibles | Media, fundamento |
| Lins, v. d. H. y Sunyaev (2021), [Trustworthy artificial intelligence](https://doi.org/10.1007/s12525-020-00441-4) | Marco conceptual, Electronic Markets | Define beneficencia, no maleficencia, autonomia, justicia y explicabilidad; vincula TAI con DLT | No ofrece un protocolo operativo ni una metrica suficiente para un agente concreto | Alta como criterio de diseño |
| Bernal Bernabe et al. (2019), [Privacy-Preserving Solutions for Blockchain: Review and Challenges](https://doi.org/10.1109/ACCESS.2019.2950872) | Revision sistematica, IEEE Access | Obliga a tratar privacidad, linkability, recuperacion de claves, datos on-chain y cumplimiento | Es una base de riesgos, no una solucion de UX o gobernanza | Alta como restriccion |

## Comparacion de lineas de producto

Puntuacion de 1 a 5. Una puntuacion alta significa mejor posicion relativa; en riesgo, significa menor riesgo. La puntuacion es una hipotesis informada por los papers, no evidencia de mercado.

| Linea | Dolor | Diferenciacion | Viabilidad MVP | Distribucion B2B | Riesgo controlable | Aprendizaje rapido | Total | Lectura |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Trust Layer: identidad, permisos y trazas | 5 | 4 | 5 | 4 | 4 | 5 | 27 | Mejor primer wedge |
| Agent Passport: DID/VC y manifiesto verificable | 4 | 5 | 4 | 4 | 4 | 4 | 26 | Complemento natural y posible estandar |
| Proof of Origin: procedencia de datos y decisiones | 4 | 4 | 4 | 4 | 4 | 4 | 24 | Muy construible, explicar integridad != verdad |
| Wallet Intelligence | 5 | 4 | 3 | 3 | 2 | 3 | 20 | Alto valor, alto coste de error |
| Escrow entre agentes | 3 | 4 | 2 | 3 | 2 | 2 | 16 | Fase posterior a demanda real |
| Research Network | 3 | 3 | 4 | 2 | 3 | 4 | 19 | Facil de prototipar, mas competida |

## Que afirmaciones quedan respaldadas

- **Respaldada como direccion:** blockchain puede aportar integridad, trazabilidad, auditabilidad y coordinacion multi-actor cuando existe un problema de confianza entre organizaciones.
- **Respaldada como arquitectura emergente:** DID y VC son una base razonable para dar a agentes identidad portable y atestaciones verificables.
- **Respaldada con cautela:** procedencia y logs ayudan a demostrar que un registro no fue alterado; no demuestran que el contenido, la fuente o la decision sean verdaderos.
- **No demostrada:** una puntuacion de reputacion por si sola predice de forma fiable el comportamiento futuro de un agente.
- **No demostrada:** que agentes autonomos deban poder gastar dinero sin aprobacion humana, limites, revocacion y mecanismo de disputa.

## Recomendacion de investigacion y MVP

### Fase 1: verificador de agentes

- Manifiesto JSON firmado: DID, version, capacidades, permisos, propietario u operador, caducidad y contacto de revocacion.
- Verificador que compruebe firma, esquema, caducidad y revocacion.
- Registro de ejecucion con `agent_id`, version, herramienta, permiso invocado, resultado, timestamp y hash de evidencia.
- No guardar prompts ni datos sensibles en la cadena; anclar solo hashes o referencias con politica de retencion.

### Fase 2: evidencia de confianza

- Credenciales verificables emitidas por un operador, auditor o plataforma.
- Metricas separadas para disponibilidad, cumplimiento de politica, tasa de incidentes y calidad por tarea.
- Mostrar evidencia y contexto, no un numero unico presentado como verdad.

### Fase 3: coordinacion economica

- Solo despues de validar usuarios y casos: presupuestos, escrow, aprobacion humana y disputa.
- Preferir saldo interno o integracion con un proveedor regulado antes que custodia propia.

## Experimentos que pueden cambiar la decision

1. Entrevistar a cinco equipos que ejecuten agentes con acceso a APIs, datos o fondos. Exito: tres describen un coste o incidente actual de trazabilidad/permisos y dos prueban el verificador.
2. Construir en siete dias un manifiesto firmado, verificador y diez trazas simuladas. Medir tiempo de integracion, errores de verificacion y campos que los usuarios consideran imprescindibles.
3. Intentar falsificar una version, reutilizar una credencial revocada y ejecutar una herramienta sin permiso. El MVP solo avanza si detecta los tres casos y deja evidencia legible.
4. Probar si una credencial verificable reduce el tiempo para integrar un agente externo frente a intercambio manual de documentacion.

## Fuentes y criterio

Los metadatos, DOI, tipo de publicacion, disponibilidad y senales de citacion se contrastaron mediante OpenAlex el 2026-09-29. Las revisiones y surveys se usan para delimitar el estado del arte; los prototipos recientes se tratan como evidencia exploratoria, no como consenso. No se han leido experimentalmente todos los textos completos en esta primera pasada, por lo que las afirmaciones de rendimiento deben verificarse antes de incorporarse a una especificacion.
