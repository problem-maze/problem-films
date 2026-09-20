from pathlib import Path
import hashlib,re,sys

def once(s, old, new, label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    s=s.replace("VM-1 — Creature & Color Master","VM-1R + VM-2 — Creature / Water Integration")
    s=s.replace("VM-1 CREATURE / COLOR MASTER","VM-1R + VM-2 VISUAL INTEGRATION")
    s=s.replace("VM1_SHARK_SHADERS_SAFE","VM12_SHARK_SHADERS_SAFE").replace("VM1_SHARK_SHADERS","VM12_SHARK_SHADERS")
    s=s.replace("vm1-webgl-safe","vm12-webgl-safe").replace("vm1-full","vm12-full")

    # Full-screen visual review without forcing fullscreen APIs.
    css=".cinema .narrative,.cinema .console,.cinema .edition,.cinema .depth,.cinema .footnote,.cinema .brand,.cinema #sound{opacity:0;pointer-events:none}"
    if css in s and ".visual-run .narrative" not in s:
        s=s.replace(css,css+".visual-run .narrative,.visual-run .console,.visual-run .edition,.visual-run .depth,.visual-run .footnote,.visual-run .brand,.visual-run #sound{opacity:0;pointer-events:none}",1)

    # Surface normal response: remove repetitive denticle stamp, use two low-amplitude longitudinal bands.
    old="""  // G3: subtle longitudinal dermal response. Keep it smaller than silhouette/detail scale.
  vec3 axis=abs(N.y)<.86?vec3(0.,1.,0.):vec3(1.,0.,0.);vec3 T=normalize(cross(axis,N)),B=normalize(cross(N,T));
  float grain=noise(vec2(vLocal.x*16.+vLocal.y*2.2,vLocal.z*9.5))-.5;
  float d=denticle(vec2(vLocal.x*21.,atan(vLocal.z,vLocal.y)*14.));
  N=normalize(N+T*((d-.34)*.015+grain*.009)+B*((normalTex.y-.5)*.018));"""
    new="""  // VM-1R: directional dermal microstructure. No stamped/graphic denticle grid.
  vec3 axis=abs(N.y)<.86?vec3(0.,1.,0.):vec3(1.,0.,0.);vec3 T=normalize(cross(axis,N)),B=normalize(cross(N,T));
  float around=atan(vLocal.z,vLocal.y);
  float grainA=noise(vec2(vLocal.x*8.8+around*1.7,around*7.6))-.5;
  float grainB=noise(vec2(vLocal.x*19.5-around*.8,around*15.2+vLocal.y*.7))-.5;
  float longFlow=grainA*.62+grainB*.38;
  N=normalize(N+T*(longFlow*.010)+B*(normalTex.y*.010+grainA*.004));"""
    s=once(s,old,new,"micro surface")

    # Refine body material and mouth geometry-driven shading.
    old="""  rough=clamp(.49+(macro-.5)*.10+(mapRough-.5)*.08+scar*.11,.38,.64);
  float mx=smoothstep(-6.45,-5.82,vLocal.x)*(1.-smoothstep(-4.70,-4.18,vLocal.x));
  mouthMask=mx*exp(-pow((angular+.39)*7.2,2.));
  albedo=mix(albedo,vec3(.042,.018,.018),mouthMask*.58);rough=mix(rough,.19,mouthMask*.72);"""
    new="""  float roughMacro=fbm(vec2(vLocal.x*.86+4.2,around*1.45));
  rough=clamp(.47+(macro-.5)*.085+(roughMacro-.5)*.085+(mapRough-.5)*.035+scar*.10,.37,.61);
  float mx=smoothstep(-6.42,-5.78,vLocal.x)*(1.-smoothstep(-4.72,-4.20,vLocal.x));
  float mouthCenter=angular+.365;
  float mouthCavity=mx*exp(-pow(mouthCenter*9.4,2.));
  float lipBand=mx*exp(-pow((abs(mouthCenter)-.105)*24.,2.));
  mouthMask=max(mouthCavity,lipBand*.72);
  albedo=mix(albedo,vec3(.034,.010,.011),mouthCavity*.78);
  albedo=mix(albedo,vec3(.155,.075,.070),lipBand*.26);
  rough=mix(rough,.14,mouthCavity*.86);rough=mix(rough,.24,lipBand*.56);"""
    s=once(s,old,new,"body/mouth")

    # Eyes: deeper socket feel through corneal edge and tiny asymmetric catch, not a flat button.
    old="""  eyeFace=smoothstep(.24,.88,abs(N.z));
  float irisRing=smoothstep(.36,.58,eyeFace)*(1.-smoothstep(.76,.96,eyeFace));
  albedo=vec3(.0007,.0010,.0012)+irisRing*vec3(.006,.0065,.0058);
  rough=.022;"""
    new="""  eyeFace=smoothstep(.20,.90,abs(N.z));
  float irisRing=smoothstep(.30,.54,eyeFace)*(1.-smoothstep(.72,.965,eyeFace));
  float limbal=1.-smoothstep(.72,.98,eyeFace);
  albedo=vec3(.00045,.00065,.00078)+irisRing*vec3(.0048,.0052,.0047);
  albedo*=.82+.18*limbal;
  rough=.018;"""
    s=once(s,old,new,"eye base")

    # Gills: recessed tissue with softer skin-like edges.
    old="""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  albedo=mix(vec3(.070,.072,.069),vec3(.050,.025,.026),.38+.36*gillFade);
  rough=.34;"""
    new="""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  float gillCore=pow(gillFade,.72);
  albedo=mix(vec3(.090,.088,.082),vec3(.040,.022,.023),.28+.48*gillCore);
  rough=mix(.48,.27,gillCore);"""
    s=once(s,old,new,"gills")

    # Teeth less graphic/pure-white.
    s=s.replace("}else{albedo=vec3(.78,.80,.76);rough=.25;}","}else{albedo=vec3(.66,.67,.62);rough=.31;}",1)
    s=s.replace("enamel*.22*vec3(.95,1.,1.)","enamel*.12*vec3(.90,.92,.89)",1)

    # Eye optics: smaller hard catch + soft corneal film.
    old="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),104.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),76.);
  float edgeFilm=pow(1.-ndv,3.6);
  color+=vec3(.78,.84,.87)*cornea*.88+vec3(.34,.38,.39)*sideCatch*.18+edgeFilm*.030*vec3(.38,.43,.44);"""
    new="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),148.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),92.);
  float edgeFilm=pow(1.-ndv,3.2);
  float cornealVeil=pow(max(0.,dot(N,normalize(L+V))),22.)*.18;
  color+=vec3(.82,.86,.87)*cornea*1.08+vec3(.38,.41,.41)*sideCatch*.14+edgeFilm*.038*vec3(.42,.45,.46)+cornealVeil*vec3(.018,.022,.023);"""
    s=once(s,old,new,"eye optics")

    # Mouth wet response follows cavity/lip region but avoids glossy lipstick look.
    s=s.replace("lipSpec*.125*vec3(.74,.76,.75)","lipSpec*.105*vec3(.72,.70,.68)",1)
    s=s.replace("gillFade*slitSpec*.022*vec3(.46,.34,.34)","gillFade*slitSpec*.016*vec3(.38,.31,.31)",1)

    # VM-2: silhouette water wrap mixes the creature into surrounding medium.
    old="""color+=backscatter*vec3(.022,.040,.050);
 color=mix(color,uFog,fog);"""
    new="""color+=backscatter*vec3(.022,.040,.050);
 float waterWrap=pow(1.-ndv,2.1)*(.040+uDeep*.030);color=mix(color,uFog,waterWrap);
 color=mix(color,uFog,fog);"""
    s=once(s,old,new,"water wrap")

    # Add an expandable shell uniform to both hero vertex paths; hero uses 0, water shell >0.
    full_uniform="uniform mat4 uVP; uniform mat4 uModel; uniform float uTime; uniform float uAnimate;"
    s=once(s,full_uniform,full_uniform+" uniform float uShell;","full shell uniform")
    full_world=" vec4 world=uModel*vec4(p,1.);vWorld=world.xyz;"
    s=once(s,full_world," p+=n*uShell;"+full_world,"full shell expansion")

    safe_uniform="uniform mat4 uVP;uniform mat4 uModel;uniform float uTime;uniform float uAnimate;"
    s=once(s,safe_uniform,safe_uniform+"uniform float uShell;","safe shell uniform")
    # There are multiple 'vec4 w=' strings; target safe hero shader's exact tail.
    safe_tail="if(aMaterial>7.5&&aMaterial<8.5)p.x+=sin(uTime*.54+aPart*.31+p.y)*.07;vec4 w=uModel*vec4(p,1.);"
    s=once(s,safe_tail,"if(aMaterial>7.5&&aMaterial<8.5)p.x+=sin(uTime*.54+aPart*.31+p.y)*.07;p+=n*uShell;vec4 w=uModel*vec4(p,1.);","safe shell expansion")

    # Dedicated water-contact shell. Same animated authored geometry, expanded along normals.
    anchor="const OceanMath=(()=>{"
    shell="""const VM12_WATER_SHELL_FS=\`precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;uniform float uDensity;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
void main(){
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);float ndv=abs(dot(N,V));
 float edge=pow(1.-ndv,1.55),body=1.-smoothstep(5.4,7.2,abs(vLocal.x));
 float breakup=.72+.28*h(vec2(vLocal.x*2.4+uTime*.025,vLocal.z*3.1+vLocal.y*1.2));
 float a=(.018+.060*edge)*body*breakup*uDensity*(1.-uDeep*.18);
 vec3 c=mix(vec3(.004,.008,.011),uFog,.72);
 gl_FragColor=vec4(c,a);
}\`;

"""
    if anchor not in s: raise RuntimeError("OceanMath anchor missing")
    s=s.replace(anchor,shell+anchor,1)

    # Resource program for contact shell.
    old="const r={mesh:program(shaderSet.meshVS,shaderSet.meshFS),hero:program(heroShaderSet.meshVS,heroShaderSet.meshFS),back:program(shaderSet.backVS,shaderSet.backFS)"
    new="const r={mesh:program(shaderSet.meshVS,shaderSet.meshFS),hero:program(heroShaderSet.meshVS,heroShaderSet.meshFS),shell:program(heroShaderSet.meshVS,VM12_WATER_SHELL_FS),back:program(shaderSet.backVS,shaderSet.backFS)"
    s=once(s,old,new,"shell program")

    # Render contact shell immediately before opaque hero. It never writes depth.
    old="""gl.depthMask(true);gl.disable(gl.BLEND);common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);
  gl.activeTexture(gl.TEXTURE0);"""
    new="""gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);uniform(r.shell,'uShell',.22);uniform(r.shell,'uDensity',1.0);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',g1Pose(state.shot));gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);
  gl.activeTexture(gl.TEXTURE0);"""
    s=once(s,old,new,"shell render")

    # Keep UI out of the film while the automatic 12-second visual gate runs.
    s=s.replace("function manual(){state.auto=false;notice(","function manual(){state.auto=false;main.classList.remove('visual-run');notice(",1)
    start_old="state.auto=true;state.paused=false;if(state.shot>=11.9)state.shot=0;"
    s=once(s,start_old,"state.auto=true;state.paused=false;main.classList.add('visual-run');if(state.shot>=11.9)state.shot=0;","visual run start")
    end_old="if(state.shot===12){state.auto=false;notice("
    s=once(s,end_old,"if(state.shot===12){state.auto=false;main.classList.remove('visual-run');notice(","visual run end")

    # Correct stage language in UI.
    s=s.replace("'ابدأ G2-MESH · ١٢ث'","'ابدأ VM-1R + VM-2 · ١٢ث'")
    s=s.replace("انتهت لقطة G2-MESH. راجع استمرارية التشريح في المرور القريب قبل التقدم.","انتهت لقطة VM-1R + VM-2. راجع الجلد والعين والفم والخياشيم واندماج الجسم بالماء.")
    s=s.replace("اختبار G2-MESH مدته ١٢ ثانية: نفس اللقطة، مع إصلاح استمرارية التشريح.","اختبار VM-1R + VM-2: لقطة بصرية كاملة لسطح القرش واندماجه بالماء.")

    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-1R + VM-2 Visual Integration. No generated images. G2-MESH-C1 anatomy remains locked. -->\\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode(); sha=hashlib.sha256(bb).hexdigest(); size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm1-v1","problem-ocean-vm12-v1")
probe=re.sub(r"const META=\\{[^\\n;]+\\};",
             "const META={id:'V7-VM1R-VM2',file:'Problem-OCEAN-SHARK-V7-VM1R-VM2-VISUAL-INTEGRATION.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-1R + VM-2 probe. Visual-first safety-floor measurement; not final performance acceptance. -->\\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
