from pathlib import Path
import hashlib, sys

src=Path(sys.argv[1] if len(sys.argv)>1 else "Problem-OCEAN-WHALE-V3-G0A-CONTINUATION-BASELINE.html")
out=Path(sys.argv[2] if len(sys.argv)>2 else "Problem-OCEAN-WHALE-V3-DUAL-SCENE-ENCOUNTER.html")
s=src.read_text(encoding="utf-8")

def sub(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f"missing marker: {label}")
    s=s.replace(old,new,1)

sub(
'.cinema .narrative,.cinema .console,.cinema .edition,.cinema .depth,.cinema .footnote,.cinema .brand,.cinema #sound{opacity:0;pointer-events:none}.cinema #cinema{opacity:.35}.cinema #cinema:hover,.cinema #cinema:focus-visible{opacity:1}.cinema .vignette{opacity:.3}',
'.cinema .narrative,.cinema .console,.cinema .edition,.cinema .depth,.cinema .footnote,.cinema .brand,.cinema #sound{opacity:0;pointer-events:none}.cinema #cinema,.cinema #sceneMode{opacity:.35}.cinema #cinema:hover,.cinema #cinema:focus-visible,.cinema #sceneMode:hover,.cinema #sceneMode:focus-visible{opacity:1}.cinema .vignette{opacity:.3}\n#sceneMode{position:relative;overflow:hidden;transition:background .32s ease,border-color .32s ease,transform .32s ease}#sceneMode svg{transition:transform .45s cubic-bezier(.2,.8,.2,1)}#sceneMode[aria-pressed=true]{background:#d7e5ed18;border-color:#d7e5ed73}#sceneMode[aria-pressed=true] svg{transform:rotate(180deg)}\n.encounter .vignette{background:linear-gradient(#010508d9,transparent 17%,transparent 50%,#010407f2 98%),radial-gradient(ellipse at 50% 38%,transparent 28%,#0104079c 78%,#010407de 100%)}\n.mode-toast{position:absolute;left:50%;top:18%;z-index:7;transform:translate(-50%,-8px);padding:9px 14px;border:1px solid #dceaf33b;border-radius:999px;background:#061119d9;color:#dfeaf0;font-size:8px;letter-spacing:2.8px;direction:ltr;opacity:0;pointer-events:none;transition:opacity .28s ease,transform .28s ease;box-shadow:0 14px 45px #0009;backdrop-filter:blur(6px)}.mode-toast.show{opacity:1;transform:translate(-50%,0)}',
"css")

sub('<div class="top-actions">\n<button class="icon-button" id="cinema"',
'<div class="top-actions">\n<button class="icon-button" id="sceneMode" aria-label="فتح مشهد اللقاء" aria-pressed="false"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 6.5c3.2-3.1 8.2-3.1 11.4 0L17 9M17 13.5c-3.2 3.1-8.2 3.1-11.4 0L3 11m7-7v12"/></svg><span class="label">لقاء</span></button>\n<button class="icon-button" id="cinema"',
"button")
sub('<div class="status" id="status" role="status" aria-live="polite"></div>',
'<div class="status" id="status" role="status" aria-live="polite"></div><div class="mode-toast" id="modeToast" aria-live="polite">THE ENCOUNTER</div>',
"toast")

