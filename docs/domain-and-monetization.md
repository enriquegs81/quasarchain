# Estudio de dominio y monetizacion

Fecha de corte: 2026-09-29.

## Tesis ejecutiva

`quasarchain.crypto` puede funcionar como marca para una **Trust Layer de agentes de IA**, siempre que el producto se presente como infraestructura de control, evidencia y autorizacion, no como una nueva blockchain ni como un activo especulativo.

La promesa comercial debe ser:

> Saber que agente actuo, con que identidad, version y permisos, y poder demostrarlo despues.

El comprador no paga por "usar blockchain". Paga por reducir riesgo operativo, acelerar revisiones de seguridad y compliance, y hacer menos costosa la integracion de agentes propios o externos.

La recomendacion inicial es un SaaS B2B por organizacion, con limites de agentes, entornos y eventos auditados. La API de verificacion puede tener cobro por uso cuando exista integracion externa. No se recomienda token propio, custodia de fondos ni marketplace como punto de partida.

## 1. Lectura del dominio

### Fortalezas

- `Quasar` sugiere energia, inteligencia y alcance; tiene mas personalidad que una marca puramente descriptiva.
- `Chain` comunica relaciones, trazabilidad y verificabilidad, conceptos compatibles con identidad y evidencia.
- `.crypto` ayuda a situar el proyecto en identidad digital, wallets y activos verificables.
- El nombre permite extender la marca: Trust Layer, Agent Passport, Verifier y Registry.

### Debilidades y riesgos

- `Chain` puede hacer pensar en una blockchain propia, una criptomoneda o un proyecto especulativo.
- `.crypto` puede reducir la credibilidad inicial ante compradores enterprise que no trabajen en Web3.
- El nombre no explica por si solo agentes, autorizacion, auditoria ni compliance.
- Un dominio no prueba legitimidad, seguridad ni calidad del agente registrado.
- La disponibilidad, propiedad, renovacion y compatibilidad tecnica del dominio deben verificarse antes de convertirlo en dependencia del producto.

### Posicionamiento recomendado

Usar el dominio como marca paraguas y explicar siempre la categoria en el subtitulo:

**QuasarChain — Trust infrastructure for AI agents.**

En español, para entrevistas y ventas:

**La capa de confianza para agentes que actuan con permisos reales.**

Evitar como mensaje principal:

- "La blockchain de los agentes".
- "Reputacion inmutable de IA".
- "Agentes autonomos sin limites".
- "Seguridad garantizada por blockchain".

El primer sitio deberia ser un verificador y una consola de confianza, no una pagina de token. La experiencia visible puede incluir una pagina publica de verificacion para manifiestos y credenciales, y una consola privada para politicas, trazas y revisiones.

## 2. Producto que puede cobrar

### Trust Layer inicial

1. **Agent Manifest**: identidad, operador, version, capacidades declaradas, herramientas, permisos, caducidad y contacto de revocacion.
2. **Verification API**: comprueba firma, esquema, version, caducidad y estado de revocacion.
3. **Policy Gateway**: permite, deniega o solicita aprobacion humana antes de una accion sensible.
4. **Execution Evidence**: registra agente, version, herramienta, permiso, timestamp, resultado resumido y hash de evidencia; excluye prompts y datos privados por defecto.
5. **Audit Console**: filtra eventos por agente, herramienta, permiso, entorno e incidente.
6. **Risk Context**: muestra evidencias separadas de disponibilidad, cumplimiento de politica, incidentes y calidad por tarea; no las comprime inicialmente en una puntuacion unica.

La cadena o anclaje publico se usa solo cuando mejora la verificabilidad entre organizaciones. La autorizacion operativa, los datos sensibles y la retencion deben poder funcionar fuera de la cadena.

### Unidad de valor

La unidad que mejor conecta coste y valor es el **agente gobernado** dentro de una organizacion, con un limite razonable de eventos auditados. Cobrar solo por tokens o llamadas puede penalizar la adopcion y parecer un coste de infraestructura. Cobrar solo por agente puede desalinearse con despliegues masivos.

