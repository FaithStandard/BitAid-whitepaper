# Bitaid: ayuda en emergencias, pagada de persona a persona en Bitcoin

Noviembre de 2026 · [@fiatstandard](https://x.com/fiatstandard)

Bitaid permite que una persona en peligro llame a gente capaz que está cerca y le pague, sin centralita, sin token y sin ninguna empresa en medio. Cada pago en que puede terminar el caso se firma antes de que nadie tenga motivo para disputarlo, así que quien decide el resultado puede elegir uno, pero nunca quedarse el dinero. Ya funciona de principio a fin en la red pública de pruebas de Bitcoin, a través de Tor, entre un PC, un móvil y una tableta.

## El problema

La violencia se decide en los minutos entre el ataque y la respuesta. La defensa propia siempre está, pero una persona contra varias está en desventaja; lo que cambia el desenlace es que lleguen una segunda y una tercera persona capaces en cuestión de minutos.

Hoy el seguro paga después del daño. El rescate en el momento casi no se vende en ningún sitio, y nada permite pagar a quien, siendo capaz, pueda llegar primero. La seguridad privada factura horas, no resultados, así que protege lugares de quien puede pagar horas muertas. La policía es un monopolio: sin precios, sin rivales y sin clientes que puedan irse, no puede saber cuánto vale la protección ni para quién. Bitaid paga el problema resuelto, no las horas que se pasan esperándolo.

## La palanca del seguro

Una oferta de Bitaid queda en depósito por adelantado y no cuesta nada hasta que se usa: el dinero espera como bitcoin sin gastar, sin pagar sueldos por horas muertas. Y como las emergencias rara vez golpean a las mismas personas a la vez, una aseguradora puede respaldar muchas ofertas con un mismo depósito.

Mil personas pagando dos dólares al mes pueden, cada una, pedir ayuda con una oferta de 8.000 $: un apalancamiento de unos trescientos a uno. Ese apalancamiento descansa en que las emergencias son raras y dispersas, y en que la aseguradora mantiene reservas propias para los años malos; la prima pone precio a ambas cosas. Suscribirlo permite que el capital en bitcoin rinda bitcoin asumiendo riesgos reales, sin prestarlo. Recompensas de ese tamaño atraen a los respondedores más capaces y financian los equipos, drones y médicos que compiten por llegar primero.

Y entonces manda el propio interés de la aseguradora. Con suficiente capital comprometido, le compensa mantener sus propios vigilantes y patrullas cerca de sus clientes: disuaden las emergencias que sus ofertas tendrían que pagar y, cuando ocurre una, son los primeros en llegar y recuperan la recompensa que ella misma depositó. Menos siniestros permiten primas más bajas, que atraen más clientes, cuyas primas financian más patrullas. Ese círculo virtuoso convierte a las aseguradoras en proveedoras de seguridad que compiten en precio y en rapidez, pagadas por resultados y no por horas muertas.

Bitaid no decreta un derecho a la seguridad ni convence a nadie de pagarla; sube el precio que se paga por salvar vidas y bienes, y deja que el mercado responda.

## Cómo se resuelve un caso

1. **Antes de cualquier emergencia**, quien llama (o su aseguradora) deja una oferta en depósito en bitcoin. Queda en un script que nadie puede gastar a solas; si la emergencia nunca llega, vuelve a su dueño.
2. **La alerta** llega a los respondedores con fianza de la zona. Cada uno que acepta deposita su propia fianza.
3. **En cerca de un minuto**, los dispositivos de las partes firman cada pago en que puede terminar el caso: en la red pública de pruebas, 39 pagos posibles para tres respondedores. Después no se puede añadir ninguno.
4. **Todos graban.** Quien reclama un pago debe probar lo que hizo con su propia grabación, así que cada escena queda filmada desde varios ángulos. Cada grabación se resume en un hash y se ancla en Bitcoin.
5. **Votan los que estuvieron allí**, a ciegas y punto por punto: quién acudió, quién ayudó, qué pasó. Si coinciden, queda resuelto.
6. **Si no coinciden**, árbitros seudónimos sorteados responden preguntas de hecho concretas sobre las grabaciones. Cada uno arriesga su fianza si se equivoca. Una parte puede pagar un panel mayor, y una muestra de veredictos la revisan de nuevo tres paneles nuevos.
7. **Una atestación elige uno de los pagos ya firmados** y se emite. El dinero va directo del depósito a quienes se lo ganaron.

## Por qué hacer trampa no compensa

- **Quien decide nunca tiene el dinero.** Elige entre pagos firmados de antemano, cada uno solo a las partes. Ningún resultado le paga a él. Un fallo equivocado aún puede elegir el pago equivocado, y para eso están las fianzas, las revisiones y la restitución.
- **Cada rol deposita una fianza mayor que lo que podría ganar haciendo trampa.** Un árbitro que vota contra el fallo final pierde parte de ella.
- **Falsear la escena es lo difícil.** Una grabación con su hash desde el momento de tomarla no se puede editar después, y una escena montada tiene que sostenerse ante varias cámaras independientes y ante quienes estuvieron allí.
- **El peso se gana, no se compra.** El voto de un respondedor cuenta según el trabajo pagado que hizo en esa zona; el puesto de un árbitro, según los casos que ya juzgó. Ambos maduran con un tiempo de calendario que nadie puede comprar.
- **Cualquier caso se puede reabrir.** Si tres paneles nuevos revocan un veredicto, se incauta toda la fianza del caso a quienes lo votaron, y con ella se indemniza a los perjudicados.
- **Nada que capturar.** Sin token, sin empresa, sin administrador, sin votaciones de gobierno. El orden y la firmeza vienen de Bitcoin.

## Lo que ya funciona

Un prototipo en Rust ejecuta todos los roles: quienes llaman, respondedores, archivistas, el grupo oráculo de firma por umbral y los árbitros. Cada comprobación de abajo es un script que pasa o falla en una cadena real, con los registros publicados.

| Fecha | Dónde | Qué se probó | Resultado |
| --- | --- | --- | --- |
| 9 nov. 2026 | Signet pública de Bitcoin, por Tor, PC + móvil + tableta | Todos los plazos contados en bloques. El veredicto de un panel capturado quedó sin apelar; tres paneles de revisión nuevos lo revocaron, y los dos árbitros que lo respaldaron perdieron toda su fianza a favor de los perjudicados | [81 superadas, 1 fallida](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_public_signet_blocks_2026-11-09.txt) |
| 8 nov. 2026 | Liquid testnet | Los depósitos: financiación, un incidente cofirmado por el grupo, los pagos prefirmados, una atestación equivocada rechazada por la red, la pérdida de una fianza, la salida por bloqueo temporal | [15 superadas, 0 fallidas](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_liquid_testnet_2026-11-08.txt) |
| 7 nov. 2026 | Signet pública de Bitcoin, por Tor, PC + móvil + tableta | La revisión escalonada: tres paneles nuevos revocan un veredicto; los árbitros equivocados pierden su fianza, que indemniza al respondedor perjudicado y al disidente que acertó | [74 superadas, 0 fallidas](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_public_signet_review_2026-11-07.txt) |
| 7 nov. 2026 | La misma prueba, con un extraño hostil | Avalanchas de mensajes, basura, mensajes enormes y repetidos, alturas de bloque falsas y tormentas de conexiones contra la red mientras corría el caso. El caso terminó y todos los nodos rechazaron la altura falsa | Sin alteraciones |
| 6 nov. 2026 | Signet pública de Bitcoin, por Tor | Un caso disputado completo: voto dividido, dos niveles de arbitraje, una apelación, plazos incumplidos reemplazados, sanciones, todos los pagos en cadena | [71 superadas, 0 fallidas](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_public_signet_2026-11-06.txt) |
| 29 oct. 2026 | Signet privada, por Tor | El mismo caso en una red de pruebas privada | [84 superadas, 0 fallidas](https://github.com/FaithStandard/Bitaid-prototype/blob/main/results/m3_signet_tor_2026-10-29.txt) |
| oct. 2026 | Simulaciones económicas | Ocho experimentos, miles de casos cada uno: el trabajo honesto da beneficio; los veredictos perezosos, comprados o montados pierden con las reglas adoptadas | [Reproducibles con un solo comando](https://github.com/FaithStandard/Bitaid-prototype/tree/main/sim) |

## Lo que aún falta

- **Todos los nodos son nuestros por ahora.** Los tramposos de estas pruebas hacen trampa porque un script se lo indica. Operadores independientes, con sus propias estrategias, son el siguiente hito.
- **Una moneda de comisión de menos.** En la última prueba a un respondedor le faltó una moneda para pagar la comisión de un pago; otra parte lo emitió y todos los depósitos se liquidaron. La corrección espera a la próxima prueba.
- **Aún no hay revisión externa** de la criptografía (FROST, MuSig2, los scripts) ni de los incentivos.
- **Solo monedas de prueba.** El prototipo no debe custodiar fondos reales.

## Cómo ayudar

- **Opera un nodo** en el piloto de pruebas que viene, e intenta romperlo. Los ataques que funcionan son lo más útil que alguien puede enviar.
- **Revisa la criptografía**: el oráculo por umbral (FROST con ROAST), los conjuntos de pagos prefirmados (MuSig2) y los scripts Taproot.
- **Ataca los incentivos**: las simulaciones son abiertas; cambia un supuesto y mira qué se rompe.
- **Pruébalo en un piloto**: aseguradoras, empresas de seguridad y comunidades donde la ayuda llega tarde o no llega.

Issues y pull requests son bienvenidos en ambos repositorios.

## Para leer más (en inglés)

- [Whitepaper](https://bitaid-whitepaper.pages.dev/): el argumento completo
- [Especificación](https://bitaid-whitepaper.pages.dev/bitaid_v6_specification.html): scripts, mensajes, parámetros y el registro de cada prueba
- [Prototipo](https://github.com/FaithStandard/Bitaid-prototype): el código en Rust, los registros de pruebas y las simulaciones
