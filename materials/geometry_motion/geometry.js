/* SPDX-License-Identifier: GPL-3.0-or-later
   Exact geometric constraints for the selected tutoring problems. */
(function (root) {
  'use strict';
  const add=(a,b)=>[a[0]+b[0],a[1]+b[1]], sub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
  const mul=(a,t)=>[a[0]*t,a[1]*t], mid=(a,b)=>mul(add(a,b),.5);
  const norm=a=>Math.hypot(...a), dist=(a,b)=>norm(sub(a,b));
  const dot=(a,b)=>a[0]*b[0]+a[1]*b[1], cross=(a,b)=>a[0]*b[1]-a[1]*b[0];
  const rot=(a,t)=>[a[0]*Math.cos(t)-a[1]*Math.sin(t),a[0]*Math.sin(t)+a[1]*Math.cos(t)];
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
  function meet(a,b,c,d) {const v=sub(b,a),w=sub(d,c); return add(a,mul(v,cross(sub(c,a),w)/cross(v,w)));}
  const config={
    1:{min:0,max:1,step:.001,initial:.43,period:10,point:'M',label:'M在BD上的位置',unit:'%',title:'旋转与最短路径',stages:['① 把AM搬到EN','② 找到等边三角形','③ 连成折线'],defaultStage:2},
    2:{min:2,max:18,step:.01,initial:8,period:10,point:'P',label:'AP的长度',unit:'',title:'动点与中点轨迹',stages:['① 补固定等边三角形','② 找到QP中点','③ 观察M的轨迹'],defaultStage:2},
    3:{min:.03,max:.97,step:.001,initial:.4,period:12,point:'E',label:'E沿BC的移动位置',unit:'%',title:'半角与加减关系',stages:['① 复制DF','② 第一次全等','③ 第二次全等'],defaultStage:2},
    4:{min:0,max:360,step:.1,initial:38,period:18,point:'D',label:'△ADE逆时针旋转',unit:'°',title:'旋转、中点与面积',stages:['① 旋转的对应关系','② 单独看PM','③ 单独看PN','④ 小三角形与面积'],defaultStage:3}
  };
  function settings(q,variant='square') {
    const c={...config[q]};
    if(q===3&&variant==='outside')Object.assign(c,{min:2,max:5,initial:3.5});
    return c;
  }
  function model(q,value,variant='square') {
    const p={}, base=[], aux=[]; let metrics=[], facts=[], prompt='', traces=[], fixed=[], drag, right=[];
    if(q===1) {
      Object.assign(p,{A:[0,2],B:[0,0],C:[2,0],D:[2,2],E:[-Math.sqrt(3),1]});
      p.M=[2*value,2*value];p.N=rot(p.M,Math.PI/3);
      base.push('AB','BC','CD','DA','AE','EB','BD','AM','MC','BN');aux.push('EN','NM','EC');
      metrics=[['AM',dist(p.A,p.M)],['BM',dist(p.B,p.M)],['CM',dist(p.C,p.M)],['三段距离和',dist(p.A,p.M)+dist(p.B,p.M)+dist(p.C,p.M)],['固定的CE',dist(p.C,p.E)]];
      facts=[['AM = EN',dist(p.A,p.M)-dist(p.E,p.N)],['BM = MN',dist(p.B,p.M)-dist(p.M,p.N)]];
      prompt=value<1e-7?'M与B重合时，三角形BMN退化，三段距离和为4。':'先观察EN、NM、MC这条折线。它们什么时候能排在同一直线上？';
      traces=[{type:'segment',a:p.B,b:rot(p.D,Math.PI/3),label:'N的轨迹'}];
      fixed=[[-2.1,-.35],[2.5,3.2]];drag={kind:'line',a:p.B,b:p.D};
    } else if(q===2) {
      const s=Math.sqrt(3);Object.assign(p,{A:[0,0],B:[20,0],C:[2,0],D:[18,0],P:[value,0],Q:[10,10*s]});
      p.E=[value/2,value*s/2];p.F=[(20+value)/2,(20-value)*s/2];p.M=mid(p.E,p.F);
      p.K=mid(p.Q,p.C);p.L=mid(p.Q,p.D);
      base.push('AB','AE','EP','BF','FP','EF');aux.push('EQ','QF','QP','KL');
      metrics=[['AP',value],['QM',dist(p.Q,p.M)],['MP',dist(p.M,p.P)],['路径KL',dist(p.K,p.L)]];
      facts=[['QM = MP',dist(p.Q,p.M)-dist(p.M,p.P)],['KM + ML = KL',dist(p.K,p.M)+dist(p.M,p.L)-dist(p.K,p.L)]];
      prompt='Q不动，P沿CD移动，M始终是QP的中点。观察M从K走到L，为什么路程只走了一半？';
      traces=[{type:'segment',a:p.K,b:p.L,label:'M的轨迹'}];fixed=[[-2,-2.2],[22,20]];drag={kind:'line',a:p.A,b:p.B};
    } else if(q===3) {
      let half;
      if(variant==='square') {
        Object.assign(p,{A:[0,2],B:[0,0],C:[2,0],D:[2,2]});half=Math.PI/4;
      } else {
        Object.assign(p,{A:[0,0],B:[0,-2],D:[2*Math.cos(.35),2*Math.sin(.35)]});
        const ox=(2+p.D[1])/p.D[0],r=Math.hypot(ox,1);
        p.C=[ox+r*Math.cos(5.25),-1+r*Math.sin(5.25)];half=(Math.PI/2+.35)/2;
      }
      p.E=add(p.B,mul(sub(p.C,p.B),value));
      p.F=meet(p.A,add(p.A,rot(sub(p.E,p.A),half)),p.C,p.D);
      const df=dist(p.D,p.F),bc=sub(p.C,p.B);
      p.G=add(p.B,mul(bc,(variant==='outside'?1:-1)*df/norm(bc)));
      base.push('AB','BC','CD','DA','AE','AF','EF');aux.push('AG','BG');
      if(variant==='outside')base.push('CE','DF');
      const be=dist(p.B,p.E),ef=dist(p.E,p.F);
      metrics=[['BE',be],['DF',df],['EF',ef],['GE',dist(p.G,p.E)]];
      facts=[['AG = AF',dist(p.A,p.G)-dist(p.A,p.F)],['GE = EF',dist(p.G,p.E)-ef],[variant==='outside'?'BE = DF + EF':'EF = BE + DF',variant==='outside'?be-df-ef:ef-be-df]];
      prompt=variant==='outside'?'现在G在B、E之间。长度GE要用BE减去BG，关系变为BE=DF+EF。':'现在G在B外侧。GE由GB和BE拼成，所以EF=BE+DF。';
      const lo=settings(q,variant).min,hi=settings(q,variant).max;
      if(variant==='square')fixed=[[-2.4,-.5],[2.5,2.5]];
      else if(variant==='general')fixed=[[-2.5,-3.1],[3,.95]];
      else fixed=[[-.9,-5.4],[13,2.1]];
      traces=[{type:'segment',a:add(p.B,mul(bc,lo)),b:add(p.B,mul(bc,hi)),label:'E的轨迹'}];drag={kind:'line',a:p.B,b:p.C};
    } else {
      const k=10/Math.sqrt(2),r=4/Math.sqrt(2),theta=value*Math.PI/180;
      Object.assign(p,{A:[0,0],B:[-k,-k],C:[k,-k]});p.D=rot([-r,-r],theta);p.E=rot(p.D,Math.PI/2);
      p.M=mid(p.D,p.E);p.P=mid(p.D,p.C);p.N=mid(p.B,p.C);
      base.push('AB','BC','CA','AD','DE','EA','DC');aux.push('BD','CE','PM','PN','MN');
      const bd=dist(p.B,p.D),ce=dist(p.C,p.E),pm=dist(p.P,p.M),pn=dist(p.P,p.N);
      const u=sub(p.M,p.P),v=sub(p.N,p.P);const ang=Math.acos(clamp(dot(u,v)/(norm(u)*norm(v)),-1,1))*180/Math.PI;
      metrics=[['PM',pm],['PN',pn],['∠MPN',ang,'°'],['BD',bd],['CE',ce],['△PMN面积',Math.abs(cross(u,v))/2]];
      facts=[['PM = PN',pm-pn],['PM ⟂ PN',ang-90],['面积 = BD² / 8',Math.abs(cross(u,v))/2-bd*bd/8]];
      prompt=Math.abs(value-180)<.2?'此时D、A、B依次共线，BD=4+10=14。两条直角边都等于7，面积达到49/2。':'拖动D时，M、P、N的位置一起变化，但小三角形始终等腰且直角。想一想：BD什么时候最长？';
      right=[['P','M','N']];
      traces=[{type:'circle',center:p.A,r:4,label:'D、E的轨迹'},{type:'circle',center:p.A,r:4/Math.sqrt(2),label:'M的轨迹'},{type:'circle',center:mul(p.C,.5),r:2,label:'P的轨迹'}];
      fixed=[[-8.9,-8.9],[8.9,5.3]];drag={kind:'circle',center:p.A};
    }
    return {q,value,variant,p,base,aux,metrics,facts,prompt,traces,fixed,drag,right};
  }
  const API={add,sub,mul,mid,norm,dist,dot,cross,rot,clamp,meet,config,settings,model};
  if(typeof module!=='undefined'&&module.exports)module.exports=API;
  root.Geometry=API;
})(globalThis);
