# Ejercicio 1 — Separar los blobs y volver a elegir \(k\)

## Contexto

La notebook `Clustering K-medias/Notebooks/01 K-medias.ipynb` (capítulo de
Géron / Hands-On ML) entrena **k-means** de scikit-learn sobre nubes
gaussianas y termina con segmentación de color de una foto.

La parte central genera **5** blobs, ajusta `KMeans(n_clusters=5, ...)` y
después busca el \(k\) “bueno” con dos herramientas:

| Herramienta | Qué grafica | Lectura en la notebook original |
|---|---|---|
| **Codo** (inercia \(J\) vs \(k\)) | `inertias` para \(k = 1,\ldots,9\) | El codo está en **\(k = 4\)**, no en 5 |
| **Silueta** | `silhouette_score` para \(k = 2,\ldots,9\) | \(k = 4\) se ve muy bien; **\(k = 5\)** también |

Eso no es un bug: tres blobs de la izquierda están **casi pegados**
(`std = 0.1` y centros en \(x = -2.8\)). K-means (y el codo) los trata como
un solo grupo.

En este ejercicio **sí vas a modificar código**, pero un cambio pequeño y
local: **alejar esos blobs**. No toques `Clustering K-medias/project/`.
Trabajas en **Colab**, sobre una **copia** de la notebook.

## Objetivo

Correr la notebook en Colab **tal como está**, anotar el \(k\) que sugieren
codo y silueta, **separar los 5 blobs** en el arreglo `blob_centers` (y, si
hace falta, `blob_std`) y volver a graficar. Debes ver si el codo y la
silueta se mueven hacia **\(k = 5\)**.

## Archivos a crear / modificar

No modifiques la notebook original del repositorio.

1. Sube a Colab una **copia** de `01 K-medias.ipynb`
   (`Archivo` → `Subir notebook`) o ábrela desde Drive / GitHub.
2. En esa copia deja evidencia de la corrida **original** y de la
   **modificada** (duplica las celdas de datos, codo y silueta, o guarda
   las figuras antes de editar).

## Requisitos

1. Ejecuta **primero** la notebook **sin cambiar** `blob_centers` ni
   `blob_std`. Guarda al menos:
   - el scatter de los blobs;
   - el diagrama de Voronoi con \(k = 5\);
   - la curva de inercia (codo);
   - la curva de silueta.
2. El cambio pedido es **uno solo**: edita la celda de los centros (y, si
   quieres, las desviaciones) para que los **cinco** grupos se vean
   **separados a ojo** en el scatter. No borres blobs ni cambies
   `n_samples=2000` ni `random_state=7`.

   Centros originales (no los dejes así en la versión modificada):

   ```python
   blob_centers = np.array(
       [[ 0.2,  2.3],
        [-1.5 ,  2.3],
        [-2.8,  1.8],
        [-2.8,  2.8],
        [-2.8,  1.3]])
   blob_std = np.array([0.4, 0.3, 0.1, 0.1, 0.1])
   ```

   Ejemplo de dirección (inventa los tuyos; no copies este bloque al pie
   de la letra si se te ocurre otra separación clara):

   - mueve los tres centros de la izquierda para que **no** compartan la
     misma \(x\);
   - o súbeles el `blob_std` **y** aléjalos, para que no se fusionen.

3. **No** cambies a la vez el \(k\) del primer `KMeans`, el `init` y los
   datos. El experimento es: *mismos hiperparámetros, nubes distintas*.
   Sigue usando el bucle `kmeans_per_k` con \(k = 1,\ldots,9\).
4. Tras regenerar `X`, vuelve a correr **desde** `make_blobs` las celdas
   de ajuste, Voronoi, inercia y silueta. La sección de la catarina
   (`ladybug.png`) **pisa** la variable `X`; si ya la corriste, no uses
   ese `X` para el codo.

## Pasos sugeridos

