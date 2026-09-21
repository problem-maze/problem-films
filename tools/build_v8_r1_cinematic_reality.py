from pathlib import Path
import hashlib
import re
import sys


R0_BUILD_SHA256 = "47642578e701aa9e837134f4c017d47928f7a64179f0d1e6bf4b0bd55b4c803a"
R0_PROBE_SHA256 = "1e4b78f521c7c88316cde1aafb3c56f535846abe9398f02e2413a66951e82aec"
BUILD_NAME = "Problem-OCEAN-SHARK-V8-R1-CINEMATIC-REALITY.html"
PROBE_NAME = "Problem-OCEAN-SHARK-V8-R1-CINEMATIC-REALITY-PROBE.html"


def sha256_text(value):
    return hashlib.sha256(value.encode()).hexdigest()


def require_source(path, expected_sha256, label):
    data = Path(path).read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        raise RuntimeError(
            f"{label} SHA-256 mismatch: expected {expected_sha256}, got {actual}"
        )
    return data.decode()


def once(value, old, new, label):
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"expected one {label} patch site, found {count}")
    return value.replace(old, new, 1)


def replace_template_property(value, object_name, property_name, source):
    object_start = value.index(f"const {object_name}=")
    property_start = value.index(f" {property_name}:`", object_start)
    content_start = property_start + len(f" {property_name}:`")
    content_end = value.index("`", content_start)
    return value[:content_start] + source.strip() + value[content_end:]


def replace_template_constant(value, constant_name, source):
    marker = f"const {constant_name}=`"
    content_start = value.index(marker) + len(marker)
    content_end = value.index("`", content_start)
    return value[:content_start] + source.strip() + value[content_end:]


R1_FULL_BACKGROUND = r"""
precision highp float;varying vec2 vUV;
uniform vec3 uForward;uniform vec3 uRight;uniform vec3 uUp;uniform vec3 uEye;uniform vec3 uFog;uniform float uAspect;uniform float uTan;uniform float uTime;uniform float uDeep;uniform float uCine;uniform float uDeparture;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+1.),f.x),f.y);}
void main(){
 vec2 q=vUV*2.-1.;q.y-=.06;vec2 warp=vec2(noise(q*3.4+uTime*.012),noise(q*4.1-uTime*.010))-.5;
 vec2 refr=q+warp*.012*(1.-uDeep*.28);vec3 ray=normalize(uForward+uRight*refr.x*uTan*uAspect+uUp*refr.y*uTan);
 float upward=smoothstep(-.72,.86,ray.y);vec3 col=mix(vec3(.0015,.0035,.0060),vec3(.027,.046,.061),upward);
 float opening=exp(-dot((q-vec2(-.10,.70))*vec2(1.50,2.85),(q-vec2(-.10,.70))*vec2(1.50,2.85))*3.8);
 float surface=pow(max(0.,opening),2.15)*(1.-uDeep*.58);
 col+=surface*vec3(.155,.190,.213)*(1.+uCine*.10);
 float rayFan=pow(max(0.,1.-abs((q.x+.10)-(.70-q.y)*(.10+warp.x*.18))*4.2),3.)*smoothstep(-.40,.84,q.y);
 col+=rayFan*opening*vec3(.040,.058,.069)*(1.-uDeep*.62);
 float wallNoise=(noise(vec2(q.y*3.2,q.x*2.1)+4.7)-.5)*.12+(noise(q*7.1)-.5)*.035;
 float canyonWidth=.63-.12*(1.-smoothstep(-1.,.72,q.y));
 float left=1.-smoothstep(-canyonWidth+wallNoise-.035,-canyonWidth+wallNoise+.08,q.x);
 float right=smoothstep(canyonWidth+wallNoise-.08,canyonWidth+wallNoise+.035,q.x);
 float rock=max(left,right);float rockGrain=.72+.28*noise(q*vec2(12.,7.)+13.);
 vec3 rockCol=vec3(.0022,.0032,.0040)*rockGrain+opening*.008*vec3(.18,.23,.25);
 col=mix(col,rockCol,rock*.94);
 float distant=pow(hash(floor((q+vec2(uTime*.001,0.))*vec2(75.,110.))),28.)*(1.-rock)*(.010+.009*uCine);
 col+=distant*vec3(.48,.56,.61);
 col=mix(col,col*vec3(.70,.76,.82),uDeep*.58);
 col=mix(col,uFog,uDeparture*(.28+.24*(1.-opening)));
 float vig=1.-smoothstep(.38,1.30,length(q*vec2(.78,.66)))*.30;col*=vig;
 gl_FragColor=vec4(pow(max(col,vec3(0.)),vec3(.91)),1.);
}
"""