sub('uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;',
'uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform float uEncounter; uniform float uEncounterCue; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;',
"mesh uniforms")
sub(' vec3 color=albedo*(vec3(.34,.46,.52)+diffuse*surfaceLight*vec3(.76,.83,.85)+diffuse2*vec3(.20,.25,.27));\n color+=pbr*vec3(.95,1.02,1.08)*surfaceLight+spec*vec3(.15,.22,.25)+rim*surfaceLight*vec3(.075,.105,.12);',
' vec3 color=albedo*(vec3(.34,.46,.52)+diffuse*surfaceLight*vec3(.76,.83,.85)+diffuse2*vec3(.20,.25,.27));\n color+=pbr*vec3(.95,1.02,1.08)*surfaceLight+spec*vec3(.15,.22,.25)+rim*surfaceLight*vec3(.075,.105,.12);\n float headMask=1.-smoothstep(-3.4,.7,vLocal.x);\n vec3 encounterL=normalize(vec3(-.58,.79,.18));\n float encounterKey=max(0.,dot(N,encounterL));\n float encounterRim=pow(1.-max(0.,dot(N,V)),2.35);\n float encounterShape=uEncounter*uEncounterCue*(.34*encounterKey*(.38+.62*headMask)+.095*encounterRim);\n color+=encounterShape*vec3(.66,.75,.79);\n if(vMaterial>2.5&&vMaterial<3.5)color+=uEncounter*uEncounterCue*pow(max(0.,dot(reflect(-encounterL,N),V)),18.)*vec3(.16,.21,.23);',
"mesh light")
sub(' float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.018+uDeep*.009));',
' float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.018+uDeep*.009+uEncounter*(.003+uDeep*.0035)));',
"fog")
sub('uniform vec3 uForward;uniform vec3 uRight;uniform vec3 uUp;uniform vec3 uEye;uniform vec3 uFog;uniform float uAspect;uniform float uTan;uniform float uTime;uniform float uDeep;',
'uniform vec3 uForward;uniform vec3 uRight;uniform vec3 uUp;uniform vec3 uEye;uniform vec3 uFog;uniform float uAspect;uniform float uTan;uniform float uTime;uniform float uDeep;uniform float uEncounter;uniform float uEncounterCue;',
"back uniforms")
sub(' vec2 apertureQ=q-vec2(.05,.04);\n float apertureRing=exp(-abs(length(apertureQ*vec2(.92,.70))-.43)*54.);\n float apertureCore=exp(-length(apertureQ*vec2(.92,.70))*7.2);\n vec3 apertureLight=vec3(.19,.37,.45)*apertureRing*(.08+uDeep*1.18)+vec3(.035,.10,.13)*apertureCore*uDeep;\n col+=apertureLight;\n float edge=1.-smoothstep(.18,1.6,length(q*vec2(.75,.63)));col*=.76+.24*edge;',
' vec2 apertureQ=q-mix(vec2(.05,.04),vec2(-.02,.30),uEncounter);\n float apertureRing=exp(-abs(length(apertureQ*vec2(.92,.70))-.43)*54.);\n float apertureCore=exp(-length(apertureQ*vec2(.92,.70))*7.2);\n vec3 apertureLight=vec3(.19,.37,.45)*apertureRing*(.08+uDeep*1.18)+vec3(.035,.10,.13)*apertureCore*uDeep;\n apertureLight*=1.+uEncounter*(.80+uEncounterCue*.85);\n col+=apertureLight;\n float canyonSide=smoothstep(.38,.98,abs(q.x))*(.42+.58*smoothstep(-.35,.65,q.y));\n col*=1.-uEncounter*canyonSide*.34;\n float edge=1.-smoothstep(.18,1.6,length(q*vec2(.75,.63)));col*=.76+.24*edge;',
"background")

encounter='''\n const encounterKeys=[\n  [0,-18,2.4,.2,-4.7,0,.08],[3.2,-14.6,1.5,1.4,-4.4,-.05,.12],[6.4,-10.1,1.3,6.2,-3.25,-.14,.20],\n  [9.3,-7.2,.3,10.1,-2.4,-.24,.28],[12.4,-2.1,-2.2,9.4,-.7,-.28,.39],[15.6,3.7,-.1,11.8,1.0,-.18,.50],\n  [19.2,9.5,2.1,16.7,2.4,.05,.66],[22,13.8,4,21.5,3.3,.35,.76],[24,16.5,6.4,27,4.2,.75,.84]\n ];\n function encounterShot(t,aspect,orbitX=0,orbitY=0,zoom=1){\n  t=Math.max(0,Math.min(24,t));let i=0;while(i<encounterKeys.length-2&&t>encounterKeys[i+1][0])i++;\n  const b=encounterKeys[i],c=encounterKeys[i+1],a=encounterKeys[Math.max(0,i-1)],d=encounterKeys[Math.min(encounterKeys.length-1,i+2)],f=(t-b[0])/(c[0]-b[0]);\n  const vals=[1,2,3,4,5,6].map(k=>.5*(2*b[k]+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f));\n  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;\n  const eye=[dx*fit*zoom,(vals[1]+orbitY*10)*zoom,dz*fit*zoom],target=[vals[3],vals[4],0];\n  const ss=(a,b,x)=>{x=Math.max(0,Math.min(1,(x-a)/(b-a)));return x*x*(3-2*x);};\n  const hero=ss(4.4,8,t)*(1-ss(14.8,20.8,t)),depart=ss(18.2,24,t),whale={x:0,y:Math.sin(t*.34)*.08,z:0,s:1+hero*.075-depart*.035,yaw:-.055+ss(7.2,16.4,t)*.19};\n  return {...camera(eye,target,aspect),deep:Math.max(0,Math.min(1,vals[5])),target,whale};\n }\n'''
sub(' return {camera,shot,model,multiply};',encounter+' return {camera,shot,encounterShot,model,multiply};',"camera")

