// Chequeo del deck renderizado (issue #113). Lo cargan index.html y factum.html
// cuando la URL lleva `?chequeo`; mira lo que ve el evaluador, no el CSS:
//   1. ningún texto visible de una lámina principal mide menos de 32 px;
//   2. las duraciones de las láminas principales suman 600 s;
//   3. no queda ninguna cifra o expresión obsoleta del 50 %;
//   4. todas las imágenes cargan.
// Escribe el resultado en <pre id="chequeo"> y en la consola. Se corre con
// `presentacion/chequear.sh [deck.html]`, o abriendo <deck>.html?chequeo en el navegador.
(function(){
  var MIN=32, TOTAL=600;
  var OBSOLETAS=[/0,654/, /Entrega 4/i, /124 páginas/i, /veinte segundos/i,
    /(^|[^\d,])20(,\d+)? ?(s|seg|segundos)\b/i, /probabilidad/i, /ficticio/i, /pesa cero/i];
  var fallas=[];
  // index.html muestra la lámina con .on; factum.html, con .active.
  var VISIBLE=document.getElementById('deck')?'on':'active';
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var principales=slides.filter(function(s){ return !s.classList.contains('backup'); });

  // 1 · tamaño de letra calculado, lámina por lámina
  principales.forEach(function(s){
    var n=slides.indexOf(s)+1, estaba=s.classList.contains(VISIBLE);
    s.classList.add(VISIBLE);
    var w=document.createTreeWalker(s, NodeFilter.SHOW_TEXT), t;
    while((t=w.nextNode())){
      if(!t.nodeValue.trim()) continue;
      var el=t.parentElement;
      if(!el.getClientRects().length) continue;
      var fs=parseFloat(getComputedStyle(el).fontSize);
      if(fs<MIN) fallas.push('lámina '+n+': «'+t.nodeValue.trim().slice(0,40)+'» mide '+fs+' px');
    }
    if(!estaba) s.classList.remove(VISIBLE);
  });

  // 2 · duración
  var suma=principales.reduce(function(a,s){ return a+(+s.dataset.t||0); },0);
  if(suma!==TOTAL) fallas.push('las láminas principales suman '+suma+' s y no '+TOTAL);

  // 3 · cadenas obsoletas, en todo el deck
  var texto=document.querySelector('#deck,#deckStage').textContent;
  OBSOLETAS.forEach(function(re){
    var m=texto.match(re); if(m) fallas.push('texto obsoleto: «'+m[0].trim()+'»');
  });

  // 4 · imágenes
  function imagenes(){
    [].forEach.call(document.querySelectorAll('#deck img,#deckStage img'),function(img){
      if(!img.complete||!img.naturalWidth) fallas.push('no carga la imagen '+img.getAttribute('src'));
    });
    var out=document.createElement('pre'); out.id='chequeo';
    out.textContent=fallas.length?'CHEQUEO FALLA\n'+fallas.join('\n'):'CHEQUEO OK · '+principales.length+' láminas principales, '+suma+' s';
    document.body.appendChild(out);
    console.log(out.textContent);
  }
  if(document.readyState==='complete') imagenes(); else addEventListener('load',imagenes);
})();