R1_SAFE_BACKGROUND = r"""
precision mediump float;varying vec2 vUV;uniform float uTime;uniform float uDeep;uniform float uCine;uniform float uDeparture;uniform vec3 uFog;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
void main(){
 vec2 q=vUV*2.-1.;q.y-=.06;float y=clamp(vUV.y,0.,1.);
 vec3 col=mix(vec3(.0015,.004,.007),vec3(.024,.049,.066),pow(y,1.45));
 vec2 oq=(q-vec2(-.10,.70))*vec2(1.48,2.82);float opening=exp(-dot(oq,oq)*3.9);
 col+=pow(opening,2.1)*vec3(.135,.177,.205)*(1.-uDeep*.58)*(1.+uCine*.08);
 float rayFan=pow(max(0.,1.-abs(q.x+.10-(.70-q.y)*.12)*4.4),3.)*opening;
 col+=rayFan*vec3(.031,.050,.062)*(1.-uDeep*.62);
 float rough=(h(vec2(q.y*5.7,q.x*3.1)+4.2)-.5)*.11;
 float width=.63-.12*(1.-smoothstep(-1.,.72,q.y));
 float rock=max(1.-smoothstep(-width+rough-.035,-width+rough+.08,q.x),smoothstep(width+rough-.08,width+rough+.035,q.x));
 vec3 rockCol=vec3(.002,.003,.004)*(.72+.28*h(q*11.+9.));col=mix(col,rockCol,rock*.95);
 col+=pow(h(floor(q*vec2(67.,101.))+uTime*.001),29.)*(1.-rock)*.009*vec3(.46,.55,.60);
 col=mix(col,col*vec3(.70,.77,.83),uDeep*.58);col=mix(col,uFog,uDeparture*.44);
 float vig=1.-smoothstep(.38,1.30,length(q*vec2(.78,.66)))*.30;
 gl_FragColor=vec4(pow(max(col*vig,vec3(0.)),vec3(.94)),1.);
}
"""


R1_SAFE_ENVIRONMENT = r"""
precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uTime;uniform float uDeep;uniform float uCine;uniform float uDeparture;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
void main(){
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);if(dot(N,V)<0.)N=-N;
 vec3 L=normalize(vec3(-.34,.91,.24)),H=normalize(L+V);float ndl=max(0.,dot(N,L)),ndv=max(.001,dot(N,V));
 float spec=pow(max(0.,dot(N,H)),28.);vec3 a=vec3(.070,.105,.119);
 if(vMaterial<4.5)a=vec3(.04,.06,.067);
 else if(vMaterial<5.5)a=vec3(.018,.030,.035);
 else if(vMaterial<6.5)a=mix(vec3(.006,.009,.011),vec3(.020,.028,.031),h(vWorld.xz*.18+vWorld.y*.04));
 else if(vMaterial<7.5)a=vec3(.075,.110,.118);
 else a=vec3(.012,.036,.029);
 float surf=clamp((vWorld.y+17.)/22.,.12,1.)*(1.-uDeep*.42);float wrap=max(0.,(dot(N,L)+.20)/1.20);
 vec3 col=a*(vec3(.14,.19,.22)+wrap*surf*vec3(.46,.55,.57));
 if(vMaterial>6.5&&vMaterial<7.5)col+=spec*.025*surf*vec3(.70,.80,.82);
 float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.016+uDeep*.013+uDeparture*.010));
 col=mix(col,uFog,clamp(fog+uDeparture*.24,0.,.88));col+=pow(1.-ndv,3.)*.010*surf*vec3(.18,.29,.34);
 gl_FragColor=vec4(pow(max(col,vec3(0.)),vec3(.94)),1.);
}
"""