sub("const state={time:0,shot:0,auto:false,paused:false,reduced:media.matches,speed:1,zoom:1,targetZoom:1,orbitX:0,orbitY:0,targetX:0,targetY:0,quality:'auto',qualityTier:lowDevice?'low':'balanced',post:!lowDevice,hidden:document.hidden,inView:true,lost:false,ready:false,sound:false,frames:0};",
"const state={time:0,shot:0,scene:'journey',auto:false,paused:false,reduced:media.matches,speed:1,zoom:1,targetZoom:1,orbitX:0,orbitY:0,targetX:0,targetY:0,quality:'auto',qualityTier:lowDevice?'low':'balanced',post:!lowDevice,hidden:document.hidden,inView:true,lost:false,ready:false,sound:false,frames:0};","state")
sub("function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uFog',[.018*(1-cam.deep*.3),.062*(1-cam.deep*.4),.089*(1-cam.deep*.3)]);}",
"function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uEncounter',state.scene==='encounter'?1:0);uniform(p,'uEncounterCue',state.scene==='encounter'?Math.max(0,Math.min(1,state.shot<7?state.shot/7:state.shot>19?(24-state.shot)/5:1)):0);uniform(p,'uFog',[.018*(1-cam.deep*.3),.062*(1-cam.deep*.4),.089*(1-cam.deep*.3)]);}",
"common")
sub('const cam=OceanMath.shot(state.shot,width/height,state.orbitX,state.orbitY,state.zoom),r=resources;',
"const cam=(state.scene==='encounter'?OceanMath.encounterShot:OceanMath.shot)(state.shot,width/height,state.orbitX,state.orbitY,state.zoom),r=resources;",
"render camera")
sub("uniform(r.mesh,'uModel',OceanMath.model(14,3,-36,.65,-.24));uniform(r.mesh,'uTime',state.time+3);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);\n  uniform(r.mesh,'uModel',OceanMath.model());uniform(r.mesh,'uTime',state.time);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);",
"if(state.scene==='journey'){uniform(r.mesh,'uModel',OceanMath.model(14,3,-36,.65,-.24));uniform(r.mesh,'uTime',state.time+3);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);}\n  const wm=cam.whale||{x:0,y:0,z:0,s:1,yaw:0};uniform(r.mesh,'uModel',OceanMath.model(wm.x,wm.y,wm.z,wm.s,wm.yaw));uniform(r.mesh,'uTime',state.time);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);",
"whale draw")

