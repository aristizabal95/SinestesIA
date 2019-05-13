---
layout: post
title:  "Composiciones"
date:   2019-05-12
excerpt: "Descripción del proceso de composición y demostración de cada obra desarrollada para Sinestes.IA"
image: "/images/parametros.png"
---

La intención de las composiciones es generar ejemplos de cómo la música se relaciona con la danza, al igual que demostrar cómo se manejan los parámetros del entorno sonoro para que el algoritmo pueda luego manipularlos. Estos dos requerimientos implican que las composiciones deben representar el movimiento, y deben hacer uso único del entorno sonoro para desarrollarse.

Como es mencionado en el texto principal, se usarán los esfuerzo-acciones de Laban como medio para parametrizar la música. Esta parametrización implica relacionar características del sonido a los 3 aspectos que definen cada esfuerzo-acción. Dicha parametrización es puramente subjetiva, y fue desarrollada para este proyecto con esa intención. La aproximación a este problema consistió en observar cada esfuerzo-acción, y con base a cada uno imaginarse qué tipos de sonidos acompañarían mejor el movimiento. Una vez establecido esto, se observaban qué características musicales estaban más relacionadas con cada dimensión del movimiento y según esto establecer la relación danza-música.

Esta tabla demuestra las conclusiones a las cuales se llegó de acuerdo al proceso anterior:

<span class="image fit">
  <img src="{{'/images/parametros.png' | absolute_url}}" alt>
</span>

Observando la tabla anterior, se llega a la conclusión que la altura y el timbre están correlacionados al peso del movimiento, mientras que la longitud del sonido está relacionado con el tiempo del movimiento. Las otras características no representan una relación directa, pero también fueron consideradas para el momento de componer.

Esta parametrización funciona como una guía básica para construir los ejemplos musicales, más no representan una estructura rígida, ni completa de las composiciones. Esto significa que se puede reforzar el carácter de cada esfuerzo-acción a partir de otras características sonoras y musicales más específicas, y que se pueden sacrificar ciertas relaciones en pro de la musicalidad de las piezas.

<h2>Las implicaciones del tiempo súbito</h2>

Además de las consideraciones anteriores, es necesario que la relación demostrada en la danza y la música mantenga una correspondencia directa. Para lograr esto, cada acción musical debe ser representada por algún movimiento corporal. Esto representa un reto característico al momento de hablar del tiempo súbito, ya que este abarca tanto la temporalidad de cada movimiento, como de toda la secuencia de movimientos. Un tiempo súbito implica movimientos erráticos, que aparecen de manera impredecible en la danza. Esto implica que para mantener una coherencia directa, la música debe estar construida de manera que sea impredecible y errática.

Para lograr dicho cometido, se diseñó un algoritmo basado en el concepto de <i>Serialismo</i> para evitar dar mucha relevancia a algún patrón rítmico durante las piezas.
rri

<span class="image fit">
  <img src="{{'/images/subito.png' | absolute_url}}" alt>
</span>

El algoritmo se basa en una serie o secuencia de números base del 1 al 7. A cada número se le define un patrón rítmico diferente al resto, de tal forma que cuando el algoritmo decida reproducir un número específico, se ejecutará dicha secuencia rítmica. Con la intención de complicar la recordación de la pieza, el algoritmo alterna entre ejecutar el ritmo o agregar silencio a la pieza, cuya duración también depende del valor de la serie que se esté ejecutando en el momento. La pieza termina una vez se hayan ejecutado todos los bloques rítmicos. Por último, las alturas de las notas son escogidas a través de un algoritmo pseudoaleatorio, el cual recibe como secuencia semilla la serie de la pieza. Esto si bien no implica que las alturas no se repetirán, implicarán un nivel alto de incertidumbre.