R1_SAFE_SHARK = r"""
precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;uniform float uCine;uniform float uDeparture;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
void main(){
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);if(dot(N,V)<0.)N=-N;
 vec3 topL=normalize(vec3(-.23,.96,.17)),heroL=normalize(vec3(-.58,.73,.36));vec3 L=normalize(mix(topL,heroL,uCine*.70));
 vec3 H=normalize(L+V);float ndl=max(0.,dot(N,L)),ndv=max(.001,dot(N,V));
 float breakup=h(vLocal.xz*vec2(17.,13.)+vLocal.y*5.);float wetSpec=pow(max(0.,dot(N,H)),mix(22.,58.,breakup));
 vec3 a=vec3(.075,.105,.112);float gill=0.;
 if(vMaterial<.5){
  float radial=max(.42,length(vLocal.yz)),hn=clamp((vLocal.y+.015)/radial,-1.,1.);
  float boundary=-.11+(h(vec2(vLocal.x*.42,abs(vLocal.z)*.36))-.5)*.075;
  float belly=1.-smoothstep(boundary-.14,boundary+.19,hn),mott=h(vec2(vLocal.x*.73,vLocal.z*.58)+vLocal.y*.19);
  a=mix(vec3(.045,.052,.054),vec3(.405,.414,.399),belly);a*=.91+(mott-.5)*.13;
 }else if(vMaterial<1.5)a=vec3(.130,.172,.180);
 else if(vMaterial<2.5)a=vec3(.055,.083,.090);
 else if(vMaterial<3.5)a=vec3(.005,.007,.008);
 else if(vMaterial<4.5)a=vec3(.41,.42,.39);
 else if(vMaterial<8.5)a=vec3(.025,.045,.050);
 else if(vMaterial<9.5)a=vec3(.00025,.00034,.00038);
 else if(vMaterial<10.5){gill=sin(clamp(vUV.y,0.,1.)*3.14159);a=mix(vec3(.090,.088,.081),vec3(.016,.008,.009),.24+.70*pow(gill,1.45));}
 else if(vMaterial<11.5){gill=sin(clamp(vUV.y,0.,1.)*3.14159);a=mix(vec3(.024,.013,.014),vec3(.004,.002,.003),pow(gill,1.2));}
 else if(vMaterial<12.5)discard;
 else if(vMaterial<13.5){float cavity=1.-abs(vUV.y*2.-1.);a=mix(vec3(.053,.018,.020),vec3(.004,.0015,.002),pow(cavity,.72));}
 else a=vec3(.52,.53,.49);
 float surface=clamp((vWorld.y+17.)/22.,.13,1.)*(1.-uDeep*.40);
 float wrap=max(0.,(dot(N,L)+.20)/1.20);float head=1.-smoothstep(-2.0,-.25,vLocal.x);float shoulder=smoothstep(-6.5,-5.2,vLocal.x)*(1.-smoothstep(-1.9,-.9,vLocal.x));
 float localKey=uCine*head*(.54+.46*shoulder);float farSide=smoothstep(.10,.76,-dot(N,heroL));
 vec3 col=a*(vec3(.115,.155,.177)+wrap*surface*vec3(.53,.58,.59));
 col+=a*max(0.,dot(N,heroL))*localKey*surface*vec3(.20,.205,.20);col*=1.-farSide*localKey*.17;
 if(vMaterial<3.5)col+=wetSpec*(.018+.023*breakup)*surface*vec3(.69,.76,.78);
 col+=pow(1.-ndv,3.2)*.018*surface*vec3(.26,.36,.39);
 if(vMaterial>8.5&&vMaterial<9.5){float eyeGlint=pow(max(0.,dot(N,normalize(heroL+V))),92.);float limbal=pow(1.-ndv,2.4);col=col*.70+eyeGlint*(.18+.18*uCine)*vec3(.82,.86,.85)+limbal*.008*vec3(.24,.28,.29);}
 if(vMaterial>9.5&&vMaterial<11.5)col*=1.-pow(gill,1.35)*.22;
 if(vMaterial>12.5&&vMaterial<13.5)col*=.68;
 float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.014+uDeep*.012+uDeparture*.010));
 float posterior=smoothstep(-.4,4.7,vLocal.x),tailHold=smoothstep(4.8,6.7,vLocal.x)*(1.-smoothstep(.60,.93,uDeparture));
 float depart=uDeparture*(.16+.42*posterior)*(1.-tailHold*.42);col=mix(col,uFog,clamp(fog+depart,0.,.90));col*=1.-uDeparture*.15;
 gl_FragColor=vec4(pow(max(col,vec3(0.)),vec3(.92)),1.);
}
"""


R1_CORNEA = r"""
precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uCine;uniform float uDeparture;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
void main(){
 if(vMaterial<11.5||vMaterial>12.5)discard;
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);if(dot(N,V)<0.)N=-N;
 vec3 L=normalize(mix(vec3(-.23,.96,.17),vec3(-.58,.73,.36),uCine*.70)),H=normalize(L+V);
 float ndv=max(.001,dot(N,V)),fres=pow(1.-ndv,2.6),glint=pow(max(0.,dot(N,H)),118.);
 float pin=pow(max(0.,dot(N,normalize(vec3(-.18,.95,.25)))),170.);
 float alpha=clamp(.018+fres*.095+glint*(.30+.13*uCine)+pin*.12,0.,.58)*(1.-uDeparture*.38);
 vec3 c=vec3(.010,.014,.016)+fres*vec3(.028,.034,.035)+glint*vec3(.53,.58,.59)+pin*.22*vec3(.82,.85,.84);
 c=mix(c,uFog,uDeep*.055+uDeparture*.18);
 gl_FragColor=vec4(c,alpha);
}
"""


R1_WATER_SHELL = r"""
precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;uniform float uDensity;uniform float uMode;uniform float uCine;uniform float uDeparture;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}
void main(){
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);float ndv=abs(dot(N,V));
 float silhouette=pow(1.-ndv,1.45),face=pow(ndv,.72);
 float body=(1.-smoothstep(5.35,6.95,abs(vLocal.x)))*smoothstep(-6.95,-5.85,vLocal.x);
 float shoulder=smoothstep(-6.25,-5.05,vLocal.x)*(1.-smoothstep(-2.40,-1.25,vLocal.x));
 float wake=smoothstep(-.2,5.95,vLocal.x),breakup=.48+.52*n2(vec2(vLocal.x*1.35+uTime*.026,vLocal.z*1.75+vLocal.y*.55));
 if(uMode>.5){
  float a=(.003+.020*silhouette*body+.010*shoulder+.009*wake)*breakup*uDensity*(.82+.18*uCine);
  gl_FragColor=vec4(vec3(.0018,.0028,.0034),a);
 }else{
  float occupancy=(.004+.010*face*body+.010*shoulder+.008*wake+.009*uDeparture)*breakup*uDensity;
  vec3 c=mix(vec3(.005,.009,.012),uFog,.76);gl_FragColor=vec4(c,occupancy*(1.+uDeep*.22));
 }
}
"""


