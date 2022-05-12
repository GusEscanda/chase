# Notas

#### 12/05/2022 - Nico
## Added
  - Mejoras en los iconos.
  - Tooltip para los botones de acciones.
  - Sección de instrucciones.
  - Sección de presentación. _Ver las notas para impletarlma_.
  - Ya saqué el **svg_root**.


### Notes
  - Para pintar los circulos (**count-indicator__circle**) hay que agregarles la clase **count-indicator__circle--active**. _Tienen un id para poder refernciarlos en Python_.
  - Sacar los botones del **table** para que no rompa.
  - Para terminar la sección de presentación del juego habría que agregar alguna variable que se inicialice en **False** y con la primera interación se cambie a **True**. La primera interacción la interpreté como _click_ o _keydown_. Eso es para que mientras la sección de presentación del juego esté activa no se pueda interactuar con el juego. Entonces habría que preguntar si esa variable es **True** para las interacciónes con el juego. Eso es una idea.
