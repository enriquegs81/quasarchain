# Piloto experimental de bajo riesgo

Fecha: 2026-09-29.

## Objetivo

Validar si un responsable de IA, plataforma o seguridad entiende y valora una capa de verificacion para agentes sin conectar sistemas productivos ni procesar datos reales.

El piloto valida comprension, utilidad percibida y prioridad del problema. No valida seguridad en produccion, cumplimiento normativo ni capacidad para operar como proveedor critico.

## Hipotesis

> Si mostramos a un equipo un agente simulado que tiene identidad, permisos y evidencias verificables, el equipo podra identificar un coste actual de trazabilidad y describiria un caso para probarlo.

## Limites de responsabilidad

Este experimento debe cumplir todos estos limites:

- No usar datos personales, secretos, prompts reales ni informacion confidencial.
- No conectar APIs, wallets, bases de datos ni sistemas productivos del participante.
- No permitir acciones reales del agente.
- No custodiar claves, fondos ni credenciales del participante.
- No emitir una certificacion de seguridad ni afirmar que el agente es confiable.
- No tomar decisiones sobre personas, credito, empleo, salud o acceso a servicios.
- No publicar identidades, empresas o resultados sin permiso escrito.
- No depender del dominio `.crypto` para que la prueba funcione.
- No ofrecer SLA, garantia de disponibilidad ni promesa de prevencion de incidentes.

El participante solo revisa un entorno de demostracion y datos sinteticos. Aunque estos limites reducen mucho la exposicion, no deben interpretarse como una eliminacion automatica de responsabilidades legales; para un piloto con una empresa conviene usar una autorizacion escrita y revisar las condiciones con asesoramiento legal.

## Formato

- Duracion: 30-45 minutos por sesion.
- Participantes: 5-10 responsables de IA, plataforma, seguridad o compliance.
- Entorno: demo local o pantalla compartida.
- Datos: agente `support-triage-demo`, cliente ficticio y diez eventos sinteticos.
- Herramienta: `support_api` simulada.
- Coste tecnico: cero si se ejecuta localmente con el workspace actual; cualquier hosting publico es opcional.
- Resultado: notas anonimizadas, objeciones y decision sobre el siguiente experimento.

## Guion de la sesion

1. Mostrar un agente sin controles y preguntar que informacion faltaria para aprobarlo.
2. Mostrar el mismo agente con manifiesto firmado.
3. Ejecutar una lectura permitida.
4. Intentar una operacion no declarada.
5. Solicitar una exportacion que requiere revision humana.
6. Revocar el manifiesto y repetir la accion.
7. Pedir al participante que explique que ocurrio usando solo la consola.
8. Preguntar por el ultimo incidente, auditoria o integracion donde esa evidencia hubiera ahorrado tiempo.
9. Presentar un posible piloto futuro, sin solicitar acceso a sus sistemas actuales.

## Preguntas clave

- Que parte de la evidencia considera imprescindible?
- Quien deberia aprobar una accion sensible?
- Que sistema interno tendria que recibir estos eventos?
- Cuanto tiempo dedica hoy a reconstruir acciones de agentes?
- Que riesgo le impediria probarlo?
- En que condiciones autorizaria una prueba con datos sinteticos?
- Quien tendria presupuesto para resolver este problema?

## Metricas y umbrales

### Señal de problema

- 6 de 10 participantes describen un coste, incidente o auditoria relacionada con permisos, versiones o trazabilidad.

### Señal de comprension

- 8 de 10 explican el producto como control o evidencia, sin describirlo como una blockchain o un token.
- 8 de 10 pueden explicar por que una operacion fue permitida, revisada o bloqueada.

### Señal de siguiente paso

- 4 de 10 aceptan repetir la prueba con un caso sintetico propio.
- 2 de 10 aceptan discutir un piloto controlado y no productivo.

### Criterios de parada

Detener o rediseñar el experimento si:

- alguien solicita conectar datos productivos antes de validar el problema;
- el participante interpreta la demo como certificacion de seguridad;
- se solicitan acciones reales sobre dinero, personas o sistemas criticos;
- no se puede mantener la separacion entre datos del participante y datos de demo;
- aparecen requisitos legales o contractuales que no pueden revisarse antes de continuar.

## Coste y responsabilidades

La primera ronda puede hacerse sin cobrar ni pagar por infraestructura adicional. Los costes son principalmente tiempo de preparacion y entrevistas.

No debe presentarse como "piloto sin responsabilidad". La formulacion correcta es:

> demostracion controlada, con datos sinteticos y sin acceso a produccion, para descubrir requisitos y validar utilidad.

Antes de un piloto pagado o conectado a sistemas reales se deben revisar contrato, tratamiento de datos, seguridad, retencion, responsabilidad, seguros y requisitos regulatorios.

## Decision posterior

- **Continuar:** se alcanza la señal de problema y hay dos interesados en una prueba controlada.
- **Ajustar:** existe dolor, pero el comprador, el mensaje o la evidencia no son claros.
- **Descartar:** no aparece un problema recurrente o el valor depende de asumir responsabilidades que el producto no puede controlar.