def patch_common(value):
    value = value.replace("V8-R0 — Shot Reconstruction", "V8-R1 — Cinematic Reality Reconstruction")
    value = value.replace("V8-R0 SHOT RECONSTRUCTION", "V8-R1 CINEMATIC REALITY")
    value = value.replace("V8-R0 / Shot Reconstruction", "V8-R1 / Cinematic Reality Reconstruction")
    value = value.replace("V8-R0 · SHOT RECONSTRUCTION", "V8-R1 · CINEMATIC REALITY")
    value = value.replace("V8-R0 · ١٢ث", "V8-R1 · ١٢ث")
    value = value.replace("v8r0-webgl-safe", "v8r1-webgl-safe")
    value = value.replace("v8r0-full", "v8r1-full")
    value = value.replace("VM4_SHARK_SHADERS", "V8R1_SHARK_SHADERS")
    value = value.replace("VM4_CORNEA_FS", "V8R1_CORNEA_FS")
    value = value.replace("VM4_WATER_SHELL_FS", "V8R1_WATER_SHELL_FS")

    value = once(
        value,
        '<button class="chapter" data-time="0" aria-current="true"><span>01</span>ظهور</button><button class="chapter" data-time="2.6" aria-current="false"><span>02</span>اقتراب</button><button class="chapter" data-time="5.2" aria-current="false"><span>03</span>بطولة</button><button class="chapter" data-time="10.4" aria-current="false"><span>04</span>خروج</button>',
        '<button class="chapter" data-time="0" aria-current="true"><span>01</span>ظهور</button><button class="chapter" data-time="2.5" aria-current="false"><span>02</span>اقتراب</button><button class="chapter" data-time="5.5" aria-current="false"><span>03</span>بطولة</button><button class="chapter" data-time="10.7" aria-current="false"><span>04</span>خروج</button>',
        "R1 chapter controls",
    )

    old_keys = """ const keys=[
  // t, eye x/y/z, target x/y/z, depth. Dense hero/pass keys prevent target snaps.
  [0,.12,2.92,13.70,0,.08,0,.34],
  [2.6,.08,2.40,12.50,-.08,.00,0,.38],
  [5.2,1.55,1.55,10.95,-.65,-.04,0,.42],
  [6.3,2.65,1.24,10.30,-1.25,-.05,0,.44],
  [7.2,3.75,1.03,9.80,-1.95,-.05,0,.46],
  [8.0,4.55,.90,9.35,-2.80,-.04,-.20,.48],
  [8.6,4.85,.82,9.10,-3.60,-.02,1.20,.50],
  [9.4,4.35,.76,9.20,-5.10,.00,4.00,.52],
  [10.4,3.00,.82,10.50,-6.70,.04,7.30,.55],
  [11.2,2.80,1.20,16.00,-8.55,.10,10.80,.63],
  [12,3.50,1.85,24.00,-10.25,.16,14.00,.70]
 ];"""
    new_keys = """ const keys=[
  // R1: t, eye x/y/z, target x/y/z, water depth. The 7-9s run is an intentional held composition.
  [0,.08,2.70,6.00,0,.06,-1.85,.32],
  [1.10,.06,2.58,7.55,-.02,.04,-1.12,.34],
  [2.50,.10,2.35,10.90,-.10,.01,-.30,.37],
  [3.35,.52,2.08,11.55,-.30,-.02,-.08,.39],
  [4.30,1.08,1.78,11.18,-.66,-.04,.02,.41],
  [5.50,1.82,1.48,10.88,-.82,-.05,.02,.43],
  [6.30,2.65,1.27,10.48,-1.25,-.05,.02,.44],
  [7.00,3.48,1.10,10.05,-1.80,-.04,.00,.45],
  [7.65,4.18,.98,9.70,-2.38,-.035,-.10,.46],
  [8.25,4.68,.90,9.34,-3.02,-.02,.35,.47],
  [8.70,4.82,.86,9.16,-3.72,-.01,1.48,.49],
  [9.00,4.68,.84,9.16,-4.36,.00,2.72,.50],
  [9.55,4.10,.80,9.36,-5.38,.02,4.72,.52],
  [10.15,3.40,.82,10.10,-6.35,.04,6.70,.55],
  [10.70,2.86,.94,12.20,-7.18,.06,8.85,.60],
  [11.15,2.82,1.18,16.10,-8.15,.10,10.75,.70],
  [11.58,3.05,1.50,20.30,-8.92,.14,12.15,.80],
  [12.00,3.42,1.88,24.80,-9.62,.19,13.48,.88]
 ];"""
    value = once(value, old_keys, new_keys, "R1 camera trajectory")

    old_shot = """  const b=keys[i],c=keys[i+1],a=keys[Math.max(0,i-1)],d=keys[Math.min(keys.length-1,i+2)];const f=(t-b[0])/(c[0]-b[0]);
  const vals=[1,2,3,4,5,6,7].map(k=>.5*(2*b[k]+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f));
  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*fit*zoom,(vals[1]+orbitY*12)*zoom,dz*fit*zoom],target=[vals[3],vals[4],vals[5]];
  const fi=Math.max(0,Math.min(1,(t-5.90)/1.35)),fo=Math.max(0,Math.min(1,(11.00-t)/1.20));
  const frame=(fi*fi*(3-2*fi))*(fo*fo*(3-2*fo));
  const fov=.67+.022*frame;
  return {...camera(eye,target,aspect,fov),deep:Math.max(0,Math.min(1,vals[6])),target,frame};"""
    new_shot = """  const b=keys[i],c=keys[i+1],a=keys[Math.max(0,i-1)],d=keys[Math.min(keys.length-1,i+2)];const f=(t-b[0])/(c[0]-b[0]);
  const vals=[1,2,3,4,5,6,7].map(k=>.5*(2*b[k]+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f));
  const portrait=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*portrait*zoom,(vals[1]+orbitY*12)*zoom,dz*portrait*zoom],target=[vals[3],vals[4],vals[5]];
  const fi=Math.max(0,Math.min(1,(t-5.65)/1.25)),fo=Math.max(0,Math.min(1,(9.35-t)/.55));
  const frame=(fi*fi*(3-2*fi))*(fo*fo*(3-2*fo));
  const fov=.640+.018*frame;
  return {...camera(eye,target,aspect,fov),deep:Math.max(0,Math.min(1,vals[6])),target,frame};"""
    value = once(value, old_shot, new_shot, "R1 portrait camera and controlled FOV")

    value = once(
        value,
        "function cinematicCue(t){const a=clamp((t-5.40)/1.20,0,1),b=clamp((9.15-t)/.80,0,1),sa=a*a*(3-2*a),sb=b*b*(3-2*b);return sa*sb;}",
        "function cinematicCue(t){const a=clamp((t-5.45)/1.35,0,1),b=clamp((9.35-t)/.65,0,1),sa=a*a*(3-2*a),sb=b*b*(3-2*b);return sa*sb;}\n function departureCue(t){const a=clamp((t-10.62)/1.18,0,1);return a*a*(3-2*a);}",
        "R1 hero and departure envelopes",
    )
    value = once(
        value,
        "function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uCine',cinematicCue(state.shot));uniform(p,'uFog',[.010*(1-cam.deep*.20),.024*(1-cam.deep*.28),.034*(1-cam.deep*.24)]);}",
        "function common(p,cam){gl.useProgram(p.p);uniform(p,'uVP',cam.vp);uniform(p,'uEye',cam.eye);uniform(p,'uTime',state.time);uniform(p,'uDeep',cam.deep);uniform(p,'uCine',cinematicCue(state.shot));uniform(p,'uDeparture',departureCue(state.shot));uniform(p,'uFog',[.008*(1-cam.deep*.34),.018*(1-cam.deep*.25),.026*(1-cam.deep*.18)]);}",
        "R1 phase-aware shared uniforms",
    )

    value = replace_template_property(value, "OCEAN_SHADERS", "backFS", R1_FULL_BACKGROUND)
    value = replace_template_property(value, "OCEAN_SHADERS_SAFE", "backFS", R1_SAFE_BACKGROUND)
    value = replace_template_property(value, "OCEAN_SHADERS_SAFE", "meshFS", R1_SAFE_ENVIRONMENT)
    value = replace_template_property(value, "V8R1_SHARK_SHADERS_SAFE", "meshFS", R1_SAFE_SHARK)
    value = replace_template_constant(value, "V8R1_CORNEA_FS", R1_CORNEA)
    value = replace_template_constant(value, "V8R1_WATER_SHELL_FS", R1_WATER_SHELL)

    value = once(
        value,
        "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
        "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform float uCine; uniform float uDeparture; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
        "full shark phase uniforms",
    )
    value = once(
        value,
        "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform float uCine; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
        "uniform vec3 uEye; uniform vec3 uFog; uniform float uTime; uniform float uDeep; uniform float uCine; uniform float uDeparture; uniform sampler2D uSkin; uniform sampler2D uSkinNormal; uniform sampler2D uSkinRough;",
        "full environment phase uniform",
    )
    value = once(
        value,
        "vec3 albedo=vec3(.10,.15,.18);float rough=.42;float skin=texture2D(uSkin,skinUv).r;",
        "vec3 albedo=vec3(.10,.15,.18);float rough=.42;float skin=texture2D(uSkin,skinUv).r;float mouthMask=0.;",
        "full environment compile fix",
    )
    value = once(
        value,
        "}else if(vMaterial<6.5){albedo=mix(vec3(.025,.07,.09),vec3(.15,.20,.20),noise(vWorld.xz*.31+vWorld.y));rough=.94;}",
        "}else if(vMaterial<6.5){albedo=mix(vec3(.006,.010,.013),vec3(.030,.038,.040),noise(vWorld.xz*.23+vWorld.y*.08));rough=.96;}",
        "graphite canyon palette",
    )
    value = once(
        value,
        "float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.018+uDeep*.009));\n color=mix(color*1.24,uFog,fog);color=pow(max(color,vec3(0.)),vec3(.86));",
        "float dist=length(uEye-vWorld);float fog=1.-exp(-dist*(.017+uDeep*.011+uDeparture*.009));\n color=mix(color*1.10,uFog,clamp(fog+uDeparture*.25,0.,.90));color=pow(max(color,vec3(0.)),vec3(.89));",
        "environment depth departure",
    )

    value = once(
        value,
        "vec3 L=normalize(vec3(-.26,1.,.18)),L2=normalize(vec3(.48,.30,.82));",
        "vec3 topL=normalize(vec3(-.23,.96,.17)),heroL=normalize(vec3(-.58,.73,.36));vec3 L=normalize(mix(topL,heroL,uCine*.70)),L2=normalize(vec3(.34,.24,.91));",
        "coordinated full-path light directions",
    )
    value = once(
        value,
        "float surfaceLight=clamp((vWorld.y+17.)/22.,.16,1.)*(1.-uDeep*.38);\n float wrap=max(0.,(dot(N,L)+.28)/1.28);vec3 ambient=vec3(.155,.182,.205)*(1.-uDeep*.30);\n float undersideAO=.0;if(vMaterial<2.5)undersideAO=smoothstep(-.15,-.95,N.y)*.18;float headAO=(vMaterial<.5)?(1.-smoothstep(-6.4,-5.0,vLocal.x))*.045:0.;\n vec3 color=albedo*(ambient+wrap*surfaceLight*vec3(.64,.675,.69)+diffuse2*vec3(.095,.108,.118));color*=1.-undersideAO-headAO;",
        "float surfaceLight=clamp((vWorld.y+17.)/22.,.13,1.)*(1.-uDeep*.41);\n float wrap=max(0.,(dot(N,L)+.22)/1.22);vec3 ambient=vec3(.112,.142,.164)*(1.-uDeep*.35);\n float undersideAO=.0;if(vMaterial<2.5)undersideAO=smoothstep(-.10,-.94,N.y)*.21;float headAO=(vMaterial<.5)?(1.-smoothstep(-6.4,-5.0,vLocal.x))*.055:0.;\n vec3 color=albedo*(ambient+wrap*surfaceLight*vec3(.57,.595,.60)+diffuse2*vec3(.052,.061,.066));color*=1.-undersideAO-headAO;",
        "full shark top-source exposure",
    )
    value = once(
        value,
        "float farSide=smoothstep(.08,.72,-dot(N,L))*(vMaterial<2.5?1.:0.);\n float shoulderOcclusion=smoothstep(-5.45,-3.25,vLocal.x)*(1.-smoothstep(-3.10,-1.70,vLocal.x))*farSide;\n color*=1.-farSide*(.055+.045*uDeep)-shoulderOcclusion*.045;\n float cineFront=(1.-smoothstep(-1.75,-.35,vLocal.x))*(vMaterial<2.5?1.:0.);\n float cineShoulder=smoothstep(-6.15,-5.05,vLocal.x)*(1.-smoothstep(-2.45,-1.55,vLocal.x));\n float cineGate=cineFront*(.62+.38*cineShoulder);\n vec3 cineL=normalize(vec3(-.55,.80,.26));\n float cineDiff=max(0.,dot(N,cineL));\n float cineRim=pow(1.-ndv,2.45)*max(0.,dot(N,normalize(vec3(-.12,.94,.31))));\n color+=albedo*cineDiff*cineGate*uCine*surfaceLight*vec3(.060,.063,.064);\n color+=cineRim*cineGate*uCine*.024*vec3(.50,.55,.58);\n color*=1.-farSide*cineGate*uCine*.050;",
        "float farSide=smoothstep(.10,.76,-dot(N,heroL))*(vMaterial<2.5?1.:0.);\n float shoulderOcclusion=smoothstep(-5.65,-4.65,vLocal.x)*(1.-smoothstep(-2.65,-1.35,vLocal.x))*farSide;\n color*=1.-farSide*(.065+.050*uDeep)-shoulderOcclusion*.065;\n float cineFront=(1.-smoothstep(-1.85,-.28,vLocal.x))*(vMaterial<2.5?1.:0.);\n float cineShoulder=smoothstep(-6.45,-5.30,vLocal.x)*(1.-smoothstep(-2.30,-1.05,vLocal.x));\n float cineGate=cineFront*(.52+.48*cineShoulder);\n float cineDiff=max(0.,dot(N,heroL));float cineRim=pow(1.-ndv,2.85)*max(0.,dot(N,topL));\n color+=albedo*cineDiff*cineGate*uCine*surfaceLight*vec3(.205,.210,.205);\n color+=cineRim*cineGate*uCine*.018*vec3(.42,.47,.49);\n color*=1.-farSide*cineGate*uCine*.16;",
        "localized hero key and far-side falloff",
    )
    value = once(
        value,
        "float wet=pow(1.-ndv,4.)*(vMaterial<2.5?1.:0.);\n color+=pbr*vec3(.90,.98,1.04)*surfaceLight+rim*surfaceLight*vec3(.040,.068,.082)+wet*.026*vec3(.66,.72,.76);\n float microSpec=pow(max(0.,dot(reflect(-L,N),V)),28.)*(.45+.55*noise(vLocal.xz*vec2(54.,41.)));if(vMaterial<2.5)color+=microSpec*.019*surfaceLight*vec3(.80,.86,.90);",
        "float wet=pow(1.-ndv,4.4)*(vMaterial<2.5?1.:0.);\n color+=pbr*vec3(.82,.88,.91)*surfaceLight+rim*surfaceLight*vec3(.024,.038,.044)+wet*.014*vec3(.58,.63,.65);\n float microBreak=.22+.78*noise(vLocal.xz*vec2(39.,31.)+vLocal.y*17.);float microSpec=pow(max(0.,dot(reflect(-L,N),V)),34.)*microBreak;if(vMaterial<2.5)color+=microSpec*.014*surfaceLight*(.72+.28*uCine)*vec3(.72,.76,.77);",
        "wet rough surface breakup",
    )
    value = once(
        value,
        "float tinyGlint=pow(max(0.,dot(N,normalize(vec3(-.20,.94,.28)))),135.);\n  color+=vec3(.84,.88,.89)*cornea*1.20+vec3(.40,.43,.43)*sideCatch*.18+edgeFilm*.052*vec3(.43,.47,.48)+cornealVeil*vec3(.023,.027,.028)+cornealBand*.012*vec3(.48,.52,.53)+tinyGlint*.28*vec3(.92,.95,.95);",
        "float tinyGlint=pow(max(0.,dot(N,normalize(vec3(-.20,.94,.28)))),155.);\n  color=color*.78+vec3(.72,.76,.76)*cornea*(.58+.20*uCine)+vec3(.32,.34,.34)*sideCatch*.08+edgeFilm*.015*vec3(.34,.38,.39)+cornealVeil*vec3(.010,.012,.013)+cornealBand*.005*vec3(.42,.45,.45)+tinyGlint*(.12+.12*uCine)*vec3(.86,.88,.87);",
        "physical eye response",
    )
    value = once(
        value,
        "float dist=length(uEye-vWorld);vec3 extinction=vec3(.030,.018,.0105)*(1.+uDeep*.62);vec3 trans=exp(-dist*extinction);color*=mix(vec3(1.),trans,.44);\n float fog=1.-exp(-dist*(.0145+uDeep*.010));float backscatter=pow(max(dot(V,-L),0.),5.)*(1.-exp(-dist*.026))*(1.-uDeep*.25);color+=backscatter*vec3(.022,.040,.050);\n float waterWrap=pow(1.-ndv,2.35)*(.058+uDeep*.038);color=mix(color,uFog,waterWrap);\n color=mix(color,uFog,fog);color=pow(max(color,vec3(0.)),vec3(.88));",
        "float dist=length(uEye-vWorld);vec3 extinction=vec3(.031,.019,.011)*(1.+uDeep*.70);vec3 trans=exp(-dist*extinction);color*=mix(vec3(1.),trans,.46);\n float fog=1.-exp(-dist*(.0145+uDeep*.012+uDeparture*.010));float backscatter=pow(max(dot(V,-L),0.),5.)*(1.-exp(-dist*.026))*(1.-uDeep*.30);color+=backscatter*vec3(.015,.028,.034);\n float waterWrap=pow(1.-ndv,2.45)*(.040+uDeep*.036);color=mix(color,uFog,waterWrap);\n float posterior=smoothstep(-.4,4.7,vLocal.x),tailHold=smoothstep(4.8,6.7,vLocal.x)*(1.-smoothstep(.60,.93,uDeparture));\n float depart=uDeparture*(.16+.42*posterior)*(1.-tailHold*.42);color=mix(color,uFog,clamp(fog+depart,0.,.90));color*=1.-uDeparture*.15;color=pow(max(color,vec3(0.)),vec3(.90));",
        "full-path depth departure",
    )

    value = once(
        value,
        "beamFS:`precision mediump float;varying vec2 vBeam;varying float vFade;uniform float uDeep;void main(){float alpha=exp(-vBeam.x*vBeam.x*6.)*pow(1.-vBeam.y,1.3)*.082*vFade*(1.-uDeep*.65);gl_FragColor=vec4(.50,.56,.61,alpha);}`",
        "beamFS:`precision mediump float;varying vec2 vBeam;varying float vFade;uniform float uDeep;uniform float uCine;uniform float uDeparture;void main(){float alpha=exp(-vBeam.x*vBeam.x*6.5)*pow(1.-vBeam.y,1.45)*.060*vFade*(.88+.18*uCine)*(1.-uDeep*.68)*(1.-uDeparture*.48);gl_FragColor=vec4(.43,.49,.52,alpha);}`",
        "restrained motivated light beams",
    )

    old_render = """  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',sharkModel);uniform(r.shell,'uBank',sharkBank);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
  uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.13);uniform(r.shell,'uWake',.31);uniform(r.shell,'uDensity',1.06);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  uniform(r.shell,'uMode',0);uniform(r.shell,'uShell',.34);uniform(r.shell,'uWake',.14);uniform(r.shell,'uDensity',.90);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);uniform(r.hero,'uWake',0);uniform(r.hero,'uBank',sharkBank);
  gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,r.texture);let loc=gl.getUniformLocation(r.hero.p,'uSkin');if(loc!==null)gl.uniform1i(loc,0);
  gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,r.normalTexture);loc=gl.getUniformLocation(r.hero.p,'uSkinNormal');if(loc!==null)gl.uniform1i(loc,1);
  gl.activeTexture(gl.TEXTURE2);gl.bindTexture(gl.TEXTURE_2D,r.roughTexture);loc=gl.getUniformLocation(r.hero.p,'uSkinRough');if(loc!==null)gl.uniform1i(loc,2);gl.activeTexture(gl.TEXTURE0);
  attributes(r.hero,r.whaleBuffer,meshLayout,40);uniform(r.hero,'uModel',sharkModel);uniform(r.hero,'uTime',state.time);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  common(r.cornea,cam);"""
    new_render = """  // Dark contact density sits behind the opaque animal and anchors its silhouette without a bright shell.
  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',sharkModel);uniform(r.shell,'uBank',sharkBank);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
  uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.12);uniform(r.shell,'uWake',.26);uniform(r.shell,'uDensity',1.02);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);uniform(r.hero,'uWake',0);uniform(r.hero,'uBank',sharkBank);
  gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,r.texture);let loc=gl.getUniformLocation(r.hero.p,'uSkin');if(loc!==null)gl.uniform1i(loc,0);
  gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,r.normalTexture);loc=gl.getUniformLocation(r.hero.p,'uSkinNormal');if(loc!==null)gl.uniform1i(loc,1);
  gl.activeTexture(gl.TEXTURE2);gl.bindTexture(gl.TEXTURE_2D,r.roughTexture);loc=gl.getUniformLocation(r.hero.p,'uSkinRough');if(loc!==null)gl.uniform1i(loc,2);gl.activeTexture(gl.TEXTURE0);
  attributes(r.hero,r.whaleBuffer,meshLayout,40);uniform(r.hero,'uModel',sharkModel);uniform(r.hero,'uTime',state.time);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  // The second existing shell pass is composited over the body as broken water occupancy, never as a luminous rim.
  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',sharkModel);uniform(r.shell,'uBank',sharkBank);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
  uniform(r.shell,'uMode',0);uniform(r.shell,'uShell',.045);uniform(r.shell,'uWake',.10);uniform(r.shell,'uDensity',.82);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.cornea,cam);"""
    value = once(value, old_render, new_render, "integrated contact-water draw order")

    value = once(
        value,
        "const c=state.shot<2.6?0:state.shot<5.2?1:state.shot<10.4?2:3;",
        "const c=state.shot<2.5?0:state.shot<5.5?1:state.shot<10.7?2:3;",
        "R1 chapter timing",
    )
    value = value.replace(
        "انتهت لقطة V8-R0. راجع الظهور والـhero frame والمرور القريب والخروج مع الحفاظ على حركة VM-3R1.",
        "انتهت لقطة V8-R1. راجع الكتلة والضوء والماء والـhero frame والمرور والخروج مع الحفاظ على حركة VM-3R1.",
    )
    value = value.replace(
        "اختبار V8-R0: Shot Reconstruction — ظهور أمامي، hero frame، مرور قريب، ذيل، ثم خروج قصير للضباب.",
        "اختبار V8-R1: Cinematic Reality — ظهور ثقيل، hero مضاء داخل الماء، مرور مقروء، ثم ذوبان في العمق.",
    )
    value = value.replace(
        "تظهر الكتلة كاملة.",
        "الضوء يكشف الكتلة داخل الماء.",
    )
    return value