Por eso conviene combinar:

- cuota fija por organizacion;
- limite de agentes y entornos;
- eventos auditados incluidos;
- exceso medido por eventos o volumen;
- funciones enterprise por contrato.

## 3. Segmentos prioritarios

| Segmento | Dolor comprable | Comprador probable | Entrada recomendada | Prioridad |
| --- | --- | --- | --- | --- |
| Empresas que despliegan agentes con acceso a datos o APIs sensibles | No pueden reconstruir permisos, versiones y acciones durante un incidente | Head of AI, seguridad, plataforma o compliance | Piloto con un agente de alto riesgo | 1 |
| Proveedores de agentes B2B | Cada cliente pide documentacion, limites y evidencias distintas | CTO, producto o seguridad | Passport y Verification API embebible | 2 |
| Integradores y marketplaces | Necesitan decidir que agentes aceptar y como revocar acceso | Platform lead o trust and safety | Registry privado y credenciales | 3 |
| Empresas crypto con tesoreria o automatizacion | Riesgo financiero y necesidad de aprobaciones | Security lead o operations | Politicas y aprobacion humana | 4 |
| Auditores y consultoras | Necesitan recolectar evidencia de controles | Socio de riesgo o compliance | Exportes y workspace por cliente | 5 |

El primer segmento es preferible porque tiene un dolor interno, una autoridad de compra identificable y no exige resolver de entrada un estandar de mercado entre muchas organizaciones.

## 4. Modelos de monetizacion

| Modelo | Ventaja | Riesgo | Veredicto |
| --- | --- | --- | --- |
| SaaS por organizacion y agentes | Ingreso predecible y facil de presupuestar | Hay que definir limites que no frenen pruebas | Modelo inicial |
| Precio por evento auditado | Escala con uso y refleja volumen | Penaliza instrumentacion y puede ser dificil de prever | Add-on o exceso |
| API de verificacion | Encaja con proveedores y marketplaces | Puede convertirse en commodity | Segunda via |
| Plan enterprise/self-hosted | Resuelve residencia de datos, SSO y redes privadas | Ventas mas lentas y soporte costoso | Cuando haya demanda |
| Servicios de integracion | Financia los primeros despliegues y aprendizaje | No escala como producto | Complemento limitado |
| Registry o marketplace premium | Posible efecto red y descubrimiento | Problema de liquidez, responsabilidad y moderacion | Fase posterior |
| Token propio | Puede financiar comunidad | Regulacion, especulacion y distrae de la utilidad | No recomendado |
| Custodia, escrow o pagos autonomos | Captura valor transaccional | Riesgo legal, fraude y disputas | No en el MVP |

## 5. Pricing inicial para validar, no para fijar mercado

Los precios siguientes son hipotesis de entrevista, no una afirmacion de disposicion a pagar.

### Developer / piloto

- Gratis o precio simbolico.
- 1 organizacion, 3 agentes, 1 entorno y 10.000 eventos auditados al mes.
- Manifiestos firmados, verificador y consola basica.
- Objetivo: reducir friccion de instalacion y conseguir evidencia de uso real.

### Team

- Referencia a probar: 300-800 EUR al mes.
- Hasta 25 agentes, varios entornos, politicas, revocacion, exportes y retencion ampliada.
- Soporte por email y una integracion principal.
- Comprador: equipo de plataforma o seguridad.

### Business

- Referencia a probar: 1.500-4.000 EUR al mes.
- Agentes y eventos ampliados, SSO, RBAC, webhooks, API de verificacion, alertas y evidencias para auditoria.
- Precio final dependiente de volumen, retencion y requisitos de despliegue.

### Enterprise

- Precio anual negociado.
- Despliegue privado o self-hosted, residencia de datos, SLA, integraciones, soporte de compliance y contrato de seguridad.
- No venderlo antes de que un piloto revele requisitos repetidos entre clientes.

