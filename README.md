<div align="center">

# MiAPI

**Inspeccioná cómo responde una API sin necesitar una herramienta pesada.**

[![CI](https://github.com/amoedo7/MiAPI/actions/workflows/ci.yml/badge.svg)](https://github.com/amoedo7/MiAPI/actions/workflows/ci.yml)

`HTTP` · `JSON` · `latencia` · `headers` · `Android / Windows / macOS / Linux`
</div>

---

## Qué muestra

MiAPI hace una petición explícita a un endpoint y devuelve:

- método y URL final;
- status HTTP;
- tiempo observado;
- tamaño de respuesta;
- Content-Type;
- headers de respuesta;
- si el body es JSON válido;
- una vista previa opcional;
- nombres de headers enviados, **nunca sus valores en el reporte**.

## Ejecutar

```bash
python miapi.py https://api.github.com
```

POST JSON:

```bash
python miapi.py https://example.com/api --method POST --json '{"demo":true}'
```

Agregar un header público:

```bash
python miapi.py https://example.com --header 'Accept: application/json'
```

Guardar reporte:

```bash
python miapi.py https://example.com --output api.json
```

Para evitar exponer secretos en historial de shell o logs, no recomendamos pasar tokens reales en demos públicas.

## Contrato

```json
{
  "schema": "desarrollamo.miapi.v1",
  "request": {"method": "GET", "url": "https://example.com"},
  "response": {"status": 200, "elapsed_ms": 184, "is_json": false}
}
```

---

**DesarrollAMO** · una integración empieza por entender exactamente qué entra y qué vuelve.