labels="const journeyLabels=[['01 / THE ENCOUNTER','في الهدوء… عظمة.','سيب العالم فوق، وتعالى لحظة لجوه.','OPEN WATER'],['02 / IN THE PRESENCE','في حاجات، لازم تقرّب لها.','تفاصيل صغيرة… في كائن أكبر من خيالك.','UP CLOSE'],['03 / INTO THE BLUE','أعمق مما تتخيّل.','كل ما الضوضاء تبعد، التفاصيل بتبان.','THE DEEP'],['04 / RETURN TO LIGHT','ارجع… بمساحة أوسع.','مش لازم تغيّر كل حاجة. ابدأ بنظرة جديدة.','TOWARD LIGHT']];\n const encounterLabels=[['01 / BELOW THE GIANT','فوقك… كتلة تتحرك.','مشهد أقرب وأثقل. خليك ثابت وسيب الحوت يقترب.','FRONTAL APPROACH'],['02 / THE TURN','المسافة بتختفي.','الرأس والكتف يدخلوا الضوء قبل مرور الجسم.','THREE QUARTER'],['03 / UNDER THE MASS','دلوقتي… الحجم له وزن.','مرور قريب تحت الكاميرا مع بقاء الحركة هادئة وثقيلة.','CLOSE PASS'],['04 / INTO THE HAZE','الضوء يسيبه يمشي.','الجسم يبعد تدريجيًا لحد ما الماء ياخده تاني.','DEPARTURE']];\n const sceneDuration=()=>state.scene==='encounter'?24:96;\n const sceneTimes=()=>state.scene==='encounter'?[0,6,12,18]:[0,30,60,82];\n const sceneNames=()=>state.scene==='encounter'?['الظهور','الاقتراب','المرور','العودة']:['اللقاء','عن قرب','العمق','الضوء'];"
sub("const labels=[['01 / THE ENCOUNTER','في الهدوء… عظمة.','سيب العالم فوق، وتعالى لحظة لجوه.','OPEN WATER'],['02 / IN THE PRESENCE','في حاجات، لازم تقرّب لها.','تفاصيل صغيرة… في كائن أكبر من خيالك.','UP CLOSE'],['03 / INTO THE BLUE','أعمق مما تتخيّل.','كل ما الضوضاء تبعد، التفاصيل بتبان.','THE DEEP'],['04 / RETURN TO LIGHT','ارجع… بمساحة أوسع.','مش لازم تغيّر كل حاجة. ابدأ بنظرة جديدة.','TOWARD LIGHT']];",
labels,"labels")

sub("if(state.auto){state.shot=Math.min(96,state.shot+dt);if(state.shot===96){state.auto=false;notice('وصلت للضوء. تقدر تعيد الرحلة أو تستكشف بحرّية.');}}",
"if(state.auto){const limit=sceneDuration();state.shot=Math.min(limit,state.shot+dt);if(state.shot===limit){state.auto=false;notice(state.scene==='encounter'?'انتهى اللقاء. تقدر تعيده أو ترجع للرحلة.':'وصلت للضوء. تقدر تعيد الرحلة أو تستكشف بحرّية.');}}",
"duration")
sub("$('journey').addEventListener('click',()=>{if(state.reduced)return;if(state.auto){manual();return;}state.auto=true;state.paused=false;if(state.shot>=95.9)state.shot=0;state.targetX=state.targetY=0;state.targetZoom=1;notice('رحلة مدتها دقيقة و٣٦ ثانية. تقدر توقفها أو تستكشف في أي وقت.');updateUI();start();});",
"$('journey').addEventListener('click',()=>{if(state.reduced)return;if(state.auto){manual();return;}const limit=sceneDuration();state.auto=true;state.paused=false;if(state.shot>=limit-.1)state.shot=0;state.targetX=state.targetY=0;state.targetZoom=1;notice(state.scene==='encounter'?'مشهد اللقاء مدته ٢٤ ثانية. تقدر توقفه أو تبدّل للرحلة في أي وقت.':'رحلة مدتها دقيقة و٣٦ ثانية. تقدر توقفها أو تستكشف في أي وقت.');updateUI();start();});",
"journey button")

switch="let modeToastTimer=0;\n function showModeToast(text){const el=$('modeToast');el.textContent=text;el.classList.add('show');clearTimeout(modeToastTimer);modeToastTimer=setTimeout(()=>el.classList.remove('show'),1450);}\n function switchScene(){state.scene=state.scene==='journey'?'encounter':'journey';state.auto=false;state.paused=false;state.shot=0;state.targetX=state.targetY=state.orbitX=state.orbitY=0;state.targetZoom=state.zoom=1;lastChapter=-1;main.classList.toggle('encounter',state.scene==='encounter');$('zoom').value=1;showModeToast(state.scene==='encounter'?'THE ENCOUNTER · 24s':'THE OCEAN WITHIN · 96s');notice(state.scene==='encounter'?'مشهد لقاء جديد — اقتراب أمامي، مرور قريب، ثم اختفاء في العمق.':'رجعنا لرحلة المحيط الكاملة.');updateUI();render();start();}\n $('sceneMode').addEventListener('click',switchScene);\n "
sub("async function cinema(){const on=main.classList.toggle('cinema');",switch+"async function cinema(){const on=main.classList.toggle('cinema');","switch")

out.write_text(s,encoding="utf-8")
b=out.read_bytes()
print(out)
print("bytes",len(b))
print("sha256",hashlib.sha256(b).hexdigest())
