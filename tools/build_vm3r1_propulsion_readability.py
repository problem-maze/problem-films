from pathlib import Path
import hashlib,re,sys

BT=chr(96)

def replace_mesh_vs(s, object_marker, new_vs):
    p=s.find(object_marker)
    if p<0:
        raise RuntimeError("missing shader object "+object_marker)
    a=s.find("meshVS:"+BT,p)
    if a<0:
        raise RuntimeError("missing meshVS "+object_marker)
    a+=len("meshVS:"+BT)
    b=s.find(BT+",\n meshFS:",a)
    if b<0:
        raise RuntimeError("missing meshVS end "+object_marker)
    return s[:a]+new_vs+s[b:]

def once(s,old,new,label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    s=s.replace("VM-3 — Life & Weight","VM-3R1 — Propulsion Readability")
    s=s.replace("VM-3 LIFE / WEIGHT","VM-3R1 PROPULSION READABILITY")
    s=s.replace("VM3_SHARK_SHADERS_SAFE","VM3R1_SHARK_SHADERS_SAFE").replace("VM3_SHARK_SHADERS","VM3R1_SHARK_SHADERS")
    s=s.replace("VM3_WATER_SHELL_FS","VM3R1_WATER_SHELL_FS")
    s=s.replace("VM3_CORNEA_FS","VM3R1_CORNEA_FS")
    s=s.replace("vm3-webgl-safe","vm3r1-webgl-safe").replace("vm3-full","vm3r1-full")

    full_vs=r"""precision highp float;
attribute vec3 aPosition; attribute vec3 aNormal; attribute vec2 aUV; attribute float aMaterial; attribute float aPart;
uniform mat4 uVP; uniform mat4 uModel; uniform float uTime; uniform float uAnimate; uniform float uShell; uniform float uWake; uniform float uBank;
varying vec3 vWorld; varying vec3 vNormal; varying vec3 vLocal; varying vec2 vUV; varying float vMaterial; varying float vPart;
void main(){
 vec3 p=aPosition,n=aNormal; vLocal=p; vUV=aUV; vMaterial=aMaterial; vPart=aPart;
 float t=uTime*1.02;
 bool shark=(aMaterial<4.5 || aMaterial>8.5);
 if(shark){
  // VM-3R1: quiet head, readable trunk->peduncle->tail power transfer.
  float headLock=smoothstep(-2.35,-.20,p.x);
  float trunk=smoothstep(-1.65,3.10,p.x);
  float peduncle=smoothstep(2.00,5.45,p.x);
  float preTail=smoothstep(2.55,4.40,p.x)*(1.-smoothstep(4.65,5.45,p.x));
  float drive=t*1.48;
  float phase=drive-p.x*.425;
  float primary=sin(phase);
  float harmonic=.095*sin(phase*2.03+.78);
  float amp=(.0028*headLock+.0155*trunk+.071*pow(peduncle,1.65))*uAnimate;

  // Local S-curve before the caudal pivot makes the source of thrust visible.
  float tailPhase=drive-5.55*.425-.50;
  float counter=-sin(tailPhase)*preTail*.0155*uAnimate;
  p.z+=(primary+harmonic)*amp+counter;
  p.y+=sin(phase*.48+.90)*amp*.068*trunk;

  float slope=-(cos(phase)+.193*cos(phase*2.03+.78))*.425*amp;
  n.x-=slope*n.z;

  // Caudal sweep is stronger than VM-3, but still restrained and phase-lagged.
  if(aPart>2.0 && aPart<3.2){
   float angle=(sin(tailPhase)*.335+.046*sin(tailPhase*2.02+.48))*uAnimate;
   float c=cos(angle),ss=sin(angle);vec2 q=p.xz-vec2(5.55,0.);
   p.xz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(5.55,0.);
   n.xz=vec2(c*n.x-ss*n.z,ss*n.x+c*n.z);
  }

  // Keep pectorals in the VM-3 stabilization role; do not turn them into flapping propulsors.
  if(abs(aPart)>.5 && abs(aPart)<1.5){
   float side=sign(aPart);
   float finAngle=(-.034+sin(t*.43+side*.72)*.011)*side-uBank*.55;
   finAngle*=uAnimate;
   float c=cos(finAngle),ss=sin(finAngle);vec2 q=p.yz-vec2(-.26,side*1.12);
   p.yz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(-.26,side*1.12);
   n.yz=vec2(c*n.y-ss*n.z,ss*n.y+c*n.z);
  }

  // Preserve the subtle inertial bank and low-frequency body mass cue.
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
  float headLock=smoothstep(-2.35,-.20,p.x);
  float trunk=smoothstep(-1.65,3.10,p.x);
  float ped=smoothstep(2.00,5.45,p.x);
  float pre=smoothstep(2.55,4.40,p.x)*(1.-smoothstep(4.65,5.45,p.x));
  float drive=t*1.48,ph=drive-p.x*.425;
  float amp=(.0026*headLock+.0145*trunk+.067*pow(ped,1.62))*uAnimate;
  float tp=drive-5.55*.425-.50;
  p.z+=(sin(ph)+.085*sin(ph*2.03+.78))*amp-sin(tp)*pre*.014*uAnimate;
  p.y+=sin(ph*.48+.90)*amp*.060*trunk;

  if(aPart>2.0&&aPart<3.2){
   float a=(sin(tp)*.320+.040*sin(tp*2.02+.48))*uAnimate,c=cos(a),ss=sin(a);
   vec2 q=p.xz-vec2(5.55,0.);p.xz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(5.55,0.);
   n.xz=vec2(c*n.x-ss*n.z,ss*n.x+c*n.z);
  }

  if(abs(aPart)>.5&&abs(aPart)<1.5){
   float side=sign(aPart),a=((- .034+sin(t*.43+side*.72)*.010)*side-uBank*.52)*uAnimate,c=cos(a),ss=sin(a);
   vec2 q=p.yz-vec2(-.26,side*1.12);p.yz=vec2(c*q.x-ss*q.y,ss*q.x+c*q.y)+vec2(-.26,side*1.12);
   n.yz=vec2(c*n.y-ss*n.z,ss*n.y+c*n.z);
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

    s=replace_mesh_vs(s,"const VM3R1_SHARK_SHADERS={",full_vs)
    s=replace_mesh_vs(s,"const VM3R1_SHARK_SHADERS_SAFE={",safe_vs)

    s=s.replace("'ابدأ VM-3 · ١٢ث'","'ابدأ VM-3R1 · ١٢ث'")
    s=s.replace(
      "انتهت لقطة VM-3. راجع ثبات الرأس وانتقال القوة للجذع والذيل والوزن أثناء المرور.",
      "انتهت لقطة VM-3R1. راجع وضوح انتقال القوة للذيل مع بقاء الرأس والزعانف الصدرية هادئة."
    )
    s=s.replace(
      "اختبار VM-3: Life & Weight — ثبات الرأس، موجة عضلية متأخرة، ذيل دافع وزعانف تثبيت.",
      "اختبار VM-3R1: Propulsion Readability — ذيل أوضح، peduncle أنشط، counter-bend صغير، بدون مبالغة."
    )
    s=s.replace(
      "AUTHORED MESH / LIFE + WEIGHT / 12-SECOND MOTION TEST",
      "AUTHORED MESH / PROPULSION READABILITY / 12-SECOND MOTION TEST"
    )
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-3R1 Propulsion Readability. No generated images. Camera, materials, water and large-form anatomy remain locked. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm3-v1","problem-ocean-vm3r1-v1")
probe=re.sub(
    r"const META=\{[^\n;]+\};",
    "const META={id:'V7-VM3R1',file:'Problem-OCEAN-SHARK-V7-VM3R1-PROPULSION-READABILITY.html',sha256:'%s',bytes:%d};"%(sha,size),
    probe,1
)
probe="<!-- VM-3R1 probe: propulsion-readability gate; performance remains safety-floor only. -->\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
