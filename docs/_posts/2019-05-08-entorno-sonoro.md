---
layout: post
title:  "Entorno Sonoro"
date:   2019-05-08
excerpt: "Una exploración detallada de la construcción del entorno sonoro y las posibilidades sonoras que ofrece."
image: "/images/instrument.png"
---

El ambiente sonoro de Sinestes.IA debe ser diseñado con el propósito de ofrecer la mayor cantidad de variedad sonora y textural en un número reducido de parámetros. De esta manera, el modelo de inteligencia artificial no se verá limitado por la diversidad sonora, sino por sus capacidades de aprendizaje. Además de esto, la sonoridad del entorno sonoro debe poder ser completamente representada en todo momento por los parámetros que el programa va a manipular, lo que significa que el algoritmo tendrá control absoluto de lo que está sonando en este entorno.

Para lograr representar la sonoridad del entorno sonoro, los parámetros no solo deben capturar la información de intensidad y altura de cada voz o línea que se piense manejar, sino que además deben capturar las características sonoras, tímbricas y temporales de cada sonido. Esto lo diferencia del protocolo MIDI, ya que este no encapsula la información sonora, sino las instrucciones de interpretación que debe manejar el instrumento que uno decida. Para lograr esto, se desarrolló un instrumento como un componente aislado del entorno sonoro, el cual encapsula todos los requerimientos anteriores. De esta forma, se puede construir el entorno sonoro a partir de múltiples instrumentos, cuya construcción es idéntica, reduciendo la complejidad del entorno, y maximizando la variedad sonora del mismo.

Los parámetros del instrumento deben contener información que indique la intensidad, altura, envolvente, timbre, volumen, paneo y demás agregados que afecten la sonoridad del instrumento. A partir de esto, el instrumento se desarrolló de la siguiente manera.

De esta manera, el instrumento recibe como entrada en el siguiente orden:
<ol>
  <li><h5>Velocity:</h5>Similar al protocolo MIDI, este es un valor de 0 a 127 que representa la intensidad interpretativa del sonido.</li>
  <li><h5>Amplitud de ataque:</h5>Este es un valor de 0 a 1 que representa el porcentaje de intensidad al que llega el instrumento durante el ataque de la envolvente.</li>
  <li><h5>Tiempo de ataque:</h5>Indica la duración de la etapa de ataque en milisegundos.</li>
  <li><h5>Curva de ataque:</h5>Es un valor binario (0,1) que indica si la curva es lineal o logarítmica respectivamente.</li>
  <li><h5>Amplitud de decay:</h5>Representa el porcentaje de intensidad en la etapa de decay. Esta será la misma amplitud usada para el sustain.</li>
  <li><h5>Tiempo de decay:</h5>Indica la duración de la etapa de decay en milisegundos.</li>
  <li><h5>Curva de decay:</h5>Valor binario que indica el tipo de curva de la etapa de decay.</li>
  <li><h5>Tiempo de sustain:</h5>Indica la duración de la etapa de sustain.</li>
  <li><h5>Note-off trigger:</h5>Indica si el tiempo de sustain dependerá de un mensaje de note-off, que en este caso sería un Velocity de cero. De ser así, el tiempo de sustain es ignorado, para depender del velocity.</li>
  <li><h5>Tiempo de release:</h5>Indica el tiempo que se demora el sonido en silenciarse desde que termina la etapa de sustain.</li>
  <li><h5>Curva de release:</h5>Indica si la curva de la etapa de release es lineal o logarítmica.</li>
  <li><h5>Velocity-dependent:</h5>Valor binario que señala si la intensidad de la envolvente depende del velocity, o si se usará el velocity como trigger únicamente. Esta es más una herramienta para el intérprete que para el modelo.</li>
  <li><h5>Reverse:</h5>Valor binario que indica si se desea reproducir la envolvente en reversa. Esto permite generar sonoridades de sonidos reproducidos en reversa.</li>
  <li><h5>Frecuencia:</h5>Representa la altura del sonido en términos de frecuencia. Puede variar entre 20Hz y 20kHz.</li>
  <li><h5>Tipo de oscilador:</h5>es un número del 0 al 4, que permite variar de manera continua entre múltiples tipos de forma de onda. 0 es sinusoidal, 1 es triangular, 2 es diente de sierra, 3 es cuadrada y 4 es ruido blanco. Si el valor es intermedio a los previamente indicados, entonces es una mezcla de las dos formas de onda más cercana. Por ejemplo 0.5 es la combinación de sinusoidal con triangular en magnitudes iguales.</li>
  <li><h5>Tiempo de glissando:</h5>Representa el tiempo que se demora el instrumento en pasar de una altura a otra. Si es 0 significa que no hay glissando.</li>
  <li><h5>Tasa de FM:</h5>Valor que representa la relación entre la frecuencia portadora y moduladora en la etapa de FM.</li>
  <li><h5>Cantidad de FM:</h5>Valor que representa la cantidad de modulación en la etapa de FM. 0 representa sin FM.</li>
  <li><h5>Tipo de oscilador FM:</h5>Este valor define la forma de onda a usar como moduladora del FM, y se comporta como el parámetro “Tipo de oscilador”.</li>
  <li><h5>Compresor:</h5>Valor de 0 a 5 que representa una cantidad específica de compresión. Esto se logra haciendo uso del objeto <code>compressor</code> de Pure Data, que lamentablemente no específica lo que representa exáctamente cada valor.</li>
  <li><h5>Filtro pasa altos:</h5>Representa la frecuencia de corte del filtro pasa altos. 0 significa sin filtro.</li>
  <li><h5>Filtro pasa bajos:</h5>Representa la frecuencia de corte del filtro pasa bajos. 20000 es equivalente a sin filtro.</li>
  <li><h5>Tiempo de delay:</h5>El tiempo en milisegundos entre cada repetición del delay.</li>
  <li><h5>Cantidad de delay:</h5>Valor que representa el porcentaje de nivel de salida del delay en comparación al nivel de entrada. 100% representa mismo nivel de entrada.</li>
  <li><h5>Damping de reverberación:</h5>Valor que representa el porcentaje de amortiguación de sonido en la etapa de reverberación.</li>
  <li><h5>Tamaño de cuarto:</h5>Valor de 0 a 1 que representa el tamaño de cuarto en la reverberación.</li>
  <li><h5>Dry/Wet:</h5>Relación entre sonido reverberado y sonido limpio.</li>
  <li><h5>Volumen:</h5>Valor de 0 a 1 que representa el nivel de volumen a la salida del instrumento.</li>
  <li><h5>Paneo:</h5>Valor de -1 a 1 que representa la posición estéreo del instrumento.</li>
