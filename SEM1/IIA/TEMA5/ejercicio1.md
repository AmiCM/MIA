# Ejercicio 1 — Más capas en el perceptrón multicapa (Iris)

## Contexto

En `Perceptrón multicapa/Notebooks/` hay dos notebooks que resuelven el mismo
problema: clasificar las **3 especies** del conjunto **Iris** (4 atributos:
sépalo/pétalo en largo y ancho). Ambas redes son un MLP con activación
**sigmoide**, error **MSE**, **SGD** con \(\eta = 0.03\) y **500 épocas**.

| Notebook | Cómo está implementada | Topología inicial |
|---|---|---|
| `01 Multilayer perceptron.ipynb` | A mano (NumPy): forward, error y backprop | \(4 \times 3 \times 3\) |
| `02 Keras - multilayer perceptron - iris.ipynb` | Keras / TensorFlow (`Sequential`) | \(4 \times 3 \times 3\) |

En la notebook 01, \(4 \times 3 \times 3\) significa: **4** entradas, **una**
capa oculta de **3** neuronas y **3** neuronas de salida (una por clase). En
Keras es lo mismo: dos `Dense(3)` (la primera con `input_shape=(4,)`).

En este ejercicio **sí vas a modificar código**, pero no el de
`Perceptrón multicapa/project/`. Trabajas **en Colab**, sobre **copias** de las
dos notebooks.

## Objetivo

Correr ambas notebooks en **Google Colab** con la arquitectura original,
**agregar dos capas** a cada red, volver a entrenar y **comparar** qué cambia
(curva de error/pérdida, velocidad, calidad de la clasificación).

## Archivos a crear / modificar

No modifiques las notebooks originales del repositorio.

1. Sube a Colab una **copia** de cada notebook (o ábrela desde GitHub / Drive).
2. En esas copias, después de la corrida original, deja una **segunda versión**
   de la red con dos capas extra (puedes duplicar celdas para no perder la
   corrida de referencia).

## Requisitos

1. Ejecuta **primero** las dos notebooks **sin cambiar** la topología
   \(4 \times 3 \times 3\). Guarda las gráficas de error/pérdida.
2. Agrega **exactamente dos capas ocultas** a **cada** red. La entrada sigue
   siendo 4 y la **salida sigue siendo 3** (Iris tiene 3 clases). Topología
   pedida:

   \[
   4 \times 3 \times 3 \times 3 \times 3
   \]

   (cuatro capas de 3 neuronas: tres ocultas + salida). Usa **sigmoide** en
   todas las capas, el mismo \(\eta = 0.03\) y las mismas **500 épocas**, para
   que la comparación sea justa.
3. En la notebook **01** debes actualizar **todas** las partes que asumen dos
   capas: tamaños, `init_weights`, el forward de `calculate_error` y el ciclo
   de entrenamiento (propagación **y** retropropagación). No basta con declarar
   dos listas más si el backprop no las usa.
4. En la notebook **02** añade dos `layers.Dense(3, activation="sigmoid", ...)`
   **antes** de la capa de salida. `model.summary()` debe mostrar **4** capas
   `Dense`.
5. El análisis comparativo cubre **cuatro** corridas: original vs. más profunda,
   en implementación a mano **y** en Keras.

## Pasos sugeridos

