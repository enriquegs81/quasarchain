# MVP de QuasarChain Trust Layer

Fecha: 2026-09-29.

## Objetivo

Construir la version minima que permita comprobar esta hipotesis:

> Un equipo con un agente que accede a una API o dato sensible pagara por verificar su identidad, controlar sus permisos y reconstruir sus ejecuciones.

El MVP no intenta demostrar que todos los agentes sean confiables. Demuestra que una organizacion puede controlar y explicar acciones de un agente concreto.

## Usuario y escenario inicial

- Usuario: responsable de plataforma, seguridad o IA.
- Organizacion: equipo que ya ejecuta agentes en un entorno de prueba o produccion.
- Agente: uno que pueda leer datos o invocar una herramienta externa.
- Accion sensible: lectura de un recurso protegido, escritura en un sistema o llamada a una API con coste.
- Resultado esperado: permitir, bloquear o solicitar aprobacion y dejar evidencia verificable.

## Alcance incluido

### 1. Manifiesto del agente

Documento JSON firmado con:

- `agent_id`.
- `operator_id`.
- `version`.
- `capabilities`.
- `tools`.
- `permissions`.
- `issued_at` y `expires_at`.
- `revocation_endpoint`.

El manifiesto debe tener un esquema versionado. Los prompts, secretos y datos del cliente quedan fuera del manifiesto.

### 2. Verificacion

El verificador debe comprobar:

- firma valida;
- esquema valido;
- manifiesto no expirado;
- version identificable;
- agente no revocado;
- herramienta y permiso declarados.

Debe devolver un resultado legible para una persona y una respuesta estructurada para una API.

### 3. Politica de autorizacion

Tres decisiones son suficientes para el MVP:

- `allow`: la accion puede ejecutarse;
- `deny`: la accion se bloquea;
- `review`: requiere aprobacion humana.

La politica debe considerar como minimo agente, version, herramienta, permiso y entorno.

### 4. Evidencia de ejecucion

Cada intento registra:

- identificador del evento;
- agente y version;
- herramienta y permiso solicitado;
- decision de la politica;
- identidad del aprobador cuando exista;
- timestamp;
- resultado resumido;
- hash de la evidencia completa.

No se almacenan prompts, respuestas completas, secretos ni datos personales salvo que el piloto lo requiera y exista una politica expresa de retencion.

### 5. Consola minima

La consola debe permitir:

- registrar o importar un agente;
- consultar el estado del manifiesto;
- listar ejecuciones;
- filtrar por agente, herramienta, decision y fecha;
- abrir el detalle de un evento;
- exportar evidencia en JSON;
- revocar un manifiesto.

## Fuera de alcance

- Token propio.
- Custodia o movimiento de fondos.
- Escrow y pagos autonomos.
- Marketplace publico.
- Puntuacion global de reputacion.
- Soporte multi-chain como requisito.
- Anclaje permanente de todos los eventos en una blockchain.
- Integraciones con multiples frameworks antes de validar una.
- Almacenamiento de prompts o datos sensibles por defecto.

## Flujo de demostracion

1. El operador registra un agente y publica su manifiesto firmado.
2. El verificador confirma identidad, version, permisos y caducidad.
3. El agente intenta usar una herramienta autorizada.
4. La politica devuelve `allow` y se registra la evidencia.
5. El agente intenta una accion no declarada.
6. La politica devuelve `deny` y se registra el intento.
7. El agente intenta una accion que requiere supervision.
8. Un usuario aprueba o rechaza y la decision queda vinculada al evento.
9. El operador revoca el manifiesto.
10. Una nueva ejecucion con ese manifiesto es bloqueada y verificable.

## Criterios de aceptacion

### Funcionales

- Una firma alterada se detecta.
- Un manifiesto expirado se rechaza.
- Un manifiesto revocado se rechaza.
- Una herramienta no declarada se bloquea.
- Una accion `review` no se ejecuta sin decision humana.
- Cada intento genera un evento exportable.
- El evento permite responder quien, que, cuando, con que version y con que permiso.

### De experiencia

- Un desarrollador puede registrar el primer agente en menos de 30 minutos siguiendo la documentacion.
- Un responsable no tecnico puede interpretar el detalle de una ejecucion sin leer el formato JSON.
- La integracion de un agente piloto no supera un dia de trabajo.

### De validacion comercial

