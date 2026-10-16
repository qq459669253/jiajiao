/* SPDX-License-Identifier: GPL-3.0-or-later */
(() => {
  'use strict';
  const G=Geometry, $=id=>document.getElementById(id);
  const state={q:4,value:38,variant:'square',stage:3,playing:false,aux:true,traces:false,numbers:true,direction:1};
  const C={ink:'#61766b',red:'#bc4b47',blue:'#326db2',green:'#2e7963',gold:'#cb923f',faint:'#b8c6bb'};
  let current=null,projection=null,lastTime=null,dragId=null;
  const fmt=(x,n=3)=>Math.abs(x)<1e-9?'0':Number(x.toFixed(n)).toString();
  const settings=()=>G.settings(state.q,state.variant);
  const visibleValue=(v)=>state.q===4?fmt(v,1)+'°':(state.q===1||state.q===3)?fmt(100*v,1)+'%':fmt(v,2);
  const stageCopy={
    1:[
      '把△ABM绕B逆时针转60°，A到E，M到N，所以AM=EN。拖动M，看看这对对应边怎样一起变化。',
      'BM=BN，且∠MBN=60°，所以△BMN是等边三角形，BM=MN。M移动时，N必须同步跟随。',
      'AM+BM+CM=EN+NM+MC≥EC。点“到最短路径的位置”，观察E、N、M、C怎样排成一条直线。'
    ],
    2:[
      '补固定的等边△ABQ。Q不动，E在AQ上，F在BQ上；EP与FQ等长且平行。',
      'EM=FM，EP=FQ，∠PEM=∠QFM，故△PEM≌△QFM（SAS）。再看对应角，可知Q、M、P共线且QM=MP。',
      '当P从C走到D时，M从QC中点K走到QD中点L。KL∥CD，KL=CD/2=(20−2−2)/2=8。'
    ],
    3:[
      '复制DF的长度得到BG，再连AG。基本位置把G放在B外侧；延长线位置把G放在B朝C的方向。',
      'AB=AD，BG=DF，夹角∠ABG=∠ADF，所以△ABG≌△ADF（SAS），AG=AF，∠BAG=∠DAF。',
      '半角条件给∠GAE=∠EAF，AE公共，AG=AF，因此△GAE≌△FAE（SAS），GE=EF。最后按B、G、E的顺序决定加法还是减法。'
    ],
    4:[
      '把AB和AD同时绕A逆时针转90°，分别与AC、AE重合。所以BD对应CE，始终等长且互相垂直。',
      '只看蓝色△DCE：P是DC中点，M是DE中点。所以PM∥CE，PM=CE/2。小线段PM属于这个大三角形。',
      '改看蓝色△DCB：P是DC中点，N是CB中点。所以PN∥DB，PN=DB/2。PN属于另一个大三角形。',
      'BD=CE且BD⊥CE，所以PM=PN、PM⊥PN。面积=(1/2)×(BD/2)×(BD/2)=BD²/8；当BD=14时达到49/2。'
    ]
  };
  const givens={1:'固定条件：正方形边长2；△ABE为向外的等边三角形；BM逆时针旋转60°得到BN。',2:'固定条件：AB=20，AC=BD=2；△APE和△BPF都是等边三角形；M为EF中点。',3:'固定条件：AB=AD，∠B+∠D=180°；∠EAF是∠BAD的一半。',4:'固定条件：AB=AC=10，AD=AE=4；∠BAC=∠DAE=90°；M、P、N始终分别为DE、DC、BC中点。'};

  function controls() {
    const c=settings();
    document.querySelectorAll('[data-q]').forEach(b=>b.setAttribute('aria-selected',String(+b.dataset.q===state.q)));
    $('figure-title').textContent='第'+state.q+'题 · '+c.title;
    $('drag-hint').textContent='直接拖动金色的'+c.point+'点，也可调节滑块';
    $('position-label').textContent=c.label;
    Object.assign($('position'),{min:c.min,max:c.max,step:c.step,value:state.value});
    $('position-value').textContent=visibleValue(state.value);
    $('min-label').textContent=visibleValue(c.min);$('max-label').textContent=visibleValue(c.max);
    $('variant').classList.toggle('hidden',state.q!==3);$('variant-label').classList.toggle('hidden',state.q!==3);
    $('special').classList.toggle('hidden',![1,4].includes(state.q));
    $('special').textContent=state.q===1?'到最短路径的位置':'到最大面积的位置';
    $('play').textContent=state.playing?'暂停播放':'自动播放';$('play').setAttribute('aria-pressed',String(state.playing));
    $('step-tabs').innerHTML=c.stages.map((s,i)=>'<button type="button" data-stage="'+i+'" aria-pressed="'+(i===state.stage)+'">'+s+'</button>').join('');
    $('step-copy').textContent=stageCopy[state.q][state.stage];$('given').textContent=givens[state.q];
  }

  function draw(m) {
    const mobile=matchMedia('(max-width:720px)').matches,vw=mobile?700:920,vh=mobile?680:610;
    $('scene').setAttribute('viewBox',`0 0 ${vw} ${vh}`);
    const p=m.p,[lo,hi]=m.fixed,availW=mobile?600:790,availH=mobile?510:445;
    const scale=Math.min(availW/(hi[0]-lo[0]),availH/(hi[1]-lo[1]));
    const ox=(vw-scale*(hi[0]-lo[0]))/2,oy=(mobile?40:72)+(availH-scale*(hi[1]-lo[1]))/2;
    const map=a=>[ox+(a[0]-lo[0])*scale,oy+(hi[1]-a[1])*scale];
    const unmap=a=>[lo[0]+(a[0]-ox)/scale,hi[1]-(a[1]-oy)/scale];projection={map,unmap,scale};
    const fragments=[`<rect width="${vw}" height="${vh}" fill="#fffefa"/>`];
    const point=(k)=>map(p[k]);
    function line(a,b,color=C.ink,width=1.6,dash=false) {
      const u=typeof a==='string'?point(a):map(a),v=typeof b==='string'?point(b):map(b);
      fragments.push(`<line x1="${u[0]}" y1="${u[1]}" x2="${v[0]}" y2="${v[1]}" stroke="${color}" stroke-width="${width}" ${dash?'stroke-dasharray="7 6"':''} stroke-linecap="round"/>`);
    }
    function poly(keys,color) {
      fragments.push('<polygon points="'+keys.map(k=>point(k).join(',')).join(' ')+'" fill="'+color+'" fill-opacity=".09" stroke="'+color+'" stroke-width="2.4" stroke-linejoin="round"/>');
    }
    function tick(a,b,n=1,color=C.ink) {
      const u=point(a),v=point(b),vec=G.sub(v,u),l=G.norm(vec);if(l<1e-5)return;
      const unit=G.mul(vec,1/l),normal=[-unit[1],unit[0]],center=G.mid(u,v);
      for(let i=0;i<n;i++) {
        const k=G.add(center,G.mul(unit,(i-(n-1)/2)*5)),t=G.add(k,G.mul(normal,5)),s=G.add(k,G.mul(normal,-5));
        fragments.push(`<path d="M${t} L${s}" fill="none" stroke="${color}" stroke-width="1.8"/>`);
      }
    }
    function right(v,a,b,color=C.red) {
      const x=point(v),u=G.sub(point(a),x),w=G.sub(point(b),x);if(G.norm(u)<1e-6||G.norm(w)<1e-6)return;
      const uu=G.mul(u,12/G.norm(u)),ww=G.mul(w,12/G.norm(w));
      fragments.push(`<path d="M${G.add(x,uu)} L${G.add(G.add(x,uu),ww)} L${G.add(x,ww)}" fill="none" stroke="${color}" stroke-width="1.8"/>`);
    }
    if(state.traces)m.traces.forEach(t=>{
      if(t.type==='segment')line(t.a,t.b,'#cfaa76',3,true);
      else {const center=map(t.center);fragments.push(`<circle cx="${center[0]}" cy="${center[1]}" r="${t.r*scale}" fill="none" stroke="#b5c6bb" stroke-dasharray="4 6" stroke-width="1.4"/>`);}
    });
    m.base.forEach(e=>line(e[0],e[1]));
    if(state.aux) {
      m.aux.forEach(e=>line(e[0],e[1],C.blue,1.4,true));
      if(state.q===1) {
        if(state.stage===0){poly(['A','B','M'],C.red);poly(['E','B','N'],C.blue);tick('A','B');tick('E','B');tick('B','M',2);tick('B','N',2);}
        if(state.stage===1){poly(['B','M','N'],C.red);[['B','M'],['B','N'],['M','N']].forEach(e=>tick(...e,1,C.red));}
        if(state.stage===2){['EN','NM','MC'].forEach(e=>line(e[0],e[1],C.red,3));line('E','C',C.blue,1.7,true);}
      } else if(state.q===2) {
        if(state.stage===0){line('Q','A',C.blue,2,true);line('Q','B',C.blue,2,true);line('E','P',C.red,3);line('F','Q',C.red,3);tick('E','P');tick('F','Q');}
        if(state.stage===1){poly(['P','E','M'],C.red);poly(['Q','F','M'],C.blue);tick('E','M',2);tick('F','M',2);line('Q','P',C.green,2,true);}
        if(state.stage===2){poly(['Q','C','D'],C.blue);line('K','L',C.red,3);tick('Q','K');tick('K','C');tick('Q','L',2);tick('L','D',2);line('Q','P',C.green,1.8,true);}
      } else if(state.q===3) {
        if(state.stage===0){line('B','G',C.red,3);line('D','F',C.red,3);tick('B','G',2);tick('D','F',2);}
        if(state.stage===1){poly(['A','B','G'],C.red);poly(['A','D','F'],C.blue);tick('A','B');tick('A','D');tick('B','G',2);tick('D','F',2);}
        if(state.stage===2){poly(['G','A','E'],C.red);poly(['F','A','E'],C.blue);line('G','E',C.green,3);line('E','F',C.green,3);tick('A','G');tick('A','F');}
      } else {
        if(state.stage===0){poly(['B','A','D'],C.red);poly(['C','A','E'],C.blue);tick('A','B');tick('A','C');tick('A','D',2);tick('A','E',2);}
        if(state.stage===1){poly(['D','C','E'],C.blue);line('P','M',C.red,3);tick('D','P');tick('P','C');tick('D','M',2);tick('M','E',2);}
        if(state.stage===2){poly(['D','C','B'],C.blue);line('P','N',C.red,3);tick('D','P');tick('P','C');tick('B','N',2);tick('N','C',2);}
        if(state.stage===3){poly(['M','P','N'],C.red);right('P','M','N');tick('P','M',1,C.red);tick('P','N',1,C.red);}
      }
    }
    if(state.q===4)right('A','B','C',C.ink);
    let names=Object.keys(p);
    if(state.q===2&&!state.aux)names=names.filter(k=>!['Q','K','L'].includes(k));
    if(state.q===3&&!state.aux)names=names.filter(k=>k!=='G');
    const groups=[];
    names.forEach(k=>{const old=groups.find(g=>G.dist(p[k],p[g[0]])<1e-7);if(old)old.push(k);else groups.push([k]);});
    const used=[],occupied=names.map(k=>{const pos=point(k);return[pos[0]-7,pos[1]-7,14,14];});
    const intersect=(a,b)=>!(a[0]+a[2]<b[0]||b[0]+b[2]<a[0]||a[1]+a[3]<b[1]||b[1]+b[3]<a[1]);
    groups.forEach(group=>{
      const k=group[0],pos=point(k),moving=group.includes(settings().point),label=group.join('='),w=label.length*(mobile?15:12)+8;
      const candidates=[[13,-16],[13,22],[-w-7,-14],[-w-7,22],[-w/2,-23],[-w/2,32],[24,0],[-w-18,0]];
      let best=null,bestScore=Infinity;
      candidates.forEach(([dx,dy],idx)=>{
        const r=[pos[0]+dx-3,pos[1]+dy-19,w+4,25];
        const score=used.filter(x=>intersect(x,r)).length*100+occupied.filter(x=>intersect(x,r)).length*25+(r[0]<15||r[0]+r[2]>vw-15||r[1]<25||r[1]+r[3]>vh-85?500:0)+idx;
        if(score<bestScore){bestScore=score;best={r,x:pos[0]+dx,y:pos[1]+dy};}
      });used.push(best.r);
      if(moving)fragments.push(`<circle data-drag="true" cx="${pos[0]}" cy="${pos[1]}" r="${mobile?26:17}" fill="${C.gold}" fill-opacity=".17" style="cursor:grab"/>`);
      fragments.push(`<circle data-point="${group.join(',')}" ${moving?'data-drag="true" tabindex="0" role="button" aria-label="拖动'+settings().point+'点"':''} cx="${pos[0]}" cy="${pos[1]}" r="${moving?6.5:4}" fill="${moving?C.gold:C.ink}" stroke="#fffefa" stroke-width="1.6" style="${moving?'cursor:grab':''}"/>`);
      fragments.push(`<text x="${best.x}" y="${best.y}" font-size="${mobile?25:21}" font-family="system-ui,sans-serif" fill="#273b32" stroke="#fffefa" stroke-width="5" paint-order="stroke" stroke-linejoin="round" pointer-events="none">${label}</text>`);
    });
    let caption;
    if(state.q===4)caption='旋转 '+fmt(state.value,1)+'°   ·   PM = '+fmt(m.metrics[0][1])+'   PN = '+fmt(m.metrics[1][1])+'   面积 = '+fmt(m.metrics[5][1]);
    else if(state.q===1)caption='AM + BM + CM = '+fmt(m.metrics[3][1])+'   ·   CE = '+fmt(m.metrics[4][1]);
    else if(state.q===2)caption='AP = '+fmt(state.value,2)+'   ·   QM = MP = '+fmt(m.metrics[1][1])+'   ·   KL = 8';
    else caption=state.variant==='outside'?'延长线位置：BE = DF + EF':'基本位置：EF = BE + DF';
    if(!state.numbers)caption='拖动'+settings().point+'点，观察形状、方向和长度的变化';
    if(mobile) {
      const split=caption.split('   ·   '),first=split.shift(),second=split.join(' · ');
      fragments.push(`<rect x="25" y="600" width="650" height="66" rx="10" fill="#edf2e9"/><text x="350" y="626" text-anchor="middle" font-size="20" font-family="system-ui,sans-serif" fill="#315849">${first}</text><text x="350" y="653" text-anchor="middle" font-size="20" font-family="system-ui,sans-serif" fill="#315849">${second}</text>`);
    } else fragments.push(`<rect x="75" y="552" width="770" height="38" rx="10" fill="#edf2e9"/><text x="460" y="577" text-anchor="middle" font-size="17" font-family="system-ui,sans-serif" fill="#315849">${caption}</text>`);
    $('scene').innerHTML=fragments.join('');
    $('scene').setAttribute('aria-label','第'+state.q+'题，'+settings().point+'点可拖动。'+m.prompt);
  }
  function render(updateControls=false) {
    if(updateControls)controls();
    current=G.model(state.q,state.value,state.variant);draw(current);
    $('position').value=state.value;$('position-value').textContent=visibleValue(state.value);
    $('metrics').innerHTML=current.metrics.map(([name,v,unit])=>'<div class="metric"><dt>'+name+'</dt><dd>'+(state.numbers?fmt(v)+(unit||''):'—')+'</dd></div>').join('');
    $('facts').innerHTML=state.numbers?current.facts.map(([name,error])=>'<div class="fact">'+(Math.abs(error)<1e-6?'✓ ':'')+name+'</div>').join(''):'数值已隐藏，先让学生观察。';
    $('observe').textContent=current.prompt;
  }
  function pause() {state.playing=false;lastTime=null;$('play').textContent='自动播放';$('play').setAttribute('aria-pressed','false');}
  function setValue(v) {state.value=G.clamp(v,settings().min,settings().max);render();}
  function selectQuestion(q) {pause();state.q=q;state.value=settings().initial;state.stage=settings().defaultStage;state.direction=1;render(true);}
  document.querySelectorAll('[data-q]').forEach(b=>b.addEventListener('click',()=>selectQuestion(+b.dataset.q)));
  $('variant').addEventListener('change',()=>{pause();state.variant=$('variant').value;state.value=settings().initial;render(true);});
  $('position').addEventListener('input',()=>{pause();setValue(+$('position').value);});
  $('play').addEventListener('click',()=>{state.playing=!state.playing;lastTime=null;$('play').textContent=state.playing?'暂停播放':'自动播放';$('play').setAttribute('aria-pressed',String(state.playing));});
  $('reset').addEventListener('click',()=>{pause();state.value=settings().initial;state.stage=settings().defaultStage;state.direction=1;render(true);});
  $('special').addEventListener('click',()=>{pause();state.stage=settings().stages.length-1;state.value=state.q===4?180:(1-1/Math.sqrt(3))/2;render(true);});
  ['aux','traces','numbers'].forEach(k=>$(k).addEventListener('change',()=>{state[k]=$(k).checked;render();}));
  $('step-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-stage]');if(b){state.stage=+b.dataset.stage;render(true);}});
  $('scene').addEventListener('pointerdown',e=>{
    const circle=e.target.closest('[data-drag]');if(!circle)return;
    e.preventDefault();pause();dragId=e.pointerId;$('scene').setPointerCapture(e.pointerId);
  });
  $('scene').addEventListener('pointermove',e=>{
    if(e.pointerId!==dragId||!projection)return;
    const screen=new DOMPoint(e.clientX,e.clientY).matrixTransform($('scene').getScreenCTM().inverse());
    const world=projection.unmap([screen.x,screen.y]),drag=current.drag;
    if(drag.kind==='circle') {
      const v=G.sub(world,drag.center);if(G.norm(v)<1e-6)return;
      const angle=Math.atan2(v[1],v[0])*180/Math.PI;
      setValue(((angle-225)%360+360)%360);
    } else {
      const v=G.sub(drag.b,drag.a),t=G.dot(G.sub(world,drag.a),v)/G.dot(v,v);
      setValue(state.q===2?t*20:t);
    }
  });
  const endDrag=e=>{if(e.pointerId===dragId){dragId=null;if($('scene').hasPointerCapture(e.pointerId))$('scene').releasePointerCapture(e.pointerId);}};
  $('scene').addEventListener('pointerup',endDrag);$('scene').addEventListener('pointercancel',endDrag);$('scene').addEventListener('lostpointercapture',()=>{dragId=null;});
  $('scene').addEventListener('keydown',e=>{if(!e.target.closest('[data-drag]'))return;if(['ArrowLeft','ArrowDown','ArrowRight','ArrowUp'].includes(e.key)){e.preventDefault();pause();setValue(state.value+(['ArrowLeft','ArrowDown'].includes(e.key)?-1:1)*(state.q===4?1:settings().step*5));$('scene').querySelector('[data-point][data-drag]').focus({preventScroll:true});}});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
  window.addEventListener('resize',()=>render());
  $('save').addEventListener('click',()=>{
    const svg=$('scene').cloneNode(true);svg.setAttribute('xmlns','http://www.w3.org/2000/svg');
    svg.removeAttribute('style');svg.setAttribute('width',svg.viewBox.baseVal.width);svg.setAttribute('height',svg.viewBox.baseVal.height);
    const blob=new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download='第'+state.q+'题_当前图.svg';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  function animate(time) {
    if(state.playing) {
      if(lastTime!==null) {
        const c=settings(),dt=Math.min((time-lastTime)/1000,.1),delta=(c.max-c.min)*dt/c.period;
        let next=state.value+state.direction*delta;
        if(state.q===4)next=((next%360)+360)%360;
        else if(next>c.max){next=c.max-(next-c.max);state.direction=-1;}else if(next<c.min){next=c.min+(c.min-next);state.direction=1;}
        setValue(next);
      }
      lastTime=time;
    } else lastTime=null;
    requestAnimationFrame(animate);
  }
  window.mathMotion={inspect:()=>({state:{...state},model:current}),setValue,selectQuestion};
  render(true);requestAnimationFrame(animate);
})();
