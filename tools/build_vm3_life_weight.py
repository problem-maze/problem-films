from pathlib import Path
import hashlib,re,sys

def once(s, old, new, label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def replace_mesh_vs(s, object_marker, new_vs):
    p=s.find(object_marker)
    if p<0: raise RuntimeError("missing shader object "+object_marker)
    a=s.find("meshVS:\`",p)
    if a<0: raise RuntimeError("missing meshVS "+object_marker)
    a+=len("meshVS:\`")
    b=s.find("\`,\n meshFS:",a)
    if b<0: raise RuntimeError("missing meshVS end "+object_marker)
    return s[:a]+new_vs+s[b:]

def patch(s):
    s=s.replace("VM-2R.2 — Local Feature Depth","VM-3 — Life & Weight")
    s=s.replace("VM-2R.2 LOCAL FEATURE DEPTH","VM-3 LIFE / WEIGHT")
    s=s.replace("VM2R2_SHARK_SHADERS_SAFE","VM3_SHARK_SHADERS_SAFE").replace("VM2R2_SHARK_SHADERS","VM3_SHARK_SHADERS")
    s=s.replace("VM2R2_WATER_SHELL_FS","VM3_WATER_SHELL_FS")
    s=s.replace("VM2R2_CORNEA_FS","VM3_CORNEA_FS")
    s=s.replace("vm2r2-webgl-safe","vm3-webgl-safe").replace("vm2r2-full","vm3-full")

    full_vs=r"""precision highp float;
attribute vec3 aPosition; attribute vec3 aNormal; attribute vec2 aUV; attribute float aMaterial; attribute float aPart;
uniform mat4 uVP; uniform mat4 uModel; uniform float uTime; uniform float uAnimate; uniform float uShell; uniform float uWake; uniform float uBank;
varying vec3 vWorld; varying vec3 vNormal; varying vec3 vLocal; varying vec2 vUV; varying float vMaterial; varying float vPart;
void main(){
 vec3 p=aPosition,n=aNormal; vLocal=p; vUV=aUV; vMaterial=aMaterial; vPart=aPart;
 float t=uTime*1.02;
 bool shark=(aMaterial<4.5 || aMaterial>8.5);
 if(shark){
  // VM-3: propulsion travels trunk -> peduncle -> caudal fin. The head is intentionally quiet.
  float headLock=smoothstep(-2.45,-.45,p.x);
  float trunk=smoothstep(-1.85,3.45,p.x);
  float peduncle=smoothstep(2.30,5.72,p.x);
  float phase=t*1.24-p.x*.390;
  float primary=sin(phase);
  float harmonic=.105*sin(phase*2.01+.72);
  float amp=(.0035*headLock+.0135*trunk+.055*pow(peduncle,1.55))*uAnimate;
  p.z+=(primary+harmonic)*amp;
  p.y+=sin(phase*.48+.90)*amp*.075*trunk;
  float slope=-(cos(phase)+.211*cos(phase*2.01+.72))*.390*amp;
  n.x-=slope*n.z;

  // Caudal drive lags the trunk wave instead of rotating with the whole body.
  if(aPart>2.0 && aPart<3.2){
   float tailPhase=t*1.24-5.55*.390-.30;
   float angle=(sin(tailPhase)*.285+.040*sin(tailPhase*2.02+.48))*uAnimate;
   float c=cos(angle),ss=sin(angle);vec2 q=p.xz-vec2(5.55,0.);
   p.xz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(5.55,0.);
   n.xz=vec2(c*n.x-ss*n.z,ss*n.x+c*n.z);
  }

  // Pectorals stabilize the body: no visible flapping, only small differential corrections.
  if(abs(aPart)>.5 && abs(aPart)<1.5){
   float side=sign(aPart);
   float finAngle=(-.034+sin(t*.43+side*.72)*.011)*side-uBank*.55;
   finAngle*=uAnimate;
   float c=cos(finAngle),ss=sin(finAngle);vec2 q=p.yz-vec2(-.26,side*1.12);
   p.yz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(-.26,side*1.12);
   n.yz=vec2(c*n.y-ss*n.z,ss*n.y+c*n.z);
  }

  // Small path bank and heave give mass without shaking the head.
  float bank=uBank*uAnimate;
  float cb=cos(bank),sb=sin(bank);
  p.yz=vec2(cb*p.y-sb*p.z,sb*p.y+cb*p.z);
  n.yz=vec2(cb*n.y-sb*n.z,sb*n.y+cb*n.z);
  p.y+=sin(t*.27)*.010*uAnimate;
 }
 if(aMaterial>6.5 && aMaterial<7.5){p.x+=sin(uTime*.13+aPart*.04)*3.;p.y+=sin(uTime*.6+aPart)*.13;}
 if(aMaterial>7.5 && aMaterial<8.5){float sway=sin(uTime*.62+aPart*.31+p.y*1.8)*(.08+.08*p.y);p.x+=sway;p.z+=sin(uTime*.45+aPart)*.025;}
 p+=n*uShell;
 p.x+=uWake*smoothstep(-4.8,5.8,p.x);
 vec4 world=uModel*vec4(p,1.);vWorld=world.xyz;vNormal=normalize(mat3(uModel)*n);gl_Position=uVP*world;
}
"""
    safe_vs=r"""precision mediump float;
attribute vec3 aPosition;attribute vec3 aNormal;attribute vec2 aUV;attribute float aMaterial;attribute float aPart;
uniform mat4 uVP;uniform mat4 uModel;uniform float uTime;uniform float uAnimate;uniform float uShell;uniform float uWake;uniform float uBank;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
void main(){
 vec3 p=aPosition,n=aNormal;vLocal=p;vUV=aUV;vMaterial=aMaterial;
 float t=uTime*1.02;
 if(aMaterial<4.5||aMaterial>8.5){
  float headLock=smoothstep(-2.45,-.45,p.x),trunk=smoothstep(-1.85,3.45,p.x),ped=smoothstep(2.30,5.72,p.x);
  float ph=t*1.24-p.x*.390;
  float amp=(.0035*headLock+.013*trunk+.053*pow(ped,1.5))*uAnimate;
  p.z+=(sin(ph)+.09*sin(ph*2.0+.72))*amp;
  p.y+=sin(ph*.48+.90)*amp*.065*trunk;
  if(aPart>2.0&&aPart<3.2){
   float tp=t*1.24-5.55*.390-.30,a=(sin(tp)*.275+.034*sin(tp*2.0+.48))*uAnimate,c=cos(a),ss=sin(a);
   vec2 q=p.xz-vec2(5.55,0.);p.xz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(5.55,0.);
  }
  if(abs(aPart)>.5&&abs(aPart)<1.5){
   float side=sign(aPart),a=((- .032+sin(t*.43+side*.72)*.009)*side-uBank*.50)*uAnimate,c=cos(a),ss=sin(a);
   vec2 q=p.yz-vec2(-.26,side*1.12);p.yz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(-.26,side*1.12);
  }
  float b=uBank*uAnimate,cb=cos(b),sb=sin(b);
  p.yz=vec2(cb*p.y-sb*p.z,sb*p.y+cb*p.z);
  n.yz=vec2(cb*n.y-sb*n.z,sb*n.y+cb*n.z);
  p.y+=sin(t*.27)*.009*uAnimate;
 }
 if(aMaterial>6.5&&aMaterial<7.5){p.x+=sin(uTime*.13+aPart*.04)*2.4;p.y+=sin(uTime*.55+aPart)*.10;}
 if(aMaterial>7.5&&aMaterial<8.5)p.x+=sin(uTime*.54+aPart*.31+p.y)*.07;
 p+=n*uShell;p.x+=uWake*smoothstep(-4.8,5.8,p.x);
 vec4 w=uModel*vec4(p,1.);vWorld=w.xyz;vNormal=normalize(vec3(uModel*vec4(n,0.)));gl_Position=uVP*w;
}
"""
    s=replace_mesh_vs(s,"const VM3_SHARK_SHADERS={",full_vs)
    s=replace_mesh_vs(s,"const VM3_SHARK_SHADERS_SAFE={",safe_vs)

    # Replace stop-start smoothstep trajectory with Catmull-Rom continuity.
    old=""" function g1Pose(t){
  const pts=[
   [0,0,.18,-28,1.5708,.82],
   [3,-.15,.10,-17,1.555,.82],
   [6,-.85,.00,-7.0,1.49,.82],
   [9,-3.9,-.12,1.0,1.28,.82],
   [12,-10.5,.08,14.0,1.04,.82]
  ];
  t=clamp(t,0,12);let i=0;while(i<pts.length-2&&t>pts[i+1][0])i++;
  const a=pts[i],b=pts[i+1],f=clamp((t-a[0])/(b[0]-a[0]),0,1),e=f*f*(3-2*f);
  const v=k=>a[k]+(b[k]-a[k])*e;
  return OceanMath.model(v(1),v(2),v(3),v(5),v(4));
 }"""
    new=""" function g1Pose(t){
  const pts=[
   [0,0,.18,-28,1.5708,.82],
   [3,-.15,.10,-17,1.555,.82],
   [6,-.85,.00,-7.0,1.49,.82],
   [9,-3.9,-.12,1.0,1.28,.82],
   [12,-10.5,.08,14.0,1.04,.82]
  ];
  t=clamp(t,0,12);let i=0;while(i<pts.length-2&&t>pts[i+1][0])i++;
  const p0=pts[Math.max(0,i-1)],p1=pts[i],p2=pts[i+1],p3=pts[Math.min(pts.length-1,i+2)];
  const f=clamp((t-p1[0])/(p2[0]-p1[0]),0,1),f2=f*f,f3=f2*f;
  const cr=k=>.5*(2*p1[k]+(-p0[k]+p2[k])*f+(2*p0[k]-5*p1[k]+4*p2[k]-p3[k])*f2+(-p0[k]+3*p1[k]-3*p2[k]+p3[k])*f3);
  return OceanMath.model(cr(1),cr(2),cr(3),cr(5),cr(4));
 }
 function g1Bank(t){
  const b=[[0,0],[3,-.006],[6,-.018],[9,-.040],[12,-.014]];
  t=clamp(t,0,12);let i=0;while(i<b.length-2&&t>b[i+1][0])i++;
  const p0=b[Math.max(0,i-1)],p1=b[i],p2=b[i+1],p3=b[Math.min(b.length-1,i+2)];
  const f=clamp((t-p1[0])/(p2[0]-p1[0]),0,1),f2=f*f,f3=f2*f;
  return .5*(2*p1[1]+(-p0[1]+p2[1])*f+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*f2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*f3);
 }"""
    s=once(s,old,new,"continuous trajectory and bank")

    # Compute one pose/bank per frame so shell, hero and cornea cannot drift apart.
    old="const cam=OceanMath.shot(state.shot,width/height,state.orbitX,state.orbitY,state.zoom),r=resources;"
    new="const cam=OceanMath.shot(state.shot,width/height,state.orbitX,state.orbitY,state.zoom),r=resources,sharkModel=g1Pose(state.shot),sharkBank=g1Bank(state.shot);"
    s=once(s,old,new,"frame pose cache")
    s=s.replace("g1Pose(state.shot)","sharkModel")

    # Bank must be identical across all shark passes.
    s=s.replace("uniform(r.shell,'uModel',sharkModel);gl.enable(gl.BLEND);",
                "uniform(r.shell,'uModel',sharkModel);uniform(r.shell,'uBank',sharkBank);gl.enable(gl.BLEND);",1)
    s=s.replace("common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);uniform(r.hero,'uWake',0);",
                "common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);uniform(r.hero,'uWake',0);uniform(r.hero,'uBank',sharkBank);",1)
    s=s.replace("common(r.cornea,cam);uniform(r.cornea,'uAnimate',state.reduced?0:1);uniform(r.cornea,'uShell',0);uniform(r.cornea,'uWake',0);",
                "common(r.cornea,cam);uniform(r.cornea,'uAnimate',state.reduced?0:1);uniform(r.cornea,'uShell',0);uniform(r.cornea,'uWake',0);uniform(r.cornea,'uBank',sharkBank);",1)

    # UI copy now tests movement, not surface micro-detail.
    s=s.replace("'ابدأ VM-2R.2 · ١٢ث'","'ابدأ VM-3 · ١٢ث'")
    s=s.replace("انتهت لقطة VM-2R.2. راجع العمق الهندسي للخياشيم والعين والفم قبل VM-3.",
                "انتهت لقطة VM-3. راجع ثبات الرأس وانتقال القوة للجذع والذيل والوزن أثناء المرور.")
    s=s.replace("اختبار VM-2R.2: Local Feature Depth — آخر فحص قصير قبل VM-3.",
                "اختبار VM-3: Life & Weight — ثبات الرأس، موجة عضلية متأخرة، ذيل دافع وزعانف تثبيت.")
    s=s.replace("AUTHORED MESH / MATERIAL REALITY / 12-SECOND CLOSE-PASS TEST",
                "AUTHORED MESH / LIFE + WEIGHT / 12-SECOND MOTION TEST")
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-3 Life & Weight. No generated images. VM-2R.2 local feature geometry and material/water master preserved. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm2r2-v1","problem-ocean-vm3-v1")
probe=re.sub(r"const META=\{[^\n;]+\};",
             "const META={id:'V7-VM3',file:'Problem-OCEAN-SHARK-V7-VM3-LIFE-WEIGHT.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-3 probe: motion/life visual gate; performance remains safety-floor only. -->\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