def patch_probe(value, build_sha256, build_bytes):
    value = value.replace(
        "<!-- V8-R0 phone probe: shot reconstruction visual gate; telemetry reports engine timing only. -->",
        "<!-- V8-R1 phone probe: cinematic-reality visual gate; telemetry reports engine timing only. -->",
        1,
    )
    value = value.replace(
        "/* V8-R0 phone probe: one measured 12-second shot, no second animation clock. */",
        "/* V8-R1 phone probe: one measured 12-second shot, no second animation clock. */",
        1,
    )
    value = value.replace("__V8R0", "__V8R1")
    value = value.replace("V8R0Probe", "V8R1Probe")
    value = value.replace("v8r0Probe", "v8r1Probe")
    value = value.replace("problem-ocean-v8-r0-v1", "problem-ocean-v8-r1-v1")
    value = re.sub(
        r"const META=\{[^\n;]+\};",
        "const META={id:'V8-R1',file:'%s',sha256:'%s',bytes:%d};"
        % (BUILD_NAME, build_sha256, build_bytes),
        value,
        count=1,
    )
    value = value.replace("V8-R0 probe", "V8-R1 probe")
    value = value.replace("V8-R0 · shot measured — JSON", "V8-R1 · shot measured — JSON")
    value = value.replace("V8-R0 · invalid — repeat", "V8-R1 · invalid — repeat")
    value = value.replace("V8-R0 · warm-up 3s", "V8-R1 · warm-up 3s")
    value = value.replace("V8-R0 · measuring 12s reconstructed shot", "V8-R1 · measuring 12s cinematic reality")
    value = value.replace("V8-R0-phone-probe.json", "V8-R1-phone-probe.json")
    value = value.replace("Start V8-R0", "Start V8-R1")
    value = value.replace("V8-R0 · READY", "V8-R1 · READY")
    return value


