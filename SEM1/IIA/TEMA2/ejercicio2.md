# Ejercicio 2 — Descripción PEAS de agentes inteligentes

## Contexto

En el capítulo 2 de *Artificial Intelligence: A Modern Approach* (Russell & Norvig),
un agente se entiende mejor cuando se especifica su **entorno de tarea**. Una forma
estándar de hacerlo es la descripción **PEAS**:

| Letra | Significado | Pregunta guía |
|---|---|---|
| **P** | *Performance* (medida de desempeño) | ¿Cómo se evalúa el éxito del agente? |
| **E** | *Environment* (entorno) | ¿En qué mundo opera? ¿Quién más actúa ahí? |
| **A** | *Actuators* (actuadores) | ¿Qué acciones puede ejecutar? |
| **S** | *Sensors* (sensores) | ¿Qué información puede percibir? |

Este ejercicio **no requiere programar**. Consiste en analizar distintos tipos de
aplicaciones reales y describir cada una con el esquema PEAS.

## Objetivo

Para cada una de las **8 aplicaciones** listadas abajo, redacta una descripción
PEAS completa y coherente. Debes pensar como diseñador del agente: qué optimiza,
dónde actúa, con qué puede mover o modificar el mundo, y qué puede observar.

## Aplicaciones a analizar

Describe PEAS para cada una de estas aplicaciones:

1. **Asistente virtual de voz** (p. ej. Siri, Alexa o Google Assistant en un altavoz inteligente).
2. **Robot aspirador doméstico** (p. ej. Roomba u otro robot que limpia pisos de un departamento).
3. **Sistema de recomendación de streaming** (p. ej. Netflix o Spotify que sugiere películas o canciones).
4. **Vehículo autónomo en ciudad** (conducción sin conductor en calles urbanas con tráfico y peatones).
5. **Agente de trading algorítmico en bolsa** (compra y venta automática de acciones en mercados financieros).
6. **Sistema de diagnóstico médico asistido por IA** (apoya a un médico a interpretar síntomas e imágenes clínicas).
7. **Dron de inspección de infraestructura** (revisa grietas, corrosión o fugas en puentes, tuberías o líneas eléctricas).
8. **Agente jugador de ajedrez** (programa que compite contra un humano u otro agente en partidas completas).

## Instrucciones

Para **cada** aplicación entrega una sección con este formato:

```markdown
### N. Nombre de la aplicación

- **Performance:** ...
- **Environment:** ...
- **Actuators:** ...
- **Sensors:** ...
```

### Criterios de calidad

- **Performance:** incluye métricas concretas (precisión, tiempo, costo, satisfacción del usuario, ganancia, seguridad, etc.), no solo “hacerlo bien”.
- **Environment:** menciona si es parcialmente observable o totalmente observable, si es estocástico o determinista, episódico o secuencial, estático o dinámico, y discreto o continuo (según aplique).
- **Actuators:** lista acciones reales que el agente puede ejecutar, no capacidades vagas.
- **Sensors:** lista percepciones concretas (cámara, micrófono, API, historial de usuario, cotizaciones de mercado, etc.).

### Ejemplo breve (solo como referencia de formato)

**Aplicación:** termostato inteligente de una casa.

- **Performance:** mantener la temperatura deseada con mínimo consumo de energía y máxima comodidad del habitante.
- **Environment:** interior de una vivienda; cambia con clima exterior, ventanas abiertas y presencia de personas.
- **Actuators:** encender/apagar calefacción o aire acondicionado; ajustar temperatura objetivo; enviar alertas al usuario.
- **Sensors:** termómetro interior, horario, presencia (movimiento), lectura de clima exterior vía internet.

> El termostato **no** está en la lista de las 8 aplicaciones: es solo un ejemplo.
> Debes completar las ocho aplicaciones indicadas arriba.

## Entrega

Un documento (Markdown o PDF) con las **8 descripciones PEAS**, numeradas y con título
claro para cada aplicación.

Opcional pero recomendado: al final de cada descripción, añade **2–3 líneas** que
justifiquen por qué clasificaste el entorno como observable/estocástico/secuencial/etc.

## Criterios de aceptación

- No usar IA para generar las respuestas de este ejercicio.
- Hay exactamente **8** descripciones PEAS, una por cada aplicación de la lista.
- Cada descripción tiene los cuatro componentes (**P**, **E**, **A**, **S**) claramente identificados.
- Las respuestas son específicas de la aplicación (evita copiar la misma descripción genérica para todas).
- El entorno (**E**) incluye al menos una clasificación AIMA (p. ej. parcialmente observable, estocástico, secuencial).
- Redacción clara, en español, sin ambigüedades evidentes.

## Pistas

- Un mismo tipo de agente puede tener **distintos PEAS** según el contexto: un dron de inspección en un túnel no es igual que uno en un campo abierto.
- **Performance** y **Environment** suelen confundirse: la medida de desempeño dice *qué optimizas*; el entorno dice *dónde ocurre la tarea y qué condiciones enfrentas*.
- Si dudas entre dos sensores o actuadores, pregúntate: *¿esto lo usa el agente para decidir, o solo el humano que lo supervisa?* Solo cuenta lo que el **agente** percibe o controla.

## Solución
### 1. Asistente virtual de voz

