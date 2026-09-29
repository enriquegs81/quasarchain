# Kit inicial de visibilidad

Fecha: 2026-09-29.

## Objetivo de la primera ronda

Conseguir conversaciones cualificadas con equipos que ya utilizan agentes de IA y descubrir si tienen un problema real de identidad, permisos o trazabilidad.

Esta ronda no busca maximizar visitas. Busca obtener cinco entrevistas y dos posibles pruebas controladas.

## Mensaje base

**QuasarChain** es una capa de confianza para agentes de IA que necesitan actuar con permisos reales.

Permite comprobar:

- qué agente actuó;
- con qué versión;
- qué herramienta intentó usar;
- qué permiso se aplicó;
- si la acción fue permitida, revisada o bloqueada;
- quién aprobó una excepción.

La demo actual funciona con un agente y una API simulados, datos sintéticos y sin conexión a producción.

## Frase corta

> Identity, permissions and evidence for AI agents.

## Descripción para perfil o publicación

> Estoy explorando QuasarChain, una Trust Layer para agentes de IA. La primera demo verifica manifiestos firmados, aplica permisos `allow`, `review` y `deny`, y genera evidencia auditable de cada intento. El experimento usa datos sintéticos y no conecta sistemas productivos. Busco hablar con equipos que ya estén desplegando agentes y quieran compartir qué controles necesitan.

## Mensaje de contacto

> Hola, [nombre]. Estoy validando una herramienta para controlar agentes de IA que acceden a APIs o datos sensibles. He preparado una demo local con datos sintéticos, sin acceso a producción ni venta. Me gustaría entender cómo resolvéis hoy la identidad, los permisos y la trazabilidad de esos agentes. ¿Tendrías 30 minutos para revisar la demo y decirme qué evidencia necesitarías antes de aprobar un agente?

## Personas a contactar

Priorizar perfiles con estos cargos o responsabilidades:

- Head of AI o AI Platform Lead.
- Engineering Manager de automatización.
- MLOps o Platform Engineer.
- Security Engineer o CISO en empresas con agentes.
- Responsible AI o AI Governance.
- Compliance tecnológico.
- Proveedor B2B de agentes.
- Consultor de automatización empresarial.

Evitar empezar por audiencias interesadas únicamente en tokens, trading o especulación crypto.

## Canales iniciales

1. Contactos profesionales directos.
2. LinkedIn con mensajes personalizados.
3. GitHub con README y demo reproducible.
4. Comunidades de AI engineering, MLOps, seguridad e identidad.
5. Consultoras que ya integren agentes en empresas.

No invertir todavía en anuncios, influencers ni campañas masivas.

## Contenido inicial

Publicar una pieza cada dos días, siempre con una invitación a conversar:

1. **Un agente no debería tener permisos implícitos**: ejemplo `customer.delete` bloqueado.
2. **Una firma no demuestra que una acción sea correcta**: diferencia entre integridad y verdad.
3. **Qué contiene un manifiesto de agente**: identidad, versión, capacidades y caducidad.
4. **Demo de revisión humana**: una exportación pasa de `review` a `allow` con aprobación.
5. **Revocación**: el mismo agente queda bloqueado después de revocar su manifiesto.

## Agenda de siete días

### Día 1: preparar

- Ejecutar el demo.
- Revisar que la consola carga diez eventos.
- Capturar tres imágenes: resumen, acción bloqueada y aprobación.
- Preparar un enlace al README y al protocolo del piloto.

### Día 2: publicar

- Publicar el mensaje base en un perfil profesional.
- Publicar el repositorio o una página de demo.
- Contactar con cinco personas conocidas del sector.

### Día 3: ampliar

- Contactar con cinco responsables de plataforma o seguridad.
- Publicar el caso de operación no declarada.
- Registrar respuestas sin datos confidenciales.

### Día 4: entrevistar

- Realizar las primeras entrevistas.
- Usar [interview-scorecard.md](interview-scorecard.md).
- No presentar precios todavía salvo que el participante los pregunte.

### Día 5: ajustar

- Comparar las palabras que usan los participantes.
- Cambiar el mensaje solo si se repite una confusión.
- Contactar con cinco proveedores o integradores de agentes.

### Día 6: demostrar

- Realizar entrevistas restantes.
- Ofrecer una repetición con un caso sintético del participante.
- Preguntar quién sería el comprador y qué aprobación necesitaría.

### Día 7: decidir

- Consolidar métricas.
- Mantener los resultados anonimizados.
- Elegir continuar, ajustar o descartar.

## Registro mínimo

| Métrica | Objetivo inicial |
| --- | ---: |
| Contactos personalizados | 20 |
| Respuestas relevantes | 8 |
| Entrevistas realizadas | 5 |
| Problemas reales descritos | 3 |
| Repeticiones de demo aceptadas | 2 |
| Pilotos controlados discutidos | 2 |

Las visitas, impresiones y likes son señales secundarias. No sustituyen entrevistas ni pruebas aceptadas.

## Reglas de comunicación

- Decir "verificable" y "auditable", no "seguro por defecto".
- Decir "demo controlada", no "piloto sin responsabilidad".
- No publicar nombres de participantes sin autorización.
- No mostrar datos, prompts, claves ni trazas reales.
- Explicar que `.crypto` es marca y namespace potencial, no prueba de seguridad.
- No anunciar token, rendimiento financiero ni agentes autónomos con fondos.

## Extension: quantum experiment visibility

The Bell-state laboratory has a separate English-language visibility kit in
[quantum-visibility-kit.md](quantum-visibility-kit.md). Use it when discussing
the Quantum Experiment Passport with academic or quantum-computing audiences.
Describe the result as a reproducibility and record-integrity prototype. Do not
call it a Bell test, a hardware benchmark, or a scientific certification.