</ol>

Con esto podemos representar todo el estado de un instrumento en 29 valores individuales. Es importante destacar que esta definición fue realizada previamente a las composiciones, y algunos de estos parámetros no fueron manipulados en las bases de datos. Esto significa que se podría definir un número de parámetros menor a este, pero con la intención de mantener una consistencia con la idea de ofrecer la mayor variedad posible se mantendrán dentro de la definición del instrumento.

Habiendo desarrollado, y encapsulado toda la idea de un instrumento bajo estos parámetros, se puede especificar el tipo de sonido a producir asignando valores a cada parámetro. Como ejemplo:

<h3>Bombo</h3>
<span class="image fit">
  <img src="{{'/images/kick.png' | absolute_url}}" alt>
</span>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/kick.wav' | absolute_url}}" />
</audio>
Este ejemplo demuestra qué parámetros usar para generar sonidos percutivos bajos como el bombo de una batería.
<h3>Flauta</h3>
<span class="image fit">
  <img src="{{'/images/flute.png' | absolute_url}}" alt>
</span>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/flute.wav' | absolute_url}}" />
</audio>
Acá podemos ver la versatilidad del instrumento, ya que sin haber modificado la arquitectura pudimos obtener un sonido contrastante al bombo modificando los parámetros. En este caso, hacemos uso del FM con una tasa tan baja que actúa como un LFO, generando un efecto de vibrato en la nota.
<h3>Sonido dinámico</h3>
<span class="image fit">
  <img src="{{'/images/estridente.png' | absolute_url}}" alt>
</span>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/synth.wav' | absolute_url}}" />
</audio>
Se pueden encadenar mensajes para generar sonoridades más interesantes. En este caso, hacemos uso del glissando para cambiar de altura de manera gradual, y haciendo uso de la síntesis FM, del compresor y de los filtros se obtiene un timbre interesante.
<h3>Arpegio</h3>
<span class="image fit">
  <img src="{{'/images/arpegio.png' | absolute_url}}" alt>
</span>
<audio class="js-player" controls preload>
  <source src="{{ 'audios/arp.wav' | absolute_url}}" />
</audio>
El encadenamiento de mensajes también permite generar secuencias, lo cual abre la posibilidad a construir melodías en un solo instrumento. Acá se hace uso del delay para mantener el arpeggio por más tiempo.

La única limitante del instrumento es que es una única fuente sonora, lo que significa que por diseño es monofónico. Para poder aumentar la textura del entorno sonoro, es por lo tanto necesario usar más de un instrumento. Priorizando la variedad sonora, se ha decidido manejar 6 instrumentos independientes, lo que puede ser usado como 4 voces para armonía y melodía, y dos para percusión o efectos. De esta forma se diseñó el entorno sonoro, el cual es usado tanto por la inteligencia artificial como para la construcción de las composiciones.