def main(argv):
    if len(argv) != 5:
        raise SystemExit(
            "usage: build_v8_r1_cinematic_reality.py "
            "R0_BUILD R0_PROBE OUTPUT_BUILD OUTPUT_PROBE"
        )

    source_build = require_source(argv[1], R0_BUILD_SHA256, "V8-R0 build")
    source_probe = require_source(argv[2], R0_PROBE_SHA256, "V8-R0 probe")

    build = patch_common(source_build)
    build = (
        "<!-- V8-R1 Cinematic Reality Reconstruction. Authored anatomy and both "
        "established VM-3R1 propulsion vertex paths remain locked. -->\n" + build
    )
    build_bytes = len(build.encode())
    build_sha256 = sha256_text(build)

    probe = patch_common(source_probe)
    probe = patch_probe(probe, build_sha256, build_bytes)
    Path(argv[3]).write_text(build)
    Path(argv[4]).write_text(probe)

    print("BUILD_FILE", Path(argv[3]).name)
    print("BUILD_BYTES", build_bytes)
    print("BUILD_SHA256", build_sha256)
    print("PROBE_FILE", Path(argv[4]).name)
    print("PROBE_BYTES", len(probe.encode()))
    print("PROBE_SHA256", sha256_text(probe))


if __name__ == "__main__":
    main(sys.argv)
