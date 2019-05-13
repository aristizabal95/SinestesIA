---
layout: submain
title: Sinestes
alt_title: .IA
subtitle: Música, Danza e Inteligencia Artificial
description: Sinestes.IA es un proyecto artistico realizado por Alejandro Aristizábal con la intención de explorar las utilidades del aprendizaje profundo como instrumento de creación musical.
sitemap:
    priority: 1.0
    lastmod: 2019-02-04
    changefreq: weekly
---
<article class="post">
	<header class="major">
    <h2 id="title"><a href="{{site.baseurl}}/">{{site.title}}<span>{{site.alt_title}}</span></a></h2>
		<p style="margin: 0"><i>"El baile puede revelar todo el misterio que la música concede."</i></p>
    <p>Charles Baudelaire</p>
	</header>
	<a href="#intro" class="image main scrolly"><img src="{{ "/images/main.png" | absolute_url }}" alt="" /></a>
	<h3 id="index">Índice</h3>
	<ol class="alt">
		<li><a href="#one" class="scrolly">Introducción</a></li>
		<li><a href="#two" class="scrolly">Contexto</a></li>
    <li>
      <a href="#three" class="scrolly">Marco Teórico</a>
      <ol class="alt prefix three">
        <li>
          <a href="#three-one" class="scrolly">Redes Neuronales</a>
          <ol class="alt prefix three-one">
		        <li><a href="#three-one-one" class="scrolly">Redes Neuronales Completamente Conectadas</a></li>
		        <li><a href="#three-one-two" class="scrolly">Redes Neuronales Convolucionales</a></li>
		        <li><a href="#three-one-three" class="scrolly">Redes Neuronales Recurrentes</a></li>
          </ol>
        </li>
        <li><a href="#three-two" class="scrolly">Sistemas de Tracking</a></li>
        <li><a href="#three-three" class="scrolly">Los Esfuerzo-Acciones de Laban</a></li>
      </ol>
    </li>
    <li><a href="#four" class="scrolly">Objetivos</a></li>
		<li>
      <a href="#five" class="scrolly">Metodología</a>
      <ol class="alt prefix five">
        <li><a href="#five-one" class="scrolly">Definir el problema de aprendizaje</a></li>
        <li>
          <a href="#five-two" class="scrolly">Obtener bases de datos</a>
          <ol class="alt prefix five-two">
		        <li><a href="#five-two-one" class="scrolly">Cómo capturar el video</a></li>
		        <li><a href="#five-two-two" class="scrolly">Cómo capturar el sonido</a></li>
		        <li><a href="#five-two-three" class="scrolly">Componer los ejemplos sonoros</a></li>
		        <li><a href="#five-two-four" class="scrolly">Capturar los datos</a></li>
          </ol>
        </li>
        <li>
          <a href="#five-three" class="scrolly">Definir un modelo de aprendizaje base</a>
          <ol class="alt prefix five-three">
		        <li><a href="#five-three-one" class="scrolly">Modelo de comprensión espacial</a></li>
		        <li><a href="#five-three-two" class="scrolly">Modelo de comprensión temporal</a></li>
		        <li><a href="#five-three-three" class="scrolly">Modelo de acción</a></li>
          </ol>
        </li>
        <li><a href="#five-four" class="scrolly">Entrenar el modelo de aprendizaje</a></li>
      </ol>
    </li>
		<li><a href="#six" class="scrolly">Resultados</a></li>
		<li><a href="#seven" class="scrolly">Conclusión</a></li>
		<li><a href="#biblio" class="scrolly">Bibliografía</a></li>
		<li><a href="#anexos" class="scrolly">Anexos</a></li>
	</ol>
  <!-- INTRODUCTION -->
  <header>
    <h3 id="one">1.Introducción</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Pocos fenómenos sensoriales son atribuidos tanto misterio y tanto arte como la sinestesia. Sinestesia es un fenómeno poco comprendido, que se describe como <em><i>"la confusión de sensaciones, donde la excitación de un sentido genera estimulación en otra modalidad sensorial completamente diferente". (Ternaux, 2003, p. 1, t.d.a)</i></em>. Artistas como <i><a target="_blank" href="https://es.wikipedia.org/wiki/Arthur_Rimbaud">Rimbaud</a>, <a target="_blank" href="https://es.wikipedia.org/wiki/Charles_Baudelaire">Baudelaire</a> y <a target="_blank" href="https://es.wikipedia.org/wiki/Vasili_Kandinski">Kandinsky</a></i> tuvieron la suerte de comprender medios artísticos por fuera de sus capacidades, y expresarlos a través de sus habilidades.
  </p>
  <p>
  Lamentablemente, la sinestesia es un fenómeno poco común, razón por la cual el arte de Kandinsky, o los poemas de Baudelaire se destacan del ordinario. La sinestesia, como herramienta artística, tiene una característica interesante, y es que reduce la brecha entre la destreza y la creatividad, permitiendo a escritores expresarse en términos de luz, a pintores expresarse en términos de sonido, entre otros. Si este fenómeno pudiera replicarse, ¿cuántas personas disfrutarían de la capacidad de expresarse en medios que desconocen?.
  </p>
  <p>
  Se han realizado diversos estudios, con el objetivo de comprender las razones por las que este tipo de fenómenos se dan, y en qué manera se expresan; y si bien se han llegado a conclusiones sobre la causa física, los mecanismos cerebrales relacionadas a su expresión siguen siendo desconocidos (Ternaux, 2003, p. 2, t.d.a). Uno de los esfuerzos más reconocibles de comprender la asociación artística entre percepciones en un artista ha sido con Kandinsky, quien logró especificar una teoría bajo la cual su percepción musical se relacionaba con su expresividad visual. Por desgracia, esta descripción es bastante subjetiva y única, no extendiéndose a una generalidad del fenómeno.
  </p>
  <span class="image fit">
    <img src="{{'/images/kandinsky-01.jpg' | absolute_url}}" alt>
    <p><i>Composición V, pieza sinestética realizada por Wassily Kandinsky (Di Marco & Spadaccini, 2015, p. 33).</i></p>
  </span>
  <blockquote>
  "El azul [...] es comparable con el sonido de una flauta. El rojo es cálido, [...] comparable con el sonido de una tuba. El naranja [...] sonido de una campana..." (Di Marco & Spadaccini, 2015, p. 25)
  </blockquote>
  <p>
  Todo pareciera indicar que estamos lejos de comprender este fenómeno, mucho menos de replicarlo. Pero, hoy en día, tenemos herramientas tecnológicas que podrían permitirnos cerrar la brecha entre la destreza y la creatividad. El aprendizaje de máquina es una de esas herramientas. Esta área de la inteligencia artificial, desarrollada desde los años 50, permite hallar patrones entre una gran cantidad de datos, sean estos patrones conocidos previamente o no. Esta capacidad computacional, que a primera instancia suena sencilla, ha permitido una expansión acelerada al uso de la tecnología en el día a día. Cosas como reconocimiento facial, reconocimiento de voz, procesamiento de lenguaje natural, y mucho más; son algunos ejemplos de aprendizaje de máquina siendo usado en la cotidianidad.
  </p>
  <div class="box">
  <p>
  <b>Es probable que no podamos comprender con totalidad la expresión de la sinestesia, pero podemos generar herramientas que busquen simularla.</b>
  </p>
  </div>
  <p>
  El desarrollo de estas herramientas tiene el potencial de aproximar la expresión creativa a la sociedad, permitiendo a personas sin formación artística expresarse de manera instintiva. Lograr este objetivo implica generar herramientas de creación con funcionalidades intuitivas, donde la curva de aprendizaje sea sutil. Cumplir este objetivo requiere de mucha experimentación y exploración en distintas técnicas y estrategias para facilitar la expresividad artística. Es debido a esto que se crea Sinestes.IA, proyecto artístico con la intención de indagar en el uso de inteligencia artificial como instrumento de expresión musical.
  </p>
  <p>
  Sinestes.IA propone la exploración de un ambiente musical a través de un medio de expresión muy común: el movimiento. Se ha escogido el movimiento debido a que es una acción natural e intuitiva. Además, su expresión artística, la danza, es un medio que se encuentra altamente ligado a la música debido a que ambas están subordinadas al factor de la temporalidad. Ahora bien, desarrollar una herramienta que pueda traducir el movimiento en música plantea varios problemas, desde el punto de vista técnico como conceptual. Entre estos se destacan realizar un sistema que comprenda tanto la danza como la música y desarrollar una función que logre traducir el movimiento a sonidos. Estos obstáculos serán enfrentados a lo largo del proyecto, con el objetivo de analizarlos y de establecer las soluciones que se implementarán para lograr el objetivo de Sinestes.IA.
  </p>
  <!-- /INTRODUCTION -->
  <!-- CONTEXT -->
  <header>
    <h3 id="two">2.Contexto</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Sinestes.IA se ha visto influenciado por proyectos previos que he desarrollado. Estos trabajos han indagado tanto en el uso de inteligencia artificial de manera artística, como en el manejo del movimiento como interfaz musical. Entre estos proyectos se encuentra “Vieja Musical Programable (MVP)”, el cual exploraba el uso de Kinect para interactuar con unos parámetros musicales desarrollados en Pure Data. La interacción permitía cambiar volumen y paneo de varios loops, al igual que activar, desactivar o cambiar pistas sonoras a través de gestos predeterminados. Además, el usuario podía interpretar sonidos de batería como hi-hat, redoblante y bombo a través de movimientos rápidos igualmente predeterminados. La intención de este proyecto era crear un instrumento que permitiera a cualquier usuario interactuar con la música, pero su desarrollo fue poco intuitivo, y tenía una curva de aprendizaje acentuada, requiriendo tiempo y habilidad poder expresarse por este medio.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/AAkLWmcJ2EI?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  <p>
  Otro proyecto desarrollado recientemente fue “Música Autómata”. Este  buscaba indagar el uso de inteligencia artificial para interactuar con un ambiente sonoro. “Música Autómata” consistía en desarrollar un programa que observaba los gestos faciales del oyente, con el objetivo de maximizar un gesto específico. El programa solo podía interactuar con parámetros sonoros, por lo que debía explorar qué sonidos generaban el gesto facial deseado en el oyente. Gracias a esto el oyente tenía el mismo control sobre la música que el programa, involucrándose de manera pasiva en la composición. El programa está basado en un algoritmo de aprendizaje reforzado, y el ambiente sonoro fue desarrollado en Pure Data.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/mghyfGKCtIo?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  <p>
  La idea de explorar el movimiento como interfaz musical no es nueva, y ha sido ampliamente explorada por varios artistas a través de la historia. Entre los experimentos pasados se destaca el uso de Theremins por John Cage y Merce Cunningham en 1965 con la intención de capturar los movimientos de bailarines y transformarlos en sonido en la obra Variations V.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/yOAagU6cfBw?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  <p>
  En otros ejemplos más recientes se encuentra Imogen Heap con los guantes Mi.Mu, los cuales le permiten captar los movimientos de sus manos con alta precisión y controlar parámetros musicales con ellos. Los guantes Mi.Mu le permiten al artista grabar pistas, agregar efectos, controlar instrumentos y mucho más a través de gestos predefinidos por el intérprete.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/7oeEQhOmGpg?t=359&origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  Ahora bien, el uso de inteligencia artificial en áreas creativas como el arte y la música también ha sido ampliamente explorado. Entre estos experimentos se destaca la extracción y adición de estilos artísticos en imágenes y pinturas, permitiendo al usuario visualizar cómo una imagen, foto y dibujo se verían bajo el estilo de distintos artistas. Algoritmos como estos le permiten a cualquier persona explorar estilos artísticos al igual que variar su intensidad o relevancia en la composición final de la imagen, y hoy en día se ha demostrado la aplicabilidad de estos algoritmos en áreas de diseño y creación.
  </p>
  <span class="image fit">
    <img src="{{'/images/styletransfer.png' | absolute_url}}" alt>
    <p><i>Figura adaptada de L. Gatys et al. "<a href="https://arxiv.org/abs/1508.06576">A Neural Algorithm of Artistic Style</a>" (2015)</i></p>
  </span>
  <p>
  En cuanto a la música, herramientas similares se han desarrollado, que estudian el estilo musical de un artista a través de múltiples ejemplos y lo recrean  para crear nuevas composiciones, o para transferirlo a motivos o ideas musicales previas. Bajo esta premisa se han construido herramientas y compañías, como Flow Machines y AIVA(Artificial Intelligence Virtual Artist) con resultados comparables e indistinguibles a los compuestos por humanos.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/03xMIcYiB80?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  <p>
  Por último, y probablemente la referencia más cercana a este proyecto, fue la demostración realizada por Yamaha presentada bajo el nombre Mai Hi Ten Yu. En esta demostración, Yamaha desarrolló una inteligencia artificial que capturaba los movimientos musculares de un bailarín para transformarlos en música a través de un piano.
  </p>
  <span class="image fit">
    <div class="plyr__video-embed" class="js-player">
      <iframe
        src="https://www.youtube.com/embed/21injmy1wsU?origin=https://plyr.io&amp;iv_load_policy=3&amp;modestbranding=1&amp;playsinline=1&amp;showinfo=0&amp;rel=0&amp;enablejsapi=1"
        allowfullscreen
        allowtransparency
        allow="autoplay"
        ></iframe>
    </div>
  </span>
  <!-- /CONTEXT -->
  <!-- THEORY -->
  <header>
    <h3 id="three">3.Marco Teórico</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Antes de continuar es necesario comprender los conceptos y tecnologías que se piensan manejar durante el desarrollo del proyecto, con el objetivo de comprender su aplicación y relación con Sinestes.IA.
  </p>
  <p>
  Sinestes.IA es un proyecto que abarca distintas temáticas y conceptos con la intención de definir las herramientas que se usarán para el desarrollo del mismo. Estos temas van desde el tipo de inteligencia artificial y las arquitecturas, como las teorías de comprensión del movimiento y su relación con la música. Siendo así, estos son los conceptos que se abarcarán:
  </p>
  <ol>
  <ol class="alt prefix three">
    <li>
      <a href="#three-one" class="scrolly">Redes Neuronales</a>
      <ol class="alt prefix three-one">
        <li><a href="#three-one-one" class="scrolly">Redes Neuronales Completamente Conectadas</a></li>
        <li><a href="#three-one-two" class="scrolly">Redes Neuronales Convolucionales</a></li>
        <li><a href="#three-one-three" class="scrolly">Redes Neuronales Recurrentes</a></li>
      </ol>
    </li>
    <li><a href="#three-two" class="scrolly">Sistemas de Tracking</a></li>
    <li><a href="#three-three" class="scrolly">Los Esfuerzo-Acciones de Laban</a></li>
  </ol>
  </ol>
  <header>
    <h4 id="three-one">3.1.Redes Neuronales</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Las redes neuronales son algoritmos usados ampliamente en el área de aprendizaje de máquina e inteligencia artificial. Estos algoritmos fueron conceptualizados con la intención de imitar la funcionalidad del cerebro y la manera en la que aprende. Las redes neuronales son máquinas de cálculo moldeables, que reciben información y sacan información, por lo que se pueden entender como una función matemática. Lo que hace a las redes neuronales especiales comparadas a cualquier otra función matemática es la capacidad de “entrenarse” o adaptarse a los requerimientos de los datos entregados. Esto permite construir modelos en los cuales se sepa con exactitud los datos que debe recibir y generar el algoritmo, aún cuando la manera en que estos datos se relacionan sean desconocidos previamente.
  </p>
  <p>
  Entrenar una red neuronal requiere de algún método para calificar su rendimiento. Al igual que en la academia se le da un puntaje a los trabajos o exámenes realizados según algún criterio, las redes neuronales necesitan una manera de medir si cumplen o no el objetivo esperado. Conociendo su rendimiento actual, se le pone la tarea a la red neuronal de maximizar su rendimiento, o en el caso del examen, se busca obtener la mejor nota. Es con base en este objetivo, y a través de la prueba y error, que la red neuronal logra aprender.
  </p>
  <p>
  Para dar un ejemplo de este proceso, supongamos que se le asigna la tarea a alguien de obtener el mejor resultado en un examen desconocido de opción múltiple. Esta persona sólo podrá saber qué ha respondido y cuál es su calificación final. Al inicio, esta persona no tendrá mejor opción que adivinar las respuestas, pero a medida que va repitiendo el proceso, empezará a observar qué respuestas son correctas y cuáles incorrectas, a través del efecto que sus elecciones dan en el resultado final. Tras un número de repeticiones de este proceso, la persona será capaz de responder el examen perfectamente, aún cuando desconoce el significado de sus respuestas.
  </p>
  <p>
  Las redes neuronales vienen en muchas formas o arquitecturas, cada una con alguna diferencia que la hace mejor para distintas situaciones. Entre estas se destacan para este proyecto las redes neuronales completamente conectadas, las redes neuronales convolucionales y las redes neuronales recurrentes.
  </p>
  <header>
    <h4 id="three-one-one">3.1.1.Redes Neuronales Completamente Conectadas</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Estas son las redes neuronales más básicas y comunes. Suelen funcionar bastante bien para casos sencillos de aprendizaje, pero no son muy eficientes al momento de analizar imágenes o datos secuenciales, comparado a otras arquitecturas.
  </p>
  <span class="image fit">
    <img src="{{'/images/neuralnetwork.gif' | absolute_url}}" alt>
    <p><i>Imagen tomada de <a>https://www.analyticsindiamag.com/how-to-create-your-first-artificial-neural-network-in-python/</a></i></p>
  </span>
  <header>
    <h4 id="three-one-two">3.1.2.Redes Neuronales Convolucionales</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Este tipo de redes neuronales son ampliamente usadas en el contexto de análisis de imágenes, ya que tienen la característica de poder analizar cada pixel en su contexto, a diferencia de las redes neuronales completamente conectadas, que consideran cada pixel un dato independiente. Este es el tipo de red neuronal que se suele usar en aplicaciones como reconocimiento facial o generación de imágenes.
  </p>
  <span class="image fit">
    <img src="{{'/images/convnetwork.png' | absolute_url}}" alt>
    <p><i>Imagen tomada de <a>https://devblogs.nvidia.com/accelerate-machine-learning-cudnn-deep-neural-network-library/</a></i></p>
  </span>
  <header>
    <h4 id="three-one-three">3.1.3.Redes Neuronales Recurrentes</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Esta arquitectura fue especialmente diseñada para tratar con datos secuenciales, tales como sonido o video. Lo que las diferencia del resto es la capacidad de retener memoria, lo cual les permite usar información pasada para tomar decisiones en el futuro. Estas redes neuronales son usadas en herramientas como en análisis de voz, comprensión del lenguaje natural, o en generación de texto, audio y video.
  </p>
  <span class="image fit">
    <img src="{{'/images/recnetwork.jpg' | absolute_url}}" alt>
    <p><i>Imagen tomada de <a>http://www.wildml.com/2015/09/recurrent-neural-networks-tutorial-part-1-introduction-to-rnns/</a></i></p>
  </span>
  <header>
    <h4 id="three-two">3.2.Sistemas de Tracking</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Ya explicados los conceptos base de la inteligencia artificial, es hora de hablar de los sistemas que suelen ser usados en música interactiva para hacer seguimiento del intérprete. Roger T. Dean, autor de <i>The Oxford Handbook of computer music</i>,  determina que existen cinco métodos para hacer seguimiento del movimiento, cada uno con sus ventajas, desventajas y requerimientos.
  </p>
  <p>
  El primer tipo de sistema de tracking es el denominado <i>Inside-in</i>, el cual consiste de sensores ubicados en el cuerpo a medir. Este tipo de sensores tienen la ventaja de que pueden capturar movimientos finos, y no requieren de una posición fija en el escenario. Entre sus desventajas se encuentra la posibilidad de obstruir la movilidad del objeto, además que dificulta la captura de información de la posición del objeto en relación al entorno. Algunos ejemplos de estos sensores son sensores Flex, acelerómetros, micrófonos piezoeléctricos y de contacto.
  </p>
  <p>
  Luego se encuentran los sensores <i>Inside-out</i>, los cuales son ubicados en el cuerpo y proveen información externa del objeto. Estos, contrario a los <i>Inside-in</i>, facilitan la captura de información del entorno, lo que puede proveer posicionamiento con respecto al escenario. Al ser sensores montados en el objeto, también tienen la desventaja de poder limitar la movilidad del objeto, además de no proveer información del objeto per-se. Algunos ejemplos son brújulas o cámaras.
  </p>
  <p>
  Los siguientes sensores son aquellos que van montados externamente al objeto, y se denominan <i>Outside-in</i>. Estos sensores captan información del objeto de interés desde una perspectiva externa al objeto. Tienen la ventaja de capturar simultáneamente información del objeto y su entorno, pero los datos capturados son menos finos comparados a los anteriores tipos de sensores. Por otro lado, estos sensores limitan la movilidad del objeto al marco de referencia que pueden capturar, y sufren de oclusión. Algunos ejemplos de estos sensores son sensores infrarrojos, cámaras, sensores de movimiento, entre otros.
  </p>
  <p>
  Está claro que los sistemas de tracking deben hacer uso de alguno de estos tipos de sensores, pero no se encuentran limitados al uso único de cada tipo. Por esta razón, se clasifica el próximo sistema de tracking como sistema híbrido, y sencillamente consiste en la combinación de los sistemas anteriormente mencionados.
  </p>
  <p>
  Por último, se menciona como otro sistema de tracking la visión computacional, que si bien no es un tipo de sensor empodera la captura de datos debido a la capacidad de procesamiento y análisis de datos que provee. Esta tecnología suele verse necesariamente acompañada de captura de imágenes, por lo que hacen uso de cámaras.
  </p>
  <p>
  Para este proyecto se hará uso del sistema Outside-in, en conjunción con visión computacional. Se ha escogido este tipo de sistema debido a la accesibilidad de este tipo de sensores, y ha que requieren preparación previa mínima con respecto al objeto a medir.  Por otro lado, debido al interés de explorar el uso de algoritmos de aprendizaje, el sistema de visión computacional será desarrollado como parte de dicha exploración.
  </p>
  <header>
    <h4 id="three-three">3.3.Los Esfuerzo-Acciones de Laban</h4>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Rudolf Von Laban es actualmente aclamado por muchos como uno de los padres de la danza contemporánea. Además de haber sido un gran coreógrafo, sus aportes al análisis del espacio y movimiento abrieron paso a nuevas maneras de comprender la danza y el arte escénico. Laban, movido por la filosofía expresionista del momento, buscó otorgarle un sentido científico a la expresión artística del movimiento, formulando estrategias para analizar, comprender y especificar el movimiento, no solo como arte sino como ciencia. Entre su trabajo sobre el movimiento, Laban postula que todo movimiento se puede describir de acuerdo a su espacialidad (E), temporalidad (T) y peso (P). Cada uno des estos aspectos se pueden combinar, y su combinación describe algún tipo de Esfuerzo-acción.
  </p>
  <ul>
    <li>
      <h4>Espacio (E):</h4>
      <p>
        La espacialidad describe el uso del espacio en el movimiento, y puede alternar entre un espacio directo e indirecto. El uso de un espacio directo implica un manejo eficiente del espacio, en el que todo movimiento toma el rumbo más corto para llegar a su objetivo. Por otro lado, el espacio indirecto implica un manejo más amplio del movimiento, en el que se exploran distintas rutas para llegar a un mismo objetivo o posición.
      </p>
    </li>
    <li>
      <h4>Tiempo (T):</h4>
      <p>
        La temporalidad describe tanto la longitud del movimiento como la periodicidad de una sucesión de movimientos. Este aspecto puede alternar entre un tiempo súbito y uno sostenido. El tiempo súbito es corto e impredecible, y se percibe como movimientos erráticos. En cuanto al tiempo sostenido se observan movimientos largos y predecibles.
      </p>
    </li>
    <li>
      <h4>Peso (P):</h4>
      <p>
        El peso es análogo a la energía del movimiento, y puede alternar entre enérgico y ligero. Un peso enérgico refleja movimientos firmes y con fuerza, mientras que un peso ligero se refleja como movimientos libres sin fuerza.
      </p>
    </li>
  </ul>
  <table class="alt">
    <thead>
      <tr>
        <th>Esfuerzo-Acción</th>
        <th>Tiempo</th>
        <th>Peso</th>
        <th>Espacio</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Flotar</td>
        <td>Sostenido</td>
        <td>Ligero</td>
        <td>Indirecto</td>
      </tr>
      <tr>
        <td>Deslizar</td>
        <td>Sostenido</td>
        <td>Ligero</td>
        <td>Directo</td>
      </tr>
      <tr>
        <td>Retorcer</td>
        <td>Sostenido</td>
        <td>Enérgico</td>
        <td>Indirecto</td>
      </tr>
      <tr>
        <td>Presionar</td>
        <td>Sostenido</td>
        <td>Enérgico</td>
        <td>Directo</td>
      </tr>
      <tr>
        <td>Sacudir</td>
        <td>Súbito</td>
        <td>Ligero</td>
        <td>Indirecto</td>
      </tr>
      <tr>
        <td>Tocar</td>
        <td>Súbito</td>
        <td>Ligero</td>
        <td>Directo</td>
      </tr>
      <tr>
        <td>Atacar</td>
        <td>Súbito</td>
        <td>Enérgico</td>
        <td>Indirecto</td>
      </tr>
      <tr>
        <td>Golpear</td>
        <td>Súbito</td>
        <td>Enérgico</td>
        <td>Directo</td>
      </tr>
    </tbody>
  </table>
  <p>
  Siendo que solo hay 3 aspectos para el movimiento, y que su descripción es binaria, solo existen 8 combinaciones posibles de estos estados<sup class="tooltip" data-tip="Si bien Laban agrega otra dimensión o característica al movimiento, denominada Flujo, esta no afecta sustancialmente la concepción de los Esfuerzo-acciones, por lo que no será discutida en este proyecto."><b>[1]</b></sup>. Según el método de Laban todo movimiento se puede caracterizar por alguna de estas combinaciones, y cada combinación refleja un estado emocional característico.
  </p>
  <!-- /THEORY -->
  <!-- OBJECTIVES -->
  <header>
    <h3 id="four">4.Objetivos</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Sinestes.IA tiene varios objetivos de carácter técnico, artístico e investigativo, que concluyen en un resultado creativo. Estos objetivos son:
  </p>
  <ul>
    <li>Generar música en tiempo real a partir de la danza, haciendo uso de la inteligencia artificial como medio para traducir ambas formas de arte.</li>
    <li>Explorar el uso de algoritmos de aprendizaje de máquina como medios de expresión artística.</li>
    <li>Estudiar la relación entre las artes escénicas y la música, y establecer una conexión directa.</li>
    <li>Componer ejemplos musicales como herramienta de entrenamiento para los algoritmos de aprendizaje.</li>
    <li>Desarrollar algoritmos de aprendizaje que logren transformar el movimiento a instrucciones musicales.</li>
  </ul>
  <header>
    <h3 id="five">5.Metodología</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Para lograr cumplir el objetivo principal de Sinestes.IA es necesario comprender qué tipo de proyecto conforma y cuál es el método que se suele aplicar. Sinestes.IA es, en gran medida, un proyecto de aprendizaje de máquina, enmarcado en un carácter artístico que lo define y complementa. Por esta razón la metodología se va a ver basada en los requerimientos de estos proyectos, y en la manera de proceder de los mismos.
  </p>
  <p>
  Para desarrollar un proyecto de aprendizaje de máquina hay que implementar varios aspectos. Estos son:
  </p>

  <ol>
  <ol class="alt prefix five">
    <li><a href="#five-one" class="scrolly">Definir el problema de aprendizaje</a></li>
    <li>
      <a href="#five-two" class="scrolly">Obtener bases de datos</a>
    </li>
    <li>
      <a href="#five-three" class="scrolly">Definir un modelo de aprendizaje base</a>
    </li>
    <li><a href="#five-four" class="scrolly">Entrenar el modelo de aprendizaje</a></li>
  </ol>
  </ol>

  <header>
    <h3 id="five-one">5.1.Definir el problema de aprendizaje</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  La definición del problema de aprendizaje se basa en la obtención de una información deseada a partir de datos previamente conocidos. Esto se suele ver reflejado como un problema de clasificación, como por ejemplo, clasificar la imagen de una persona según la identidad de la misma; o regresión, como por ejemplo, la predicción del precio de un apartamento a través de sus características. En el caso de Sinestes.IA, el problema de aprendizaje se define como predecir el sonido que debe acompañar una sucesión de imágenes de alguien bailando. Esta definición da indicios al tipo de arquitecturas que es necesario manejar, debido al uso de imágenes y secuencias como datos previamente obtenidos.
  </p>
  <header>
    <h3 id="five-two">5.2.Obtener bases de datos que reflejen el problema</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Para un proyecto de aprendizaje de máquina, la obtención de las bases de datos es el requerimiento más relevante, debido a que es con base en esto que el algoritmo podrá aprender. Para el problema que Sinestes.IA busca explorar, la base de datos debe consistir en ejemplos de la información que el programa recibirá, al igual que el resultado que se espera de dichos datos. Como ejemplo, si se desea entrenar una red neuronal para predecir los precios de apartamentos, la base de datos debe consistir de las características del apartamento como elementos de entrada, al igual que el precio de dicho apartamento como salida. Es a partir de estos datos que el algoritmo podrá comprender la relación entre la información entrante y el resultado deseado.
  </p>
  <p>
  Como fue señalado en la definición del problema, Sinestes.IA manejará como datos de entrada una sucesión de imágenes, y de salida sonidos. Ambos tipos de datos deben tener correspondencia, lo que significa que por cada imagen debe haber un dato sonoro, y que cada dato sonoro debe reflejar lo que está ocurriendo en la imagen. Para poder obtener estos datos es necesario plantear varios puntos a resolver:
  </p>
  <ol>
  <ol class="alt prefix five-two">
		 <li><a href="#five-two-one" class="scrolly">Cómo capturar el video</a></li>
		 <li><a href="#five-two-two" class="scrolly">Cómo capturar el sonido</a></li>
		 <li><a href="#five-two-three" class="scrolly">Componer los ejemplos sonoros</a></li>
		 <li><a href="#five-two-four" class="scrolly">Capturar los datos</a></li>
  </ol>
  </ol>
  <header>
    <h3 id="five-two-one">5.2.1.Cómo capturar el video</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  La captura de video se realizará usando el sensor Kinect, desarrollado para la consola de videojuegos Xbox 360. Se ha escogido esta herramienta debido a que fue diseñado con el objetivo de capturar los movimientos e interactuar con entornos virtuales, para lo que se le incorporó un sensor de profundidad.
  </p>
  <p>
  Con el objetivo de simplificar el aprendizaje y reducir los tiempos de procesamiento las imágenes obtenidas del Kinect consistirán únicamente de la captura de profundidad, y el tamaño de las imágenes será de 128x128.
  </p>
  <span class="image fit">
    <img src="{{'/images/videodata.png' | absolute_url}}" alt>
    <p><i>Ejemplos de las imágenes capturadas para el proyecto</i></p>
  </span>
  <header>
    <h3 id="five-two-two">5.2.2.Cómo capturar el sonido</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  El tratamiento del sonido en aplicaciones de inteligencia artificial no es trivial, debido a que un segundo de sonido suele representarse por decenas de miles de valores o samples. Poner a una red neuronal a generar los samples de manera secuencial requeriría de recursos y tiempos por fuera de los estipulados para este proyecto. Aproximaciones de este estilo a la generación musical se pueden observar con Wavenet de DeepMind, red neuronal que genera resultados excepcionales, a costa de los tiempos de generación, que con altos valores de computación puede tomar hasta 90 minutos generar un segundo de audio. Siendo que este proyecto requiere de generación de sonido en tiempo real es necesario buscar otras aproximaciones <i>(Cahill, P. 2018)</i>.
  </p>
  <p>
  La mejor opción para solucionar el problema anterior es codificar la información musical, de tal forma que se requiere menor información poder representar los sonidos deseados. Siendo que los sonidos son generados o sintetizados por el computador, es posible representar la información sonora por medio de mensajes que indiquen la activación y desactivación de sonidos. Este tipo de protocolos ya existen, siendo MIDI (Musical Instrument Digital Interface) el más usado. El protocolo MIDI codifica información de altura, velocidad y canal en su forma más básica, pero no incluye información alguna sobre cómo debería sonar o qué instrumento usar. Este tipo de información es relevante para este proyecto, ya que se busca que el programa pueda reproducir una gran variedad de sonoridades. Por esta razón se implementó un entorno sonoro en Pure Data, con la posibilidad de representar hasta 6 instrumentos simultáneos, cada uno absolutamente moldeable a través de una lista de parámetros. Cada instrumento puede representar desde un sonido ligero y etéreo hasta sonidos súbitos y estridentes, dependiendo de los parámetros especificados <i>(ver anexo: <a href="{{site.baseurl}}/anexos/entorno-sonoro/">entorno sonoro</a>)</i>.
  </p>
  <header>
    <h3 id="five-two-three">5.2.3.Componer los ejemplos sonoros</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Una vez desarrollado el entorno sonoro, es momento de preparar los datos a capturar. Siendo que el objetivo del proyecto es generar música en relación a la danza, dicha relación debe estar representada en los datos de entrenamiento. Para lograr esto es necesario parametrizar la música, de tal manera que pueda ser fielmente representada en la danza al momento de capturar la información. Dicha parametrización no es sencilla, debido a que no existe una relación objetiva entre el movimiento y la música, de tal forma que se pueda expresar un solo sonido específico con un solo tipo de movimiento <i>(Gualdrón, 2013)</i>.
  </p>
  <p>
  Aún así, se ha observado que conocimientos en lenguaje corporal suelen facilitar la expresividad de carácter y dinámica en estudiantes de dirección. Trabajos como Las Ventajas de Aprender Técnica de Dirección por Medio del Análisis de Movimiento Laban  de Deyanira Gualdrón exploran cómo los esfuerzo-acciones de Rudolf Von Laban pueden ejemplificar ciertos tipos de características musicales al ser usados en un ambiente de dirección. Además, la carencia de una relación directa entre la danza y la música abre la posibilidad a la creatividad, permitiendo definir un estilo propio al momento de establecer una conexión entre ambos tipos de arte. Es debido a esto, y con la intención de facilitar la labor de aprendizaje, que se usarán los esfuerzo-acciones de Laban como guía para definir un estilo musical en coherencia con el movimiento.
  </p>
  <p>
  Para establecer el estilo y su conexión con los esfuerzo-acciones, se relacionarán los aspectos del movimiento (espacio, tiempo y peso) con características sonoras y musicales, para así guiar tanto el diseño sonoro como la composición. Esta parametrización es subjetiva, pero fue pensada para mantener cierta generalidad, a través de opiniones tanto de compositores como de bailarines. Como ejemplo, el aspecto del peso en el movimiento suele verse relacionado con la altura y el timbre de los sonidos, de tal forma que sonidos agudos y redondos se ven reflejados por movimientos ligeros, mientras que sonidos estridentes y bajos se reflejan con movimientos enérgicos <i>(ver anexo: <a href="{{site.baseurl}}/anexos/entorno-sonoro/">composiciones</a>)</i>.
  </p>
  <p>
  Con base en estos parámetros se compusieron 8 pequeñas piezas, con duraciones de máximo minuto y medio, donde se buscaba reflejar cada esfuerzo-acción haciendo uso del entorno sonoro implementado anteriormente. De esta manera, se puede especificar el tipo de movimiento específico que se desea para cada obra, y así grabar los datos necesarios para el entrenamiento.
  </p>
  <header>
    <h4>Deslizar</h4>
    <p style="margin: 0;">Tiempo sostenido, Peso ligero, espacio directo</p>
    <audio class="js-player" controls preload>
      <source src="{{ 'audios/deslizar.mp3' | absolute_url}}" />
    </audio>
  </header>
  <header>
    <h4>Retorcer</h4>
    <p style="margin: 0;">Tiempo sostenido, Peso enérgico, espacio indirecto</p>
    <audio class="js-player" controls preload>
      <source src="{{ 'audios/retorcer.mp3' | absolute_url}}" />
    </audio>
  </header>
  <header>
    <h4>Golpear</h4>
    <p style="margin: 0;">Tiempo súbito, Peso enérgico, espacio directo</p>
    <audio class="js-player" controls preload>
      <source src="{{ 'audios/golpear.mp3' | absolute_url}}" />
    </audio>
  </header>
  <header>
    <h3 id="five-two-four">5.2.4.Capturar los datos</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Debido a que los datos de video y audio deben estar en sincronía, y a que la información sonora es representada de una forma no tradicional, fue necesario diseñar un sistema propio para capturar la información. Esto implicó que era necesario definir limitaciones de velocidad de captura y tamaño de buffer para una grabación fiel y constante.
  </p>
  <p>
  La velocidad de captura depende de la frecuencia máxima de la información a grabar, y según el teorema de Nyquist la frecuencia de muestreo debe estar por encima del doble de la frecuencia máxima de los datos. La frecuencia para video estándar para reproducción es de 24fps (frames por segundo), siendo 16fps el mínimo considerado para la percepción de movimiento continuo.
  </p>
  <p>
  En cuanto a los datos sonoros, es necesario establecer una velocidad máxima de acciones para establecer la frecuencia de muestreo necesaria. El estudio de Justin London denominado “Restricciones cognitivas en sistemas métricos” examina la velocidad máxima de impulsos sonoros independientes que el oído humano puede percibir, y establece que una distancia entre impulsos de 50ms (20Hz) es la velocidad teórica máxima de percepción, debido a que este es el límite mínimo de percepción de tonos en la escucha humana. A partir de esto, se puede definir la velocidad de muestreo de las acciones sonoras como 40Hz, y usar esta velocidad para la grabación tanto de sonido como de video en este proyecto.
  </p>
  <p>
  Ahora bien, al momento de capturar los datos, se trabajó con 7 bailarines para realizar múltiples grabaciones de cada composición. Se requirieron múltiples bailarines para tener variedad de estilos de danza y facilidad de coordinación de tiempos con cada bailarín. Las composiciones varían en duración entre un mínimo de 20 segundos hasta un máximo de 1 minuto 30 segundos. Debido a las diferencias de tiempo, las piezas cortas fueron grabadas más veces para compensar por su corta longitud. Una vez finalizadas las grabaciones se obtuvo una cantidad de 240 capturas individuales de vídeo y sonido, que si bien son pocas para un proyecto de aprendizaje profundo, son suficientes para obtener resultados interesantes para este proyecto.
  </p>
  <header>
    <h3 id="five-three">5.3.Definir un modelo de aprendizaje base</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  El diseño del modelo de aprendizaje se basa sustancialmente en el comportamiento de los datos. Siendo que existen tantas arquitecturas y tantas investigaciones realizadas para distintas aplicaciones, es necesario definir algún sistema inicial para evaluar su rendimiento e iterar según los requerimientos del proyecto. Esto significa que si bien es importante tener claro cómo aproximarse al problema, los detalles del modelo se pueden refinar a través de experimentación.
  </p>
  <p>
  El modelo de aprendizaje de Sinestes.IA debe ser capaz de analizar el baile desde una perspectiva espacial como temporal, debido a que son secuencias de imágenes. Además de esto, debe ser capaz de responder a las imágenes de baile con acciones sonoras a interpretar. Este tipo de problemas es similar al usado en videojuegos, donde de entrada se alimenta con una secuencia de imágenes del videojuego, y el modelo responde con las acciones que debe tomar para continuar jugando. Es por esta razón que el modelo de inteligencia artificial de Sinestes.IA va a estar basado en un estudio denominado <i><a href="http://worldmodels.github.io">“World Models”</a></i> realizado por David Ha y Jürgen Schmidhuber. Este estudio se basa en el concepto de Modelos Mentales de Jay Wright Forrester descritos por él como
  </p>
  <blockquote>
  “La imagen del mundo a nuestro alrededor, que llevamos en nuestra cabeza, es solo un modelo. Nadie se imagina en su cabeza todo el planeta, gobierna o país. Solo se tiene una cantidad selecta de conceptos, y relaciones entre ellos, y usamos estos para representar el sistema real” (J.W. Forrester, 1971, t.d.a)
  </blockquote>
  <p>
  En resumen, el modelo busca generar una comprensión simplista de los datos entrantes y su comportamiento, para a partir de esto actuar en el ambiente. Esto implica que es necesario separar el modelo en dos partes: el modelo del mundo, y el modelo de acciones. El modelo del mundo debe ser capaz de comprender una secuencia de imágenes, lo que implica que debe consistir de una red neuronal convolucional y una red neuronal recurrente, para así poder lidiar con el comportamiento espacial y temporal del baile. Es debido a esto que la estructura macro del proyecto consistirá en estas secciones.
  </p>
  <ol>
    <ol class="alt prefix five-three">
      <li><a href="#five-three-one" class="scrolly">Modelo de comprensión espacial</a></li>
      <li><a href="#five-three-two" class="scrolly">Modelo de comprensión temporal</a></li>
      <li><a href="#five-three-three" class="scrolly">Modelo de acción</a></li>
    </ol>
  </ol>
  <p>
  De esta manera, el flujo de información iniciaría con la secuencia de imágenes entrando al modelo de comprensión espacial, para luego transmitir el resultado de dicha comprensión al modelo temporal. Con esto, la inteligencia artificial sacará una conclusión de lo que está ocurriendo en el baile, y esa conclusión la enviará al modelo de acción, donde generará una hipótesis de los sonidos que deberían acompañar el baile.
  </p>
  <span class="image fit">
    <img src="{{'/images/modelflow.png' | absolute_url}}" alt>
    <p><i>Flujo y estructura del modelo de aprendizaje</i></p>
  </span>
  <header>
    <h3 id="five-three-one">5.3.1.Modelo de comprensión espacial</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Como ha sido mencionado anteriormente, el análisis de imágenes suele realizarse con una arquitectura de red neuronal convolucional. Estos modelos suelen recibir la imagen y entrenarse a partir de lo que se desee obtener de ellas. El problema actual es que se desconoce el resultado que se espera obtener de esta sección. Este tipo de problemas se conoce como aprendizaje no supervisado, ya que son problemas en los que el resultado deseado no está previamente definido.
  </p>
  <p>
  El sistema que se usa en el estudio de “World Models”, y que también será usado en este proyecto, se denomina como Autoencoder. Los autoencoders tienen la labor de codificar y decodificar la información entrante, buscando generar en la salida la misma información que en la entrada. De esta manera, el entrenamiento consiste en evaluar la similitud de los datos entrantes con los generados por el algoritmo.
  </p>
  <p>
  Ahora bien, lo que hace estos modelos especiales, es que en el proceso obligan al modelo a tener que representar los datos en un espacio menor al de la información de entrada. A esto se le llama compresión, y es lo que a nosotros realmente nos interesa de este proceso.
  </p>
  <span class="image fit">
    <img src="{{'/images/cae.png' | absolute_url}}" alt>
    <p><i>Imagen obtenida de <a href="https://www.edureka.co/blog/autoencoders-tutorial/">https://www.edureka.co/blog/autoencoders-tutorial/</a>. Acá la imagén del número 2 (izquierda) se comprime en la capa h (centro), y de esta capa se trata de reconstruir la imagen  original (derecha).</i></p>
  </span>
  <p>
  Como analogía, consideremos la labor de resumir toda una película en un solo párrafo de 500 palabras, de tal forma que luego se pueda usar ese resumen para regrabar toda la película lo más fiel a la original. Ahora consideremos que no solo debe reconstruir una película, sino una gran variedad de películas usando la misma estructura, y solo cambiando algunas cuantas palabras. Si esta tarea se realiza, obliga que cada palabra sea crucial para la reconstrucción de la (o las) películas, y ninguna palabra será malgastada.
  </p>
  <p>
  Este proceso logra reducir la información visual de las imágenes a características relevantes de las mismas, al igual que comprime la cantidad de datos que entran al sistema, facilitando el aprendizaje para las próximas capas del sistema. Este proceso logra capturar el comportamiento espacial del baile, pero no tiene conciencia de cómo el baile se desarrolla en el tiempo.
  </p>
  <span class="image fit">
    <img src="{{'/images/sinestesia-cae.png' | absolute_url}}" alt="convolutional autoencoder">
    <p><i>Demostración de la primera etapa de Sinestes.IA. En este caso la imagen original es comprimida a 128 datos (8x4x4).</i></p>
  </span>
  <header>
    <h3 id="five-three-two">5.3.2.Modelo de comprensión temporal</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Obtenida la versión comprimida de las imágenes, es posible usar esta representación para analizar la evolución del baile en el tiempo. Para lograr esto, el modelo debe tener algún tipo de memoria para recordar la información pasada. Es debido a esto que se utilizará una red neuronal recurrente, que además de recibir la imagen comprimida, recibe información de los procesos anteriores. En este caso específico, se utilizará la arquitectura LSTM (Long Short Term Memory), que ha demostrado ser buena para considerar información tanto cercana como lejana temporalmente. Para generar la comprensión temporal se entrena a la red neuronal a predecir lo que ocurrirá en el futuro según la información pasada. De esta manera, si el algoritmo predice correctamente y de manera consistente, implica que comprende el comportamiento temporal de los datos.
  </p>
  <span class="image fit">
    <img src="{{'/images/sinestesia-lstm.png' | absolute_url}}" alt="lstm">
    <p><i>Demostración de la segunda etapa de Sinestes.IA. Se puede observar cómo se procesa una secuencia de imágenes individualmente (flujo vertical), mientras que cada capa comparte información de los procesos anteriores (flujo horizontal).</i></p>
  </span>
  <p>
  De esta capa nos interesa más la salida intermedia de la red neuronal, ya que es la que representa la comprensión temporal del baile. Una vez obtenido esto, es posible usar esta información como entrada para el modelo de acción.
  </p>
  <header>
    <h3 id="five-three-three">5.3.3.Modelo de acción</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Por último se encuentra la capa de acción. Este modelo se encarga de recibir el análisis del baile, y a partir de esto proponer la acción sonora que lo acompaña. Debido a que las capas anteriores realizan una gran cantidad de trabajo, esta capa puede ser considerablemente más sencilla. Por esta razón, el modelo de acción será una red neuronal completamente conectada, la arquitectura más básica<sup class="tooltip" data-tip="Se ha escogido un modelo sencillo en coherencia con el estudio en el que está basado este proyecto. Es probable que esta opción no genere los mejores resultados, debido a que las acciones sonoras también son datos secuenciales. Como los modelos secuenciales son los más complicados de entrenar, no se optará por usar otra red neuronal recurrente en esta capa."><b>[2]</b></sup>. En este caso, la red neuronal recibe los datos de las salidas intermedias del modelo anterior, y como resultado busca predecir las acciones sonoras que acompañan el baile. Es en este punto en el que se usan los datos sonoros grabados en la base de datos para establecer la relación entre la danza y la música.
  </p>
  <header>
    <h3 id="five-four">5.4.Entrenar el modelo de aprendizaje</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Para entrenar los modelos anteriores se usaron los datos capturados necesarios en cada etapa, empezando por el modelo de comprensión espacial, para luego entrenar el modelo de comprensión temporal y por último entrenar el modelo de acción. Esto es debido a que cada modelo consecuente se entena a partir de los resultados del anterior, por lo que un entrenamiento continuo de todas las etapas no era producente.
  </p>
  <p>
  Aunque se tiene una arquitectura base del modelo, los detalles se definen en el momento de entrenamiento a través de experimentación constante. Se busca elegir los detalles que generen el mejor resultado en cada etapa, por lo que el proceso consiste en entrenar varias veces cada modelo con parámetros distintos, y observar el desempeño en cada labor específica. Una vez obtenido el mejor resultado, se guardan estos parámetros para continuar con la siguiente etapa.
  </p>