- Entrevistar 10 equipos del segmento elegido.
- Conseguir 4 pruebas con un agente real.
- Conseguir 2 conversaciones sobre un piloto pagado.
- Verificar que al menos 6 equipos describen un coste o incidente relacionado con permisos, versiones o trazabilidad.

## Arquitectura inicial

- API de manifiestos y verificacion.
- Motor de politicas independiente del modelo de IA.
- Adaptador o middleware delante de una herramienta concreta.
- Almacenamiento privado para eventos y evidencia.
- Hashes para detectar alteraciones.
- Anclaje publico opcional y posterior.
- Consola web minima para consulta y exportacion.

La identidad, custodia y autorizacion deben ser componentes separados. Una wallet puede firmar o representar una identidad, pero no debe convertirse automaticamente en permiso para actuar.

## Secuencia de construccion

### Fase 0: contrato del problema

- Tipo de agente elegido: agente de soporte interno.
- Herramienta elegida: `support_api` en un entorno sandbox.
- Operaciones iniciales: `customer.read`, `ticket.create` y `customer.export`.
- Politicas iniciales: lectura permitida, creacion de ticket permitida y exportacion sujeta a revision humana.
- Caso piloto: simular diez ejecuciones, incluyendo una operacion no declarada y una ejecucion posterior a la revocacion.
- Confirmar con un responsable de seguridad o plataforma que el evento contiene los campos que necesita revisar.

Salida: escenario reproducible, esquema inicial del manifiesto y [ejemplo de manifiesto v1](examples/agent-manifest.v1.json).

#### Matriz de pruebas de Fase 0

| Caso | Accion | Resultado esperado | Evidencia minima |
| --- | --- | --- | --- |
| P-01 | `customer.read` con manifiesto valido | `allow` | Agente, version, permiso y timestamp |
| P-02 | `ticket.create` con manifiesto valido | `allow` | Herramienta, decision y resultado resumido |
| P-03 | `customer.export` sin aprobacion | `review` y no ejecutar | Estado pendiente y aprobador ausente |
| P-04 | Operacion no declarada | `deny` | Permiso solicitado y regla aplicada |
| P-05 | Manifiesto alterado | Rechazo antes de ejecutar | Motivo de firma invalida |
| P-06 | Manifiesto revocado | Rechazo antes de ejecutar | Estado de revocacion y timestamp |

La Fase 0 termina cuando el escenario puede repetirse con los mismos resultados y una persona externa confirma que la evidencia responde quien actuo, que intento hacer y por que se permitio o bloqueo.

### Fase 1: verificador local

- Implementar esquema, firma, expiracion y revocacion.
- Crear casos de prueba para manifiesto valido, alterado y revocado.

Salida: CLI o API que devuelve una decision verificable.

### Fase 2: gateway y evidencia

- Interceptar una herramienta: implementado en `PolicyGateway` para `support_api`.
- Aplicar `allow`, `deny` y `review`: implementado con verificacion del manifiesto en cada intento.
- Crear eventos y exportarlos: implementado como `EvidenceEvent` serializable, con hash SHA-256 de la evidencia.
- Registrar el identificador de aprobacion humana cuando una operacion `review` se autoriza.

Salida actual: gateway local probado con operaciones permitidas, no declaradas, sujetas a revision y revocadas. El demo de `support_api` genera diez ejecuciones y exporta sus eventos en [demo-evidence.json](examples/demo-evidence.json).

### Fase 3: consola y piloto

- Mostrar agentes, eventos y decisiones: implementado en `web/console.html`.
- Servir evidencia local mediante `/api/summary` y `/api/events`: implementado en `quasar_verifier.console`.
- Incorporar un agente real: pendiente del piloto.
- Medir tiempo de instalacion, errores y comprension del usuario: pendiente de entrevistas y prueba con cliente.

Salida actual: consola local navegable sobre diez eventos de demo. Salida objetivo: piloto de 30 dias y decision de continuar, ajustar o descartar.

## Decision de avance

Avanzar hacia un producto comercial si se cumplen simultaneamente:

1. Los tres casos de seguridad funcionan: alteracion, revocacion y permiso insuficiente.
2. El primer agente se integra en menos de un dia.
3. Cuatro equipos aceptan probarlo con un agente real.
4. Dos equipos aceptan discutir pago.

Si falla la parte tecnica, reducir el numero de herramientas y entornos. Si falla la comprension, cambiar el mensaje y la interfaz. Si existe dolor pero no pago, probar proveedores de agentes como comprador antes de añadir funcionalidades.