1. Abre [Google Colab](https://colab.research.google.com/). Sube las notebooks
   (`Archivo` → `Subir notebook`) o ábrelas desde Drive.

2. En Colab, TensorFlow ya está instalado. Ejecuta **Runtime → Run all** en
   cada notebook original. Anota:
   - la curva de error (notebook 01) o de `loss` (notebook 02);
   - el valor de error/pérdida al **final** de las 500 épocas;
   - (notebook 02) el `model.summary()` y una predicción de ejemplo.

3. Duplica las celdas de arquitectura y entrenamiento (o crea una sección
   “red profunda”) y cambia la topología a \(4 \times 3 \times 3 \times 3 \times 3\).

   En Keras el esqueleto queda así (completa nombres y el resto del notebook):

   ```python
   model = keras.Sequential(
     [
       layers.Dense(3, activation="sigmoid", name="layer1", input_shape=(4,)),
       layers.Dense(3, activation="sigmoid", name="layer2"),
       layers.Dense(3, activation="sigmoid", name="layer3"),
       layers.Dense(3, activation="sigmoid", name="layer4"),
     ]
   )
   ```

   En la notebook 01 tendrás `layer1` … `layer4`. El backprop recorre las capas
   **de la salida hacia la entrada**: el \(\delta\) de una capa oculta usa los
   pesos y los \(\delta\) de la capa **siguiente**.

4. Vuelve a entrenar 500 épocas con \(\eta = 0.03\). Guarda las nuevas curvas
   y, si puedes, el tiempo de la celda de entrenamiento.

5. Redacta el análisis comparativo (ver entrega).

## Criterios de aceptación

- Las dos notebooks originales corrieron en **Colab** (no solo en tu máquina).
- Cada red profunda tiene **dos capas extra**; la salida sigue siendo de
  **3** neuronas.
- La notebook 01 actualiza forward **y** backprop (no solo la inicialización).
- Hay evidencias (capturas) de las **cuatro** corridas: curvas y, en Keras,
  `model.summary()` original y profundo.
- El reporte compara implementación a mano vs. Keras **y** red original vs.
  red más profunda; no es un resumen de lo que “debería” pasar sin números.

## Entrega

1. Enlaces de Colab (o archivos `.ipynb`) de las dos notebooks **modificadas**,
   con las corridas originales y las profundas.
2. Capturas: curvas de error/pérdida de las cuatro corridas y los dos
   `model.summary()` de Keras.
3. Un breve reporte (media página a una página) que responda:
   - ¿Bajar más el error al añadir dos capas, o se estancó / empeoró? ¿Igual
     en NumPy y en Keras?
   - ¿Las curvas de la notebook 01 y de Keras se parecen con la misma
     topología? Si no, ¿qué diferencias de implementación podrían explicarlo
     (orden de los datos, inicialización, vectorización, etc.)?
   - Con sigmoides apiladas y MSE, ¿tiene sentido que una red **más profunda**
     no aprenda mejor en Iris? Relaciónalo con lo que viste en las gráficas.
4. Evidencias de haber ejecutado en Colab (captura del entorno Colab o del
   menú Runtime).

## Reto opcional

- Repite la red profunda en Keras con **ReLU** en las capas ocultas y
  **softmax** en la salida, y pérdida `categorical_crossentropy`. Compara con
  la versión todo-sigmoide + MSE.
- Cambia el número de neuronas de las capas ocultas (p. ej. \(4 \times 8 \times 8 \times 8 \times 3\))
  y observa si Iris (150 ejemplos) se beneficia o se sobreajusta.
- En la notebook 01, imprime el error cada 50 épocas en ambas topologías para
  ver **cuándo** se aplana la curva.

## Pistas

- Iris es un problema **pequeño y casi linealmente separable** por pares de
  clases. Más capas no garantizan menor error.
- En backprop, si \(\delta^{(l)} = h^{(l)}(1-h^{(l)}) \odot \text{(error atrás)}\),
  varios sigmoides seguidos pueden hacer los \(\delta\) **muy chicos**
  (gradiente que se desvanece).
- No cambies a la vez topología, \(\eta\), épocas y función de pérdida: si
  cambia todo, no sabes **qué** causó la diferencia.
- La última capa debe tener **3** neuronas: `Y` es one-hot de 3 clases.

## Solución

### 1. Enlaces

Notebooks modificados (adjuntos en este folder):
- `04 Multilayer perceptron.ipynb` (NumPy): al final, sección "Red más profunda (4 x 3 x 3 x 3 x 3)".
- `05 Keras - multilayer perceptron - iris.ipynb` (Keras): al final, sección "Red más profunda en Keras".

Enlace de Colab: --

### 2. Capturas

Por tomar en Colab (Run all): curva de error de 04 (4x3x3 vs 4x3x3x3x3 en la misma gráfica), curva de loss de 05 (ídem) y los dos `model.summary()` de Keras (2 y 4 capas `Dense`).

### 3. Reporte

**Resultados** (500 épocas, η = 0.03, sigmoide + MSE):

| Implementación | Topología | Error / loss final | Accuracy | Tiempo |
|---|---|---|---|---|
| NumPy (semilla 2) | 4x3x3 | 0.057 | 0.967 | 4.0 s |
| NumPy (semilla 2) | 4x3x3x3x3 | 0.669 | 0.333 | 7.4 s |
| Keras | 4x3x3 | 0.222 | 0.567 | -- |
| Keras | 4x3x3x3x3 | 0.222 | 0.500 | 28.5 s |

Con 10 semillas en NumPy: 4x3x3 error medio 0.124 (8/10 llegan a 0.06), 4x3x3x3x3 error medio 0.425 (4/10 se quedan en 0.67, 2 en 0.39, 2 en 0.26–0.33 y sólo 2 llegan a ~0.09), accuracy medio 0.909 vs 0.619.

**¿Bajar más el error al añadir dos capas, o se estancó / empeoró? ¿Igual en NumPy y en Keras?**
Empeoró o se estancó en ambos. En NumPy la red profunda se queda en 0.669 durante casi todo el entrenamiento (en esta corrida nunca sale de ahí) mientras la de 4x3x3 baja a 0.057. En Keras ninguna baja de 0.222 en 500 épocas.

**¿Las curvas de 01 y Keras se parecen con la misma topología?**
No. NumPy converge a 0.057 y Keras queda en 0.222. Diferencias de implementación:
- Keras usa `batch_size=32` por defecto: 5 actualizaciones por época contra 150 en NumPy (SGD por ejemplo), así que aprende aproximadamente 30 veces más lento.
- El MSE de Keras es promedio sobre las 3 salidas y el de NumPy es suma, es decir, 0.222 en Keras equivale a 0.667 en NumPy.
- Inicialización: Glorot en Keras y U(-0.5, 0.5) en NumPy.

**Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris?**
Sí. El error 0.667 es el MSE de predecir 1/3 para las tres clases (la salida casi no depende de la entrada: [3,3,1,1] → [0.342, 0.339, 0.336]). Cada sigmoide multiplica el delta por h(1-h) ≤ 0.25, y con 4 capas el gradiente que llega a las primeras capas es muy pequeño (gradiente que se desvanece). Iris es un problema casi linealmente separable y una capa oculta de 3 neuronas basta; agregar capas sólo vuelve más difícil el entrenamiento.

Nota: Se cambió np.random.rand(1) por np.random.rand() en 'generate_weights' porque la versión original de numpy lanza error.

### 4. Evidencias

Por tomar: captura del entorno Colab / menú Runtime.