Otro reto con las piezas de característica súbita es la recordación por parte del bailarín. Considerando que estas composiciones buscan impredecibilidad, el bailarín tiene muy pocas herramientas para recordar toda la obra y ejecutarla. Por esta razón, se tuvo que reducir el nivel de incertidumbre en las composiciones, asegurándose que las piezas tuvieran una métrica estable, y que los bloques rítmicos fueran de una duración máxima de dos compases. Además, para facilitar la interpretación de cada obra al momento de grabar, la pieza se reproducía dos veces de manera instantánea: una pista que era la que los bailarines debían interpretar al tiempo, y la misma pista reproducida con dos compases de anticipación. Esto generaba un efecto de pregunta-respuesta, en el que el bailarín primero escuchaba la secuencia rítmica para inmediatamente después ejecutarla encima de la pista real.

<h2>Descripción de cada composición</h2>
<header>
  <h3 id="four">Flotar</h3>
  <p>Sostenido, Ligero, Indirecto</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/flotar.mp3' | absolute_url}}" />
</audio>
Este esfuerzo-acción fue el primero trabajado, y requirió de varias iteraciones para llegar a esta composición, ya fuera por un mal manejo de la parametrización, o por resultados de longitud inaceptables para la captura de los datos. Esta composición consta 3 voces sonando homorrítmicamente. La estructura de la pieza busca ser predecible, a través de repeticiones de frases, y de un ritmo base constante. Es a partir de esto, al igual que el uso de ataques largos, que se representa la temporalidad sostenida del movimiento. Por otro lado, el uso de notas agudas y timbres redondos permite ejemplificar el peso ligero que define este esfuerzo-acción. Por último, el vibrato, y el uso exagerado de reverberación, reflejan la espacialidad indirecta de la obra.

<header>
  <h3 id="four">Deslizar</h3>
  <p>Sostenido, Ligero, Directo</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/deslizar.mp3' | absolute_url}}" />
</audio>
En esta composición se hace uso exagerado del glissando para representar el movimiento de deslizamiento. Por otro lado, al igual que con Flotar, el carácter sostenido se representa con notas largas, dirección clara y una secuencia rítmica constante. Debido a que su peso es ligero, también se hace uso de notas agudas durante toda la pieza. La característica directa fue representada a partir de la ausencia de vibrato y de reverberación. En esta pieza se hizo uso de delays, que ofusca el carácter directo. Aún así, fue utilizado debido a preferencias estéticas.

<header>
  <h3 id="four">Retorcer</h3>
  <p>Sostenido, Enérgico, Indirecto</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/retorcer.mp3' | absolute_url}}" />
</audio>
Esta composición demuestra el carácter pesado y enérgico a través de su atmósfera oscura, timbres estridentes y alturas bajas. En esta, a diferencia del resto, entra el acompañamiento primero, para luego ser desarrollada con una melodía. El uso de glissandos exagerados, delays y reverberación ejemplifican el carácter indirecto de la obra, mientras que la duración larga de las notas, sus entradas graduales y la estructura predecible de la pieza caracterizan la temporalidad sostenida.

<header>
  <h3 id="four">Presionar</h3>
  <p>Sostenido, Enérgico, Directo</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/presionar.mp3' | absolute_url}}" />
</audio>
El carácter enérgico de este esfuerzo-acción diferencia esta composición de las anteriores a través del uso constante de sonidos bajos y ricos armónicamente. Al igual que la anterior composición, se hace uso de más de una voz para generar armonías, aunque estas se mantienen en unísono. La característica de espacialidad directa se ve mucho mejor refleja en esta pieza, debido a la ausencia de reverberaciones y delays. Por último, el carácter de temporalidad se ve altamente demostrado aquí con el manejo de envolventes largas, haciendo que los sonidos entren y salgan de manera gradual.

<header>
  <h3 id="four">Tocar</h3>
  <p>Súbito, Ligero, Directo</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/tocar.mp3' | absolute_url}}" />