1. Abre [Google Colab](https://colab.research.google.com/) y carga la
   copia de la notebook.

2. **Runtime → Run all**. En la parte de blobs, anota:
   - inercia de \(k = 3\), \(k = 5\) y \(k = 8\) (celdas
     `kmeans_k3.inertia_`, `kmeans.inertia_`, `kmeans_k8.inertia_`);
   - en qué \(k\) **tú** marcarías el codo;
   - en qué \(k\) es máxima la silueta.

3. Dibuja en papel (o ASCII) los 5 centros originales y los 5 nuevos,
   con una idea de radio (`blob_std`).

4. Edita `blob_centers` / `blob_std`, vuelve a ejecutar `make_blobs` y
   las celdas de gráficas (no hace falta repetir `%timeit` ni Elkan).

5. Compara lado a lado: scatter, Voronoi \(k = 5\), codo y silueta.

## Criterios de aceptación

- La notebook original corrió en **Colab** (no solo en tu máquina).
- Los centros **no** son los de Géron; en el scatter se distinguen
  **cinco** nubes (aunque alguna se solape un poco).
- Sigues teniendo **5** centros y 2000 puntos.
- Hay capturas **antes y después** del scatter, del codo y de la silueta.
- El reporte dice con números (inercias o scores) si el codo / la silueta
  se acercaron a \(k = 5\); no basta “se ve mejor”.

## Entrega

1. Enlace de Colab (o el `.ipynb` modificado) con la corrida original y
   la de blobs separados.
2. Capturas: scatter, Voronoi \(k = 5\), codo y silueta — **original** y
   **modificado** (8 figuras, o 4 pares).
3. Los 5 centros y 5 `std` que usaste.
4. Un breve reporte (media página) que responda:
   - En los datos de Géron, ¿por qué el codo “prefiere” \(k = 4\) si
     `make_blobs` usó 5 centros?
   - Con tus blobs separados, ¿el codo y la silueta coinciden en el mismo
     \(k\)? ¿Ese \(k\) es 5?
   - Si el codo sigue en 4, ¿qué te falta mover (distancia entre centros
     vs. `blob_std`)?
5. Evidencia de haber ejecutado en Colab (captura del entorno o del menú
   Runtime).

## Reto opcional

- Deja los centros de Géron y **solo** sube los tres `std = 0.1` a
  `0.4`. ¿El codo se mueve igual que al **alejar** los centros?
- En la última sección, sustituye `ladybug.png` por **una imagen tuya**
  y compara 10 / 8 / 6 / 4 / 2 colores. ¿Con cuántos colores reconoces
  todavía el objeto?
- Corre el codo y la silueta sobre **Iris** (`X = data.data` de las
  primeras celdas, 4 atributos). ¿El \(k\) “bueno” coincide con las 3
  especies? Relaciónalo con el scatter setosa vs. las otras dos.

## Pistas

- Inercia **siempre** baja (o no sube) al crecer \(k\): por eso no eliges
  el \(k\) de mínima \(J\), sino el **codo**.
- Silueta cerca de \(+1\): punto bien metido en su cluster; cerca de \(0\):
  en la frontera; negativa: quizá está en el grupo equivocado.
- Si dos centros están a distancia menor que \(\sim 2(\sigma_i+\sigma_j)\),
  las nubes se mezclan y k-means no “ve” dos grupos.
- Después de `X = image.reshape(-1, 3)` ya no tienes los blobs. Vuelve a
  la celda de `make_blobs` (o guarda `X_blobs = X.copy()` antes).
- `random_state=7` en `make_blobs` y `random_state=42` en `KMeans` dejan
  las figuras reproducibles: no los quites si quieres comparar con un
  compañero.
- No hace falta GPU. Sklearn basta con el runtime de CPU de Colab.

## Solución

### 1. Enlace

Notebook modificado adjunto en este folder: `01 K-medias.ipynb` (sección "Ejercicio 1 — Separar los blobs y volver a elegir k", al final).

Enlace de Colab: --

### 2. Capturas

Por tomar en Colab: la sección nueva genera las 4 figuras (scatter, Voronoi k = 5, codo, silueta) para la corrida **original** y para la **modificada** (8 figuras).

### 3. Centros

Centros y `std` usados (`n_samples=2000`, `random_state=7`):

```python
blob_centers = np.array(
    [[ 0.2,  2.3],
     [-1.5,  2.3],
     [-3.2,  0.8],
     [-3.2,  3.8],
     [-3.2,  2.3]])
blob_std = np.array([0.4, 0.3, 0.1, 0.1, 0.1])
```

Los tres blobs de la izquierda se separan en vertical (1.5 de distancia entre centros, con `std = 0.1`); `blob_std` no cambia.

```
Original                          Modificado
 y                                 y
 3 |  .(-2.8,2.8)                  3.8|  .(-3.2,3.8)
 2.3| .(-2.8,1.8)  o(-1.5)  O(0.2)  2.3|  .(-3.2,2.3)   o(-1.5)  O(0.2)
 1.3|  .(-2.8,1.3)                  0.8|  .(-3.2,0.8)
```

### 4. Reporte

| | Original | Modificado |
|---|---|---|
| Inercia k = 3 | 653.2 | 1218.2 |
| Inercia k = 5 | 224.1 | 213.3 |
| Inercia k = 8 | 127.1 | 119.6 |
| Inercia k = 4 | 261.8 | 752.6 |
| Silueta k = 4 | 0.689 | 0.695 |
| Silueta k = 5 | 0.627 | 0.775 |
| k con silueta máxima | 4 | 5 |

**En los datos de Géron, ¿por qué el codo "prefiere" k = 4 si `make_blobs` usó 5 centros?**
Los blobs de `(-2.8, 1.8)` y `(-2.8, 1.3)` (con `std = 0.1`) están a 0.5 de distancia y se tocan: k-means los trata como un solo grupo. Pasar de k = 4 a k = 5 sólo baja la inercia de 261.8 a 224.1 (poco), mientras que de k = 3 a k = 4 baja de 653.2 a 261.8: el codo queda en 4.

**Con tus blobs separados, ¿el codo y la silueta coinciden en el mismo k? ¿Ese k es 5?**
Sí, coinciden en k = 5. La inercia cae de 752.6 (k = 4) a 213.3 (k = 5) y después casi se aplana (170.9 en k = 6). La silueta es máxima en k = 5 (0.775 contra 0.695 en k = 4).

**Si el codo sigue en 4, ¿qué te falta mover?**
No aplica, el codo ya está en 5. Si siguiera en 4 habría que aumentar la distancia entre centros respecto a `blob_std` (regla: distancia mayor a ~2(σi + σj)) o reducir `blob_std`.

**Reto opcional**
- Centros de Géron con los tres `std = 0.1` subidos a `0.4`: inercias k = 3, 5, 8 de 941.9, 451.4, 329.2; la silueta es máxima en k = 2 (0.533, y baja a 0.395 en k = 5). Las nubes se funden aún más y el codo se desdibuja (no se mueve a 5): ensanchar los blobs empeora la separación igual o más que acercarlos.
- Iris (4 atributos): la silueta es máxima en k = 2 (0.681; 0.551 en k = 3) y el codo queda entre 2 y 3 (inercia 152.3 en k = 2, 78.9 en k = 3), sin marcar claramente k = 3. Setosa está muy separada de las otras dos, pero versicolor y virginica se solapan, así que k-means las ve como un solo grupo.

### 5. Evidencia

Por tomar: captura del entorno Colab / menú Runtime.
