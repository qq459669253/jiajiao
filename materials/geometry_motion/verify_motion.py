"""Browser and geometry regression checks; needs playwright and Chromium.

Run: python verify_motion.py
The production HTML has no dependencies; these are development checks only.
"""
from pathlib import Path
import math
import shutil
import tempfile
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent


def run():
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1365,'height':1000},offline=True,accept_downloads=True,has_touch=True)
        page=context.new_page();errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda req:requests.append(req.url))
        page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        assert page.locator('#runtime-notice').is_hidden()
        assert page.locator('#static-preview').is_hidden()
        assert page.locator('#position').is_enabled()
        cases=page.evaluate('''() => {
          const G=Geometry,close=(a,b)=>{if(Math.abs(a-b)>1e-7)throw Error(a+' differs from '+b)},len=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
          const angle=(a,b,c)=>{const u=[a[0]-b[0],a[1]-b[1]],v=[c[0]-b[0],c[1]-b[1]];const ratio=(u[0]*v[0]+u[1]*v[1])/(Math.hypot(...u)*Math.hypot(...v));return Math.acos(Math.max(-1,Math.min(1,ratio)))};
          let cases=0;
          for(let n=0;n<=200;n++) {
            const t=n/200,p=G.model(1,t).p;
            close(len(p.A,p.M),len(p.E,p.N));close(len(p.B,p.M),len(p.M,p.N));
            if(len(p.A,p.M)+len(p.B,p.M)+len(p.C,p.M)<Math.sqrt(6)+Math.sqrt(2)-1e-7)throw Error('Q1 lower bound');
            const m=G.model(2,2+16*t).p;
            close(len(m.A,m.P),len(m.A,m.E));close(len(m.A,m.P),len(m.P,m.E));
            close(len(m.B,m.P),len(m.B,m.F));close(len(m.B,m.P),len(m.P,m.F));
            close(len(m.Q,m.M),len(m.P,m.M));close(m.M[1],5*Math.sqrt(3));close(len(m.K,m.L),8);
            for(const variant of ['square','general','outside']) {
              const c=G.settings(3,variant),a=G.model(3,c.min+t*(c.max-c.min),variant).p;
              close(len(a.A,a.B),len(a.A,a.D));
              close(angle(a.E,a.A,a.F)*2,angle(a.B,a.A,a.D));
              close(len(a.B,a.G),len(a.D,a.F));close(len(a.A,a.G),len(a.A,a.F));close(len(a.G,a.E),len(a.E,a.F));
              close(len(a.E,a.F),variant==='outside'?len(a.B,a.E)-len(a.D,a.F):len(a.B,a.E)+len(a.D,a.F));
              const cd=[a.D[0]-a.C[0],a.D[1]-a.C[1]],cf=[a.F[0]-a.C[0],a.F[1]-a.C[1]];
              const along=(cd[0]*cf[0]+cd[1]*cf[1])/(cd[0]**2+cd[1]**2);
              if(variant==='outside'&&along<=1)throw Error('F must be beyond D');
              if(variant!=='outside'&&(along<0||along>1))throw Error('F must stay on CD');
              cases++;
            }
            const r=G.model(4,360*t).p;
            close(len(r.A,r.B),10);close(len(r.A,r.C),10);close(len(r.A,r.D),4);close(len(r.A,r.E),4);close(angle(r.D,r.A,r.E),Math.PI/2);
            for(const [m,a,b] of [['M','D','E'],['P','D','C'],['N','B','C']]){close(r[m][0],(r[a][0]+r[b][0])/2);close(r[m][1],(r[a][1]+r[b][1])/2)}
            close(len(r.P,r.M),len(r.P,r.N));close(angle(r.M,r.P,r.N),Math.PI/2);
            const area=len(r.P,r.M)*len(r.P,r.N)/2;if(area>24.5+1e-7)throw Error('Q4 area bound');
            cases+=3;
          }
          const p=G.model(4,180).p;close(len(p.B,p.D),14);close(len(p.P,p.M),7);close(len(p.P,p.N),7);
          return cases;
        }''')

        def inspect():return page.evaluate('mathMotion.inspect()')
        def select(q):page.locator(f'[data-q="{q}"]').click()
        def screen_point(name,value=None):
            return page.evaluate('''([name,value]) => {
              const {model:m,state:s}=mathMotion.inspect(),svg=document.getElementById('scene');
              const circle=k=>Array.from(svg.querySelectorAll('[data-point]')).find(e=>e.dataset.point.split(',').includes(k));
              const xy=k=>[+circle(k).getAttribute('cx'),+circle(k).getAttribute('cy')];
              let at=xy(name);
              if(value!==null){const target=Geometry.model(s.q,value,s.variant).p[name],a=xy('A'),b=xy('B');
                const scale=Math.hypot(b[0]-a[0],b[1]-a[1])/Geometry.dist(m.p.B,m.p.A);
                at=[a[0]+(target[0]-m.p.A[0])*scale,a[1]-(target[1]-m.p.A[1])*scale];}
              const out=new DOMPoint(...at).matrixTransform(svg.getScreenCTM());return [out.x,out.y];
            }''',[name,value])

        # Test actual mouse pointer dragging, rather than calling the math setter.
        for q,target in [(1,.25),(2,16.5),(3,.68),(4,154)]:
            select(q);name=inspect()['model']['drag'];point={1:'M',2:'P',3:'E',4:'D'}[q]
            start=screen_point(point);end=screen_point(point,target)
            page.mouse.move(*start);page.mouse.down();page.mouse.move(*end,steps=10);page.mouse.up()
            assert abs(inspect()['state']['value']-target)<1e-5,(q,inspect()['state']['value'])
        page.locator('#special').click();s=inspect();assert s['state']['value']==180
        assert abs(s['model']['metrics'][-1][1]-24.5)<1e-9
        before=s['state']['value'];page.locator('#play').click();page.wait_for_timeout(350)
        assert inspect()['state']['value']!=before
        page.locator('#play').click();paused=inspect()['state']['value'];page.wait_for_timeout(100)
        assert inspect()['state']['value']==paused
        for stage in range(4):page.locator(f'[data-stage="{stage}"]').click();assert inspect()['state']['stage']==stage
        page.locator('#aux').uncheck();assert page.locator('#scene polygon').count()==0
        page.locator('#aux').check();page.locator('#traces').check()
        assert page.locator('#scene circle[stroke-dasharray]').count()==3
        page.locator('#numbers').uncheck();assert '—' in page.locator('#metrics').inner_text();page.locator('#numbers').check()
        select(3);page.locator('#variant').select_option('outside');assert inspect()['state']['variant']=='outside'
        page.locator('#position').evaluate("e=>{e.value=4.5;e.dispatchEvent(new Event('input',{bubbles:true}))}")
        assert inspect()['state']['value']==4.5
        # Mobile layout and trusted touch gestures.
        page.set_viewport_size({'width':390,'height':844});select(4)
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        start=screen_point('D');end=screen_point('D',92)
        session=context.new_cdp_session(page)
        session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':start[0],'y':start[1]}]})
        session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':end[0],'y':end[1]}]})
        session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        assert abs(inspect()['state']['value']-92)<.01
        with page.expect_download() as dl:page.locator('#save').click()
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'export.svg';dl.value.save_as(path);text=path.read_text();assert '<svg' in text and 'viewBox="0 0 700 680"' in text
        # Reproduce the key limitation of file preview: HTML without scripts.
        preview_context=browser.new_context(java_script_enabled=False,offline=True,viewport={'width':390,'height':844})
        preview=preview_context.new_page()
        preview.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        assert preview.locator('#runtime-notice').is_visible()
        assert preview.locator('#static-preview img').is_visible()
        assert preview.locator('#position').is_disabled()
        assert preview.locator('#scene').is_hidden()
        preview_context.close()
        assert not errors,errors
        assert not requests,requests
        browser.close()
        print(f'PASS: {cases} geometry cases; all 4 drag interactions; playback/pause; stages; toggles; SVG export; offline execution; mobile touch and layout; script-disabled preview fallback.')


if __name__=='__main__':run()
