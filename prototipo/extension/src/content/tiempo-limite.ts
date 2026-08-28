/**
 * El seguro que impide que el indicador quede girando para siempre.
 *
 * El *content script* pide el análisis por mensaje al *service worker*, que es
 * quien tiene los permisos de red. Ese mensaje tiene su propio tiempo límite
 * sobre la petición HTTP, así que casi todas las fallas —el servicio caído, el
 * proveedor sin responder, una respuesta con error— vuelven como respuesta y el
 * indicador pasa a su estado de falla sin ayuda de nadie.
 *
 * Queda un caso que ninguna de esas defensas cubre: que el *service worker*
 * **nunca conteste**. En Manifest V3 el *service worker* no es un proceso
 * permanente; el navegador lo termina cuando lo considera inactivo, y si eso
 * ocurre entre el envío del mensaje y su respuesta, la promesa de
 * `sendMessage` puede quedar pendiente sin resolverse ni rechazarse. El
 * resultado visible es exactamente el que RF-08 y la historia 18 de la *spec*
 * prohíben: un indicador en estado transitorio para siempre, delante del
 * tribunal.
 *
 * Por eso el seguro vive **acá**, del lado del *content script*, y no en el
 * *service worker*: un componente no se puede vigilar a sí mismo cuando el modo
 * de falla es que deje de existir.
 *
 * El plazo es deliberadamente más largo que el del *service worker*, para que
 * en toda falla normal gane el mensaje —que trae una explicación de qué pasó— y
 * este corte quede como lo que es: el último recurso.
 */

/**
 * Plazo del seguro, holgado sobre el tiempo límite del *service worker*.
 *
 * Su trabajo no es hacer cumplir el presupuesto de latencia de RNF-02 —de eso
 * se encarga el servicio, que al agotar el suyo devuelve un análisis parcial
 * explicado—, sino garantizar que el estado transitorio termine siempre.
 *
 * De ahí que sea el plazo más largo de los tres. El orden es deliberado y hay
 * que conservarlo: presupuesto del servicio (45 s, hasta ~60 s si un paso ya
 * arrancó) < tiempo límite del *service worker* (75 s) < este seguro (85 s).
 * Invertirlo es lo que hacía que un análisis que el servicio completaba llegara
 * al ciudadano como una falla.
 */
export const LIMITE_DEL_INDICADOR_MS = 85_000;

/** Lo que ve el ciudadano cuando salta el seguro. */
export const MENSAJE_DE_CORTE = 'El análisis no respondió a tiempo';

/**
 * Devuelve la promesa recibida, o falla al vencer el plazo.
 *
 * El temporizador se cancela en cuanto la promesa se resuelve, para no dejar
 * uno vivo por cada tuit que se analiza en la *timeline*.
 */
export function conTiempoLimite<T>(
  promesa: Promise<T>,
  milisegundos: number = LIMITE_DEL_INDICADOR_MS,
  mensaje: string = MENSAJE_DE_CORTE,
): Promise<T> {
  let temporizador: ReturnType<typeof setTimeout>;

  const corte = new Promise<never>((_, rechazar) => {
    temporizador = setTimeout(() => rechazar(new Error(mensaje)), milisegundos);
  });

  return Promise.race([promesa, corte]).finally(() => clearTimeout(temporizador));
}
