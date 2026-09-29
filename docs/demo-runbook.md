# Runbook para probar la demo

## Opcion recomendada: demo guiada

Es la opción más sencilla para las primeras pruebas y no requiere publicar el servicio.

### Preparacion

1. Ejecuta la consola local:

```text
python -m quasar_verifier.console --port 8765
```

1. Abre `http://127.0.0.1:8765`.
1. Comparte la pantalla durante 15-20 minutos.
1. No compartas terminales con rutas privadas, claves ni datos reales.

### Guion de cinco minutos

1. Mostrar `support-triage.quasarchain.crypto` y su `agent_id`.
2. Abrir una ejecución `allow`.
3. Abrir una ejecución `review`.
4. Mostrar una operación `deny`.
5. Mostrar el hash de evidencia.
6. Preguntar qué información falta para confiar en el agente.

### Mensaje de invitación

> He creado una demo experimental de una capa de identidad y permisos para agentes de IA. Es local, usa datos sintéticos y no conecta ningún sistema real. ¿Te apetece verla durante 15 minutos y decirme qué entiendes y qué cambiarías?

## Opcion 2: prueba local desde el repositorio

Comparte el repositorio y estas instrucciones:

```powershell
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m quasar_verifier.demo --output docs/examples/demo-evidence.json
python -m quasar_verifier.console --port 8765
```

Después deben abrir:

```text
http://127.0.0.1:8765
```

Pide que respondan tres preguntas:

- ¿Qué agente aparece?
- ¿Qué acción fue bloqueada y por qué?
- ¿Qué demuestra el hash y qué no demuestra?

## Opcion 3: enlace público posterior

Solo cuando la demo esté clara, se puede publicar una instancia temporal para que otras personas la consulten.

Límites recomendados:

- Solo datos sintéticos.
- Sin endpoints de escritura.
- Sin subida de manifiestos de terceros.
- Sin autenticación basada únicamente en el dominio.
- Sin guardar prompts, respuestas ni identificadores personales.
- Apagar el servicio después de las pruebas.

No usaría un túnel público como primera opción: expone el ordenador local y añade riesgo operativo sin aportar mucho aprendizaje inicial.

## Registro de la prueba

Después de cada sesión anota en [interview-scorecard.md](interview-scorecard.md):

- qué entendió la persona sin explicación;
- qué parte le pareció útil;
- qué confundió;
- qué caso real mencionó;
- qué cambiaría;
- si repetiría la prueba.

No cuentes una visita como validación. Cuenta una prueba completa y una respuesta concreta.
