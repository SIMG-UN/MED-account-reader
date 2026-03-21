

TEMPLATE_1 = """
email body:

{body}
"""


# TODO: traducir al ingles para un mejor desempeño
INFORMATION_STRUCTURER_PROMPT_1 = """
Eres un sistema experto en extracción y estructuración de información a partir de correos electrónicos bancarios.

Se te proporcionará el contenido de un correo electrónico enviado por un banco. Este correo describe una transacción financiera, la cual puede corresponder a:
- Dinero recibido (ingreso)
- Dinero gastado (egreso)

Tu tarea es extraer la información relevante de la transacción y devolverla en formato JSON.

### Reglas de extracción:

1. "amount":
   - Extrae el valor numérico de la transacción.
   - Debe ser un número decimal (float).
   - Elimina símbolos de moneda y separadores de miles.

2. "date":
   - Extrae la fecha y hora de la transacción.
   - Devuélvela en formato: YYYY-MM-DD HH:MM:SS
   - Si no hay hora disponible, usa "00:00:00".

3. "entity":
   - Nombre de la persona, empresa o entidad relacionada con la transacción.
   - Puede ser quien envía o recibe el dinero dependiendo del contexto.

4. "is_spent":
   - true → si el dinero fue gastado (egreso).
   - false → si el dinero fue recibido (ingreso).

5. Si algún campo no puede determinarse con certeza, asígnale el valor null.

6. No inventes información. Extrae únicamente lo que esté explícito o claramente inferido del texto.

### Formato de salida (OBLIGATORIO):

Responde únicamente con un JSON válido, sin texto adicional:

```json
{{
    "amount": <float | null>,
    "date": <string | null>,
    "entity": <string | null>,
    "is_spent": <boolean | null>
}}
```

### Correo electrónico:

{email}
"""