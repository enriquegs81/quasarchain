# quasarchain.crypto: workspace de exploracion

Este repositorio contiene un proyecto de hobby para explorar una **Trust Layer educativa para agentes de IA** alrededor de `quasarchain.crypto`.

La demo muestra cómo un agente puede tener identidad, permisos y evidencia de ejecución. No es un producto de seguridad, una certificación, una blockchain nueva ni un sistema preparado para producción.

## Qué se está aprendiendo

- Cómo firmar y verificar manifiestos de agentes con Ed25519.
- Cómo aplicar políticas `allow`, `review` y `deny`.
- Cómo registrar evidencias sin almacenar prompts ni datos sensibles.
- Cómo revocar un agente y detectar operaciones no declaradas.
- Cómo podría funcionar un dominio `.crypto` como nombre legible y portal de verificación.

## Arquitectura de la demo

```text
Manifiesto firmado
|
v
Verificador Ed25519
|
v
PolicyGateway: allow / review / deny
|
v
EvidenceEvent con hash SHA-256
|
v
Consola local de auditoria
```

El dominio `.crypto` no es una dependencia técnica de la demo. La identidad criptográfica y la evidencia deben seguir funcionando aunque el dominio no esté disponible.

## Abrir el workspace

Abre `quasarchain-ideas.code-workspace` en VS Code.

## Flujo recomendado

1. Ejecuta el prompt `.github/prompts/quasarchain-solutions.prompt.md` con una pregunta o problema concreto.
2. Registra cada idea en `docs/hypotheses.md` como una hipotesis falsable.
3. Usa `docs/decision-matrix.md` para comparar opciones con la misma escala.
4. Documenta hechos, supuestos y preguntas pendientes en `docs/research-notes.md`.
5. No implementes nada hasta que exista un experimento pequeno con una metrica y un criterio de decision.

## Estructura

- `.github/prompts/`: prompt reutilizable para explorar soluciones.
- `.github/prompts/quantum-scientific-innovation.prompt.md`: prompt para diseñar y criticar experimentos cuánticos falsables.
- `docs/hypotheses.md`: registro de hipotesis y experimentos.
- `docs/decision-matrix.md`: criterios de priorizacion.
- `docs/ideas-quasarchain-crypto.md`: mapa inicial de oportunidades y recomendacion.
- `docs/domain-and-monetization.md`: estudio del dominio, posicionamiento, segmentos, pricing y experimento comercial.
- `docs/mvp-trust-layer.md`: alcance, flujo, arquitectura y criterios de aceptacion del MVP.
- `docs/pilot-experiment.md`: protocolo de demo controlada con datos sinteticos y limites de responsabilidad.
- `docs/interview-scorecard.md`: ficha anonima para registrar entrevistas y decidir el siguiente paso.
- `docs/demo-runbook.md`: formas seguras de compartir y probar la demo.
- `docs/visibility-starter-kit.md`: mensajes, perfiles objetivo, canales y agenda inicial de visibilidad.
- `docs/quantum-learning-plan.md`: ruta de aprendizaje y primer laboratorio de computación cuántica.
- `docs/quantum-experiment-passport.md`: nota técnica reproducible del laboratorio Bell y su recibo firmado.
- `docs/quantum-visibility-kit.md`: release, citación y comunicación académica del laboratorio cuántico.
- `docs/academic-release-brief.md`: resumen público y académico del release candidate.
- `src/quasar_verifier/agentic_quantum.py`: flujo de propuesta, política, aprobación y ejecución del agente cuántico.
- `src/quasar_verifier/qiskit_lab.py`: comparación del circuito Bell con Qiskit `BasicSimulator`.
- `src/quasar_verifier/replication.py`: informe de replicación diferencial y pasaporte firmado entre dos simuladores.
- `CITATION.cff`: metadatos de citación del prototipo.
- `docs/examples/agent-manifest.v1.json`: manifiesto de referencia para el escenario inicial.
- `docs/examples/demo-evidence.json`: diez eventos generados por el demo de `support_api`.
- `docs/examples/hardware-bell-snapshots-2026-10-02.json`: datos públicos de calibración y Bell en tres backends IBM.
- `docs/research-notes.md`: notas de investigacion y fuentes por verificar.
- `web/console.html`: consola local para consultar decisiones y evidencia.

## Ejecutar el verificador local

Instala las dependencias de desarrollo y ejecuta los tests:

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

El modulo de verificacion puede ejecutarse sobre un manifiesto JSON:

```text
python -m quasar_verifier ruta/al/manifiesto.json
```

La firma del manifiesto cubre su representacion JSON canonica, excepto el propio campo `signing.signature`. El ejemplo de `docs/examples/agent-manifest.v1.json` contiene una firma de marcador y sirve como contrato de estructura, no como credencial valida.

El gateway de politicas se importa desde `quasar_verifier.PolicyGateway`. Cada intento verifica de nuevo el manifiesto, aplica `allow`, `deny` o `review`, y devuelve un `EvidenceEvent` con hash de integridad y, cuando corresponde, el identificador de aprobacion humana.

Para ejecutar el escenario completo y exportar diez eventos:

```text
python -m quasar_verifier.demo --output docs/examples/demo-evidence.json
```

Para abrir la consola local:

```text
python -m quasar_verifier.console --port 8765
```

Abre `http://127.0.0.1:8765` en el navegador.

## Qué no hacer todavía

- No conectar APIs, bases de datos o wallets reales.
- No usar datos personales ni secretos.
- No custodiar fondos.
- No permitir acciones irreversibles.
- No presentar un agente como "seguro" por tener una firma.
- No publicar el dominio como si fuera una certificación.

## Próximos experimentos

1. Cambiar las operaciones y políticas del agente simulado.
2. Añadir tests para expiración, rotación de claves y nuevas reglas.
3. Compartir la demo con amigos técnicos y recoger preguntas.
4. Documentar qué partes del modelo de confianza resultan difíciles de entender.

El protocolo de una demostración controlada está en [docs/pilot-experiment.md](docs/pilot-experiment.md), y el kit para compartir el proyecto está en [docs/visibility-starter-kit.md](docs/visibility-starter-kit.md).