<!--
  {% highlight python %}
import h5py
import numpy as np
from PIL import Image

class CAEData:
    def __init__(self,config):
        self.config = config
        self.thresh = 8
        location = '/Volumes/TOSHIBA/TESIS/runtime/data/'
        f = h5py.File(location + 'video_dataset.hdf5','r')
        self.cv_input = f['test_data']
        self.input = f['train_data']
        im = Image.open(location + 'background.jpg')
        background = np.asarray(im)* self.config.background_percent
        self.background = np.reshape(background, self.config.state_size)

    def next_batch(self, batch_size):
        idx = np.random.choice(self.input.shape[0]-batch_size)
        batch_x = self.input[idx:idx+batch_size]
        batch_x = np.rollaxis(batch_x, 1, 4)
        # Remove background and normalize data
        batch_y = np.clip(((batch_x-self.background)-self.thresh)/(255-self.thresh), 0, 1)
        batch_x = batch_x/255
        noise = np.random.normal(0.5,0.5,((batch_size, 128, 128, 1)))
        noise_bool = np.random.normal(0,0.01,((batch_size,1,1,1)))
        batch_x = np.clip((batch_x + self.config.noise_percent*noise_bool*noise),0,1)
        yield batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0]-batch_size)
        batch_x = self.cv_input[idx:idx+batch_size]
        batch_x = np.rollaxis(batch_x, 1, 4)
        batch_y = np.clip(((batch_x-self.background)-self.thresh)/(255-self.thresh), 0, 1)
        batch_x = batch_x/255
        yield batch_x, batch_y
  {% endhighlight %}
  <p>
  Placerat in egestas erat imperdiet sed euismod nisi porta lorem. Amet volutpat consequat mauris nunc congue nisi vitae suscipit. Ultrices vitae auctor eu augue ut. Id nibh tortor id aliquet lectus proin. Malesuada fames ac turpis egestas maecenas pharetra. Aliquam malesuada bibendum arcu vitae elementum curabitur. Ipsum dolor sit amet consectetur. Nibh sed pulvinar proin gravida hendrerit lectus. Nunc sed augue lacus viverra vitae congue eu consequat. Et pharetra pharetra massa massa ultricies. Ut tellus elementum sagittis vitae et leo. Egestas congue quisque egestas diam in. Congue mauris rhoncus aenean vel elit scelerisque mauris. Ullamcorper malesuada proin libero nunc consequat interdum varius. Eu consequat ac felis donec et odio pellentesque diam volutpat. Vulputate sapien nec sagittis aliquam malesuada bibendum arcu.
  </p>
  <!-- /METHODOLOGY -->
  <!-- RESULTS -->
  <header>
    <h3 id="six">6.Resultados</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <div class="box alt">
  		<div class="row 50% uniform">
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic02.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic03.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u$"><span class="image fit"><img src="{{'/images/pic01.jpg' | absolute_url}}" alt=""></span></div>
  			<!-- Break -->
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic04.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic05.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u$"><span class="image fit"><img src="{{'/images/pic01.jpg' | absolute_url}}" alt=""></span></div>
  			<!-- Break -->
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic02.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u"><span class="image fit"><img src="{{'/images/pic04.jpg' | absolute_url}}" alt=""></span></div>
  			<div class="4u$"><span class="image fit"><img src="{{'/images/pic03.jpg' | absolute_url}}" alt=""></span></div>
  		</div>
  	</div>  
    <a href="#" class="button special fit">Generar nuevas imágenes</a>
    <p>
    Morbi leo urna molestie at elementum eu facilisis sed odio. In tellus integer feugiat scelerisque varius morbi. Neque egestas congue quisque egestas diam in arcu cursus. Turpis massa sed elementum tempus egestas sed sed risus pretium. Id eu nisl nunc mi ipsum faucibus vitae. Nulla posuere sollicitudin aliquam ultrices sagittis orci a. Bibendum est ultricies integer quis. Massa tempor nec feugiat nisl. Augue mauris augue neque gravida. Massa eget egestas purus viverra accumsan. Enim neque volutpat ac tincidunt vitae semper.
    </p>
    <p>
    Non nisi est sit amet facilisis. Venenatis tellus in metus vulputate eu scelerisque felis imperdiet. Odio facilisis mauris sit amet massa vitae tortor. Tincidunt dui ut ornare lectus. Neque viverra justo nec ultrices dui. Aliquet risus feugiat in ante metus dictum. Risus pretium quam vulputate dignissim suspendisse in est ante. Id eu nisl nunc mi ipsum faucibus vitae. Diam ut venenatis tellus in metus vulputate eu. Et malesuada fames ac turpis egestas sed tempus urna. Mauris augue neque gravida in fermentum et. Risus in hendrerit gravida rutrum quisque non tellus orci ac. Amet nisl suscipit adipiscing bibendum est. Sit amet facilisis magna etiam tempor. Ultricies lacus sed turpis tincidunt id aliquet. Viverra tellus in hac habitasse platea dictumst vestibulum rhoncus.
    </p>
  <!-- /RESULTS -->
  <!-- CONCLUSION -->
  <header>
    <h3 id="seven">Conclusión</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <p>
  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Aliquet sagittis id consectetur purus ut. Faucibus interdum posuere lorem ipsum dolor. Est ante in nibh mauris cursus mattis molestie a iaculis. Netus et malesuada fames ac. Sapien pellentesque habitant morbi tristique senectus et netus et. Tempor id eu nisl nunc mi ipsum faucibus vitae. Vitae sapien pellentesque habitant morbi tristique senectus et netus et. Consectetur lorem donec massa sapien. Accumsan in nisl nisi scelerisque eu. Eget felis eget nunc lobortis mattis aliquam faucibus. Amet mauris commodo quis imperdiet massa tincidunt nunc pulvinar. Donec ultrices tincidunt arcu non. Commodo quis imperdiet massa tincidunt. Et tortor consequat id porta nibh venenatis cras sed felis. Diam phasellus vestibulum lorem sed risus ultricies tristique nulla aliquet. Aliquam sem et tortor consequat id porta nibh venenatis.
  </p>
  <!-- /CONCLUSION -->
  <!-- BIBLIOGRAPHY -->
  <header>
    <h3 id="biblio">Bibliografía</h3>
    <p><a href="#index" class="scrolly">Volver al inicio</a></p>
  </header>
  <!-- /BIBLIOGRAPHY -->
  <ul>
    <li><a href="https://www.yamaha.com/en/news_release/2018/18013101/
" target="_blank" >Peters, G. (2012). The philosophy of improvisation. Chicago, IL: University of Chicago Press.</a></li>
    <li>Ternaux, J. (2003). Synesthesia: A Multimodal Combination of Senses. Leonardo, 36(4), 321-322. doi:10.1162/002409403322258790</li>
    <li><a target="_blank" href="https://alessiaspadaccini.com/wp-content/uploads/2015/05/Wassily-Kandinsky-y-la-Música-Visual.pdf" >Di Marco, P., & Spadaccini, A. (2015). Wassily Kandinsky y la sinestesia que lo condujo a la música visual. 25-33. Retrieved April 6, 2019.</a></li>
  </ul>
</article>
