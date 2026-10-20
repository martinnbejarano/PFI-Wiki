/**
 * Aviso de primer uso (Ley 25.326, art. 12; Decreto 1558/2001, art. 5).
 *
 * Hasta que se acepta, el *service worker* no le manda nada al servicio salvo
 * la comprobación de vida. La aceptación se guarda con la versión del texto:
 * si el texto cambia, se sube `VERSION_AVISO` y se vuelve a pedir.
 */

export const VERSION_AVISO = 1;

export const PUNTOS_DEL_AVISO: readonly string[] = [
  'El resultado lo produce un sistema automático que usa un modelo de lenguaje, sin revisión humana.',
  'Puede equivocarse. Si un veredicto te parece incorrecto, podés informarlo desde el detalle del análisis.',
  'El resultado juzga la afirmación, no a la persona que la publicó.',
  'Las fuentes enlazadas son de terceros: Factum no responde por su contenido.',
  'La extensión envía al servicio de Factum el texto de las publicaciones que ves y, cuando pedís un ' +
    'análisis, también la cuenta autora. El servicio guarda la cuenta solo como seudónimo y, para el ' +
    'análisis, le pasa el texto, sin el nombre de usuario, a un proveedor externo de modelos de lenguaje ' +
    '(OpenAI) con servidores en Estados Unidos, un país que ' +
    'la normativa argentina no reconoce con un nivel de protección de datos adecuado (Ley 25.326, art. 12). ' +
    'Al aceptar, consentís esa transferencia.',
  'La extensión es para uso personal.',
];

export const AVISO_PENDIENTE = 'Antes de analizar, aceptá el aviso de uso desde la ventana de Factum';

export async function avisoAceptado(): Promise<boolean> {
  return (await chrome.storage.local.get('avisoAceptado')).avisoAceptado === VERSION_AVISO;
}

export function aceptarAviso(): Promise<void> {
  return chrome.storage.local.set({ avisoAceptado: VERSION_AVISO });
}