### Servicios

Cobrar por integracion solo cuando acelere el primer valor: adaptadores, modelado de politicas, migracion de trazas o preparacion de controles. Mantenerlo separado de la suscripcion para no ocultar el coste real del producto.

## 6. Diferenciacion defendible

QuasarChain no deberia competir como:

- un SIEM generalista;
- una plataforma de observabilidad de LLM;
- un IAM tradicional;
- un gateway de herramientas sin evidencia portable;
- un benchmark que asigna una nota global a cada agente.

La posicion defendible es unir cuatro elementos que suelen estar separados:

1. identidad y manifiesto verificables;
2. autorizacion contextual y revocable;
3. evidencia portable de ejecuciones;
4. integracion para agentes externos sin exponer prompts ni datos privados.

La defensa real no sera el dominio ni el uso de blockchain. Sera el esquema de evidencia, las integraciones, el conocimiento de politicas y los datos operativos obtenidos con consentimiento.

## 7. Riesgos de producto y respuesta

- **Confundir integridad con verdad:** indicar que una firma demuestra quien firmo y que el registro no cambio, no que la accion fuera correcta.
- **Exceso de privacidad:** almacenar hashes, referencias y metadatos minimos; mantener prompts y datos fuera de la cadena.
- **Identidad mal definida:** separar operador, propietario, modelo, instancia y wallet; permitir rotacion y revocacion.
- **Falsa sensacion de seguridad:** mostrar politicas aplicadas y fallos detectados, no una garantia general.
- **Dependencia del ecosistema crypto:** ofrecer verificacion web y API convencional; hacer opcional el anclaje publico.
- **Ventas demasiado amplias:** empezar con un workflow de alto riesgo y un solo comprador interno.
- **Coste de integracion:** priorizar SDK, webhooks y un adaptador para una plataforma de agentes que el segmento ya use.

## 8. Experimento comercial de 7 dias

### Preparacion

- Seleccionar 10 equipos que ya ejecuten agentes con acceso a APIs, datos sensibles o acciones de escritura.
- Preparar un demo con un agente, un manifiesto firmado, tres politicas y diez ejecuciones.

### Entrevistas y prueba

- Preguntar por el ultimo incidente o auditoria donde faltaran identidad, permiso, version o evidencia.
- Pedir que conecten un agente de prueba o que revisen trazas simuladas.
- Presentar dos ofertas: Team y Business, sin negociar funcionalidades a medida.
- Preguntar que presupuesto o aprobacion seria necesario para un piloto de 30 dias.

### Metricas y umbrales

- 6 de 10 equipos describen un coste recurrente o incidente relacionado con trazabilidad y control.
- 4 de 10 aceptan una prueba con un agente real.
- 2 de 10 aceptan discutir un piloto pagado o aportar un sponsor interno.
- El primer agente se integra en menos de un dia de trabajo.
- El usuario puede verificar un evento y explicar el permiso aplicado sin ayuda del fundador.

Si no se alcanza el primer umbral, revisar el problema antes de seguir construyendo. Si hay dolor pero no pago, probar un comprador distinto: proveedor de agentes o integrador. Si hay pago por integracion pero no por suscripcion, limitar servicios y buscar el componente repetible.

## Decision provisional

1. Mantener `quasarchain.crypto` como marca paraguas.
2. Lanzar un verificador y una Trust Layer privada para equipos con agentes de riesgo.
3. Monetizar primero por organizacion y capacidad gobernada; añadir uso de API despues.
4. Usar Agent Passport como modulo de expansion para agentes externos.
5. Posponer token, marketplace, escrow y custodia hasta demostrar demanda y resolver responsabilidades.

Esta decision debe cambiar si las entrevistas muestran que el dolor principal es otro, que los compradores ya resuelven el problema con herramientas existentes o que el dominio genera una desconfianza mayor que su valor de marca.
