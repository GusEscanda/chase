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



#### 17/05/2022 - Gustavo
## Added
   - Ahora los botones de las bombas y teleports reflejan correctamente el stock de cada elemento
   - El boton de guided-teleport hace que la flecha del mouse se transforme en una mira

### Notes
    - Intenté, sin exito, hacer una clase que cambie la pinta del boton guded-teleport para que se sepa que ese modo está seleccionado. Hice una clase llamada 'button-selected' que tendrías que revisar/corregir
    - Ahora todas las clases CSS y elementos HTML pueden tener la convension de nombres que se estila para cada caso, lo unico que hay que tener en cuenta es que en el archivo constant.py hay que dejat registrados esos nombres en las definiciones de las clases HTMLElmnt y CSSClass
    - Eliminar todas las funciones de javascript que procesan eventos de mouse o keyboard dejando para los modulos de python esta tarea
    - En caso de agregar un modal, crear el/los elemento/s html (cuadro de dialogo, botones) y las clases para que aparezca/desaparezca, informarlas en el constant.py y luego desde python se trabajará la lógica correspondiente
    - Ya saqué los binds de los botones de flechas, se pueden eliminar del html
    - Ya está hecha en python la logica de esconder la 'gameTitleScreen' luego de presionar una tecla o clickear con el mouse
    - **`OJO`**:
       - En modo guided-teleport, al pasar el mouse por algunas zonas del tablero, desaparece la mira y aparece la flecha comun o incluso la barra vertical de ingreso de texto!! En esas condiciones al hacer click NO ejecuta la teletransportacion. Quiza haya que asociar la clase 'separation-wrapper--guided-teleport-cursor' a algun otro elemento HTML. Eso lo podes probar vos cambiando en las clases del constant.py tanto el elemento como la clase a utilizar para esta tarea
       - Hace un tiempo esta dando un warning como pagina insegura al cargarla desde internet, tal vez haya algun tipo de codigo javascript que la haga "sospechosa" para el antivirus
    
    
    
