/**
 * Cómo se dice en la interfaz el puntaje que el servicio devuelve.
 *
 * El servicio estima una **probabilidad de desinformación**: cuanto más alta,
 * peor. Dicho así en pantalla, el número y el color de la tarjeta apuntaban en
 * direcciones opuestas —«30 % de desinformación» en verde, «84 %» en rojo—, de
 * modo que un veredicto favorable se anunciaba con la cifra más chica y había
 * que leer el rótulo entero para saber para qué lado va. Un indicador que hay
 * que aprender a leer incumple RNF-15.
 *
 * Acá se invierte una sola vez y se lee al derecho: **probabilidad de que la
 * afirmación sea verdadera**. Grande y verde es buena noticia; chica y roja, la
 * contraria. Es la misma cifra enunciada por su complemento, no un dato nuevo:
 * la estimación es binaria y las dos lecturas dicen exactamente lo mismo.
 *
 * Vive en su propio módulo porque la usan las dos superficies de la tarjeta —la
 * ficha y el detalle— y son la misma tarjeta: si una invirtiera y la otra no,
 * la pieza se contradiría a sí misma a noventa píxeles de distancia.
 */

/** La cifra que se muestra, ya invertida y redondeada a entero. */
export function porcentajeDeVeracidad(puntajeFinal: number): number {
  return Math.round((1 - puntajeFinal) * 100);
}

/**
 * El rótulo que acompaña a la cifra grande del detalle.
 *
 * Nombra lo que el número mide. Un porcentaje nunca viaja solo.
 */
export const ROTULO_DE_VERACIDAD =
  'Probabilidad estimada de que la afirmación sea verdadera';

/**
 * La misma cifra para el renglón de la ficha, donde comparte lugar con las
 * fuentes y por lo tanto se dice en menos palabras.
 *
 * Se conserva la palabra «probabilidad»: «70 % verdadera», a secas, se lee como
 * que la afirmación es verdadera en un 70 % —parcialmente cierta—, que es un
 * juicio distinto del que el sistema emite y uno que no puede sostener.
 */
export function lineaDeVeracidad(puntajeFinal: number): string {
  return `${porcentajeDeVeracidad(puntajeFinal)}% de probabilidad de ser verdadera`;
}