</audio>
Esta pieza demuestra el uso del sistema súbito desarrollado para las piezas con este carácter temporal. La temporalidad se ve además reflejada por la duración de las notas, que es bastante corta. Por otro lado, alturas agudas y timbres redondos demuestran el peso del esfuerzo acción, mientras que la ausencia de efectos y de glissando representan la espacialidad. Acá se puede escuchar el algoritmo original para la generación de estas piezas, que fue diseñado para generar obras de una longitud cercana al minuto. Esta longitud fue luego recortada debido a que era poco práctico al momento de grabar la interpretación del bailarín. Para nivelar esta diferencia de tiempos, se grabaron más veces las piezas súbitas con cada bailarín, comparado a las piezas sostenidas.

<header>
  <h3 id="four">Sacudir</h3>
  <p>Súbito, Ligero, Indirecto</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/sacudir.mp3' | absolute_url}}" />
</audio>
En esta pieza se busca demostrar un carácter ligero únicamente a través de las alturas agudas, para explorar timbres más estridentes. Por otro lado, la espacialidad se reflejada con el uso exagerado de delays y reverberación. Acá se puede observar la longitud promedio en la cual se realizaron las grabaciones de este tipo de piezas, que es mucho más corta que la pensada anteriormente con Flotar.

<header>
  <h3 id="four">Atacar</h3>
  <p>Súbito, Enérgico, Indirecto</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/atacar.mp3' | absolute_url}}" />
</audio>
El esfuerzo-acción “Atacar” suele verse ejemplificado a través de los movimientos rápidos realizados para cortar maleza con un machete. Es por esta razón, que esta busca reflejar el sonido del viento al verse perturbado por tales movimientos. Esto implicó un manejo de ruido en la obra, el cual fue filtrado y reverberado, para representar el peso enérgico y la espacialidad indirecta.

<header>
  <h3 id="four">Golpear</h3>
  <p>Súbito, Enérgico, Directo</p>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/golpear.mp3' | absolute_url}}" />
</audio>
Las características de Golpear pueden ser fácilmente reflejadas a través de sonidos percutidos, principalmente sonidos de tambores bajos como el bombo. Es debido a esto que se diseñó esta obra a partir de dichos sonidos. Se agregó, además, el sonido de hi-hat, con la intención de generar mayor variedad sonora a este esfuerzo-acción.

<h2>Composiciones Anteriores</h2>
Antes de desarrollar todas las obras, se realizó una prueba del concepto con dos esfuerzo-acciones opuestos: <i>Flotar</i> y <i>Golpear</i>. Estas composiciones fueron realizadas con el objetivo de realizar las primeras pruebas del sistema de aprendizaje, y diagnosticar la dificultad del proyecto, al igual que el rendimiento que cada etapa. Estas piezas son claramente distintas a las anteriores, debido a que fueron desarrolladas sin una parametrización totalmente definida, y a que se desconocía la relevancia del carácter súbito en la relación danza-música.

<header>
  <h3 id="four">Flotar</h3>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/flotar-old.mp3' | absolute_url}}" />
</audio>
Esta composición fue la primera realizada, con la cual se desarrolló la prueba de concepto. Esta fue construida a partir de la escala pentatónica, haciendo alusión al manejo realizado por Debussy y Ravel para representar imágenes suaves en sus obras. Se siguen viendo representadas las características indicadas en las composiciones finales, aunque es claro que no fueron estructuradas con el objetivo de facilitar tanto el aprendizaje por parte del algoritmo, como la grabación o captura de datos debido a su longitud.

<header>
  <h3 id="four">Golpear</h3>
</header>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/golpear-old.mp3' | absolute_url}}" />
</audio>
Esta composición fue la primera realizada, con la cual se desarrolló la prueba de concepto. Esta fue construida a partir de la escala pentatónica, haciendo alusión al manejo realizado por Debussy y Ravel para representar imágenes suaves en sus obras. Se siguen viendo representadas las características indicadas en las composiciones finales, aunque es claro que no fueron estructuradas con el objetivo de facilitar tanto el aprendizaje por parte del algoritmo, como la grabación o captura de datos debido a su longitud.

Esta composición está construida a partir de varios sonidos percutidos, un sonido bajo de larga duración, y varios sonidos cortos agudos en donde se desarrolla la melodía y acompañamiento armónico de la obra.
