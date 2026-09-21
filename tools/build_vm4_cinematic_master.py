from pathlib import Path
import hashlib,re,sys
BT=chr(96)

def once(s,old,new,label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    s=s.replace("VM-3R1 — Propulsion Readability","VM-4 — Cinematic Master")
    s=s.replace("VM-3R1 PROPULSION READABILITY","VM-4 CINEMATIC MASTER")
    s=s.replace("VM3R1_SHARK_SHADERS_SAFE","VM4_SHARK_SHADERS_SAFE").replace("VM3R1_SHARK_SHADERS","VM4_SHARK_SHADERS")
    s=s.replace("VM3R1_WATER_SHELL_FS","VM4_WATER_SHELL_FS")
    s=s.replace("VM3R1_CORNEA_FS","VM4_CORNEA_FS")
    s=s.replace("vm3r1-webgl-safe","vm4-webgl-safe").replace("vm3r1-full","vm4-full")

    s=once(s,"function camera(eye,target,aspect){","function camera(eye,target,aspect,fov=.67){","camera fov signature")
    s=once(s,
      "  const fov=.67;return {vp:multiply(perspective(fov,aspect,.15,180),view),forward,right,up,tan:Math.tan(fov/2),eye};",
      "  return {vp:multiply(perspective(fov,aspect,.15,180),view),forward,right,up,tan:Math.tan(fov/2),eye};",
      "camera dynamic fov")

    old_keys=""" const keys=[
  [0,.2,2.8,13.5,0,.0,.34],
  [3,.1,2.25,12.3,0,-.05,.38],
  [6,2.2,1.35,10.8,-.9,-.10,.42],
  [9,7.6,.65,8.9,-3.0,-.05,.48],
  [12,4.2,1.8,9.1,-4.2,.10,.54]
 ];"""
    new_keys=""" const keys=[
  [0,.15,2.92,13.70,0,.03,.34],
  [2.8,.10,2.42,12.55,-.05,-.03,.38],
  [5.6,1.72,1.52,10.95,-.78,-.08,.42],
  [8.0,5.50,.88,9.55,-2.20,-.06,.46],
  [9.45,7.82,.66,9.03,-3.15,-.03,.49],
  [10.55,8.34,.70,9.18,-3.82,.00,.51],
  [11.35,7.30,.91,9.63,-4.30,.06,.53],
  [12,5.36,1.38,10.15,-4.66,.12,.55]
 ];"""
    s=once(s,old_keys,new_keys,"cinematic camera keys")

    old_shot="""  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*fit*zoom,(vals[1]+orbitY*12)*zoom,dz*fit*zoom],target=[vals[3],vals[4],0];
  return {...camera(eye,target,aspect),deep:Math.max(0,Math.min(1,vals[5])),target};"""
    new_shot="""  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*fit*zoom,(vals[1]+orbitY*12)*zoom,dz*fit*zoom],target=[vals[3],vals[4],0];
  const ci=Math.max(0,Math.min(1,(t-7.15)/1.85)),co=Math.max(0,Math.min(1,(11.85-t)/1.35));
  const cin=(ci*ci*(3-2*ci))*(co*co*(3-2*co));
  const fov=.67+.035*cin;
  return {...camera(eye,target,aspect,fov),deep:Math.max(0,Math.min(1,vals[5])),target,cin};"""
    s=once(s,old_shot,new_shot,"close pass fov")

    s=once(s,
      " const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));",
      " const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));\n function cinematicCue(t){const a=clamp((t-7.15)/1.85,0,1),b=clamp((11.85-t)/1.35,0,1),sa=a*a*(3-2*a),sb=b*b*(3-2*b);return sa*sb;}",
      "cinematic cue")
    s=once(s,
      "function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uFog',[.010*(1-cam.deep*.20),.024*(1-cam.deep*.28),.034*(1-cam.deep*.24)]);}",
      "function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uCine',cinematicCue(state.shot));uniform(p,'uFog',[.010*(1-cam.deep*.20),.024*(1-cam.deep*.28),.034*(1-cam.deep*.24)]);}",
      "common cinematic uniform")

    s=once(s,
      "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
      "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform float uCine; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
      "full cine uniform")
    s=once(s,
      """ float farSide=smoothstep(.08,.72,-dot(N,L))*(vMaterial<2.5?1.:0.);
 float shoulderOcclusion=smoothstep(-5.45,-3.25,vLocal.x)*(1.-smoothstep(-3.10,-1.70,vLocal.x))*farSide;
 color*=1.-farSide*(.055+.045*uDeep)-shoulderOcclusion*.045;""",
      """ float farSide=smoothstep(.08,.72,-dot(N,L))*(vMaterial<2.5?1.:0.);
 float shoulderOcclusion=smoothstep(-5.45,-3.25,vLocal.x)*(1.-smoothstep(-3.10,-1.70,vLocal.x))*farSide;
 color*=1.-farSide*(.055+.045*uDeep)-shoulderOcclusion*.045;
 float cineFront=(1.-smoothstep(-1.75,-.35,vLocal.x))*(vMaterial<2.5?1.:0.);
 float cineShoulder=smoothstep(-6.15,-5.05,vLocal.x)*(1.-smoothstep(-2.45,-1.55,vLocal.x));
 float cineGate=cineFront*(.62+.38*cineShoulder);
 vec3 cineL=normalize(vec3(-.55,.80,.26));
 float cineDiff=max(0.,dot(N,cineL));
 float cineRim=pow(1.-ndv,2.45)*max(0.,dot(N,normalize(vec3(-.12,.94,.31))));
 color+=albedo*cineDiff*cineGate*uCine*surfaceLight*vec3(.060,.063,.064);
 color+=cineRim*cineGate*uCine*.024*vec3(.50,.55,.58);
 color*=1.-farSide*cineGate*uCine*.050;""",
      "full cinematic sculpt")

    safe_old="meshFS:"+BT+"precision mediump float;uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;"
    safe_new="meshFS:"+BT+"precision mediump float;uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;uniform float uCine;"
    s=once(s,safe_old,safe_new,"safe cine uniform")
    s=once(s,
      "float surf=clamp((vWorld.y+17.)/22.,.15,1.)*(1.-uDeep*.36);float wrap=max(0.,(dot(N,L)+.25)/1.25);vec3 col=a*(vec3(.215,.315,.365)+wrap*surf*vec3(.69,.78,.81));",
      "float surf=clamp((vWorld.y+17.)/22.,.15,1.)*(1.-uDeep*.36);float wrap=max(0.,(dot(N,L)+.25)/1.25);vec3 col=a*(vec3(.215,.315,.365)+wrap*surf*vec3(.69,.78,.81));float cf=(1.-smoothstep(-1.75,-.35,vLocal.x))*(vMaterial<2.5?1.:0.);float ck=max(0.,dot(N,normalize(vec3(-.55,.80,.26))))*cf*uCine;col+=a*ck*surf*vec3(.050,.053,.054);",
      "safe cinematic key")

    s=once(s,
      "uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;\nvarying vec3 vWorld;",
      "uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uCine;\nvarying vec3 vWorld;",
      "cornea cine uniform")
    s=once(s,
      """ float alpha=clamp(.025+fres*.13+spec*.62+side*.08,0.,.72);
 vec3 c=mix(vec3(.050,.060,.064),vec3(.64,.70,.72),spec*.72+fres*.16);""",
      """ float alpha=clamp(.025+fres*.13+spec*(.62+.06*uCine)+side*.08,0.,.74);
 vec3 c=mix(vec3(.050,.060,.064),vec3(.64,.70,.72),spec*(.72+.05*uCine)+fres*.16);""",
      "cornea close response")

    s=s.replace("'ابدأ VM-3R1 · ١٢ث'","'ابدأ VM-4 · ١٢ث'")
    s=s.replace("انتهت لقطة VM-3R1. راجع وضوح انتقال القوة للذيل مع بقاء الرأس والزعانف الصدرية هادئة.",
                "انتهت لقطة VM-4. راجع framing الاقتراب والـclose pass والضوء والخروج مع الحفاظ على حركة VM-3R1.")
    s=s.replace("اختبار VM-3R1: Propulsion Readability — ذيل أوضح، peduncle أنشط، counter-bend صغير، بدون مبالغة.",
                "اختبار VM-4: Cinematic Master — framing، close pass، ضوء الرأس والكتفين، والخروج النهائي.")
    s=s.replace("AUTHORED MESH / PROPULSION READABILITY / 12-SECOND MOTION TEST",
                "AUTHORED MESH / CINEMATIC MASTER / 12-SECOND SHOT TEST")
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-4 Cinematic Master. No generated images. VM-3R1 motion, anatomy, materials and contact-water baseline preserved. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm3r1-v1","problem-ocean-vm4-v1")
probe=re.sub(r"const META=\{[^\n;]+\};",
             "const META={id:'V7-VM4',file:'Problem-OCEAN-SHARK-V7-VM4-CINEMATIC-MASTER.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-4 probe: cinematic visual gate; performance remains safety-floor only. -->\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
