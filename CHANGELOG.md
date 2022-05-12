# Notas

#### 12/05/2022 - Nico
## Added
  - Mejoras en los iconos.
  - Tooltip para los botones de acciones.
  - Sección de instrucciones.
  - Sección de presentación. `Ver las notas para impletarlo`.
  - Ya saqué el **`svg_root`**.
  - Agregué el cursor para cuando guided teleport está activo. `Ver las notas para impletarlo`.


### Notes

  - #### **Para trabajar tranquilo sin tener que cerrar cartel de CHASE_ siempre que se refresaca la pagina simplemente hay sacarlse la clase `game-title--active` al componente con clase `game-title`.** 
  - Para pintar los circulos (**`count-indicator__circle`**) hay que agregarles la clase **`count-indicator__circle--active`**. _Tienen un id para poder refernciarlos en Python_.
  - Sacar los botones del **`table`** para que no rompa.
  - Para terminar la sección de presentación del juego habría que agregar alguna variable que se inicialice en **`False`** y con la primera interación se cambie a **`True`**. La primera interacción la interpreté como `click` o `keydown`. Eso es para que mientras la sección de presentación del juego esté activa no se pueda interactuar con el juego. Entonces habría que preguntar si esa variable es **`True`** para las interacciónes con el juego. Eso es una idea.
  - Para implementar el cursor de guided teleport activo hay que agregarle la clase **`separation-wrapper--guided-teleport-cursor`** al componente con id **`separationWrapper`**.