- **Performance:** Satisfacción del usuario, accuracy de respuestas. 
- **Environment:** Físicos: Sala, habitación, cocina u oficina. Virtuales: Internet, servidores de amazon.
- **Actuators:** Bocinas integradas, pantalla integrada (de tenerla), text-to-speech, APIs (para búsqueda de música, búsqueda de internet, tienda de amazon, internet de las cosas, etc...).
- **Sensors:** Micrófono, cámara(a veces), integraciones con internet de las cosas (ej. sensor de temperatura), reloj / calendario, hooks para notificaciones de amazon.

  *Clasificación:* Parcialmente observable, no todos los modelos acceden a la cámara o IoT. Estocástico porque las acciones no determinan el estado futuro.

### 2. Robot aspirador doméstico

- **Performance:** Metros cuadrados limpiados, consumo (batería, materiales de limpieza), calidad de limpieza, precisión para reconocer suciedad.
- **Environment:** Sala, habitaciones, comedor, cocina, oficinas.
- **Actuators:** Ruedas, cepillos integrados, LEDs de aviso de status.
- **Sensors:** Cámaras, detectores de proximidad, indicador de batería, indicador de niveles de producto de limpieza.

  *Clasificación:* Parcialmente observable, el robot casi nunca puede conocer el status de toda la habitación en la que está. Estocástico, cuando ya limpiaste una parte, podría estar sucia al pasar de nuevo o no.

### 3. Sistema de recomendación de streaming

- **Performance:** Tiempo de retención del usuario, cantidad monetaria de ventas adicionales dentro de la plataforma (renta de películas fuera del catálogo base, mejora de planes).
- **Environment:** Catálogo de contenido disponible, usuarios / suscriptores del servicio.
- **Actuators:** Menú de selección de contenido, APIs de notificación de recomendaciones (mail, celular).
- **Sensors:** Base de datos de cliente, historial de reproducción, tiempo de visualización, tiempo de inactividad, propensión de desuscribir (churn).

  *Clasificación:* Parcialmente observable, hace falta el consumo fuera de la plataforma. Estocástico, Recomendar o no recomendar no garantiza ver o no ver una película o serie o música.

### 4. Vehículo autónomo en ciudad

- **Performance:** Velocidad de llegada, número de choques, satisfacción del usuario, satisfacción de otros vehículos, accuracy de reconocimiento de objetos.
- **Environment:** Calles, carreteras. En Mérida México: Baches, Limunarias, peatones, otros vehículos, paradas de policía, semáforos, calles sin pavimentar, señales o letreros de tránsito.
- **Actuators:** Volante, pantalla, sistema de velocidades, acelerador, frenos, luces, claxon, bocinas integradas.
- **Sensors:** Cámara, detector de proximidad, GPS.

  *Clasificación:* Parcialmente observable, el vehículo no puede identificar todo siempre debido a puntos ciegos etc. Estocástico, puedes presionar el acelerador a fondo y aún así no avanzar nada.

### 5. Agente de trading algorítmico en bolsa

- **Performance:** Rendimientos, indicadores de riesgo, velocidad de cálculo de operaciones (buy, call, short, etc.), tasa de aciertos en subida / bajada.
- **Environment:** Bolsas del mundo, economía nacional / internacional.
- **Actuators:** Crear o modificar órdenes de compra / venta, notificación a usuarios.
- **Sensors:** Indicadores macroeconómicos, índices bursátiles, reportes / indicadores financieros y de riesgo por empresa / fondo, sensor de tendencias alcistas o bajistas, percepción económica global (alta o baja generales).

  *Clasificación:* Parcialmente observable (La bolsa depende de variables exógenas). Estocástico, movimientos pasados no garantizan movimientos futuros en un random walk.

### 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** El recall del diagnóstico.
- **Environment:** Hospital o clínica. Tiempos de espera para consultas elevados.
- **Actuators:** Generador de reportes médicos con pruebas, análisis médicos etc. Sistema de alertas y medicación.
- **Sensors:** Historial médico del paciente, resultados de análisis, características físicas (altura, peso), listado y descripción de síntomas, rayos X, imágenes de heridas o edemas.

  *Clasificación:* Parcialmente observable (Casi nunca es posible saber el historial completo del paciente). Estocástico, Hoy estaba saludable y mañana sufe un infarto.

### 7. Dron de inspección de infraestructura

- **Performance:** Metros cúbicos evaluados (por hora, sesión, etc.), precisión para identificar defectos (grietas, corrosión, fugas, humedad, etc...).
- **Environment:** Campo, proyectos en obra negra / gris, puentes, vías, casas, cualquier edificación, característias climáticas (calor, humedad, lluvia, etc.) y de uso de drones en espacios abiertos.
- **Actuators:** Sistemas de movimiento (rotación, traslación), estabilizador, luces, antena para notificación y comunicación con el operador / servidor.
- **Sensors:** Cámara e identificador de objetos, batería, sensor de proximidad y movimiento, GPS, sistemas de status del dron, receptor de señales del operador del dron.

  *Clasificación:* Parcialmente observable. Estocástico, Las plantas rompieron la banqueta a los 5 años.

### 8. Agente jugador de ajedrez

- **Performance:** Porcentaje de victorias o derrotas, tiempo cálculo y movimiento.
- **Environment:** Tablero de ajedrez.
- **Actuators:** Movimiento de una pieza, solicitar tablas.
- **Sensors:** Registro de movimientos en el tablero, estado del tablero actual, tiempo restante en el reloj.

  *Clasificación:* Totalmente observable (por default). Determinista, acciones pasadas determinan el estado actual y acciones futuras el estado futuro con exactitud.