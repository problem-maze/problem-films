from pathlib import Path
import hashlib,re,sys

def once(s, old, new, label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    if '<!doctype html>' in s:
        pre,rest=s.split('<!doctype html>',1)
        pre=pre.replace('\\n','\n')
        s=pre+'<!doctype html>'+rest

    s=s.replace('VM-1R + VM-2 — Creature / Water Integration','VM-2R — Contact & Light Integration')
    s=s.replace('VM-1R + VM-2 VISUAL INTEGRATION','VM-2R CONTACT / LIGHT INTEGRATION')
    s=s.replace('VM12_SHARK_SHADERS_SAFE','VM2R_SHARK_SHADERS_SAFE').replace('VM12_SHARK_SHADERS','VM2R_SHARK_SHADERS')
    s=s.replace('VM12_WATER_SHELL_FS','VM2R_WATER_SHELL_FS')
    s=s.replace('vm12-webgl-safe','vm2r-webgl-safe').replace('vm12-full','vm2r-full')

    old="""  for(const side of [-1,1])for(let g=0;g<5;g++)for(let j=0;j<segs;j++){
   const t0=j/segs,t1=(j+1)/segs,yy0=-.62+t0*.86,yy1=-.62+t1*.86;
   const curve0=.055*Math.sin(t0*Math.PI),curve1=.055*Math.sin(t1*Math.PI),xx=xs[g];
   const zz=side*(1.035+.025*g),w=.026;"""
    new="""  for(const side of [-1,1])for(let g=0;g<5;g++)for(let j=0;j<segs;j++){
   const t0=j/segs,t1=(j+1)/segs,baseY=-.60+g*.014,len=.80-g*.018,yy0=baseY+t0*len,yy1=baseY+t1*len;
   const curveAmp=.044+.004*g,curve0=curveAmp*Math.sin(t0*Math.PI),curve1=curveAmp*Math.sin(t1*Math.PI),xx=xs[g]+(g-2)*.008;
   const zz=side*(1.006+.017*g),w=.019;"""
    s=once(s,old,new,'gill surface geometry')

    s=once(s,
      "uniform mat4 uVP; uniform mat4 uModel; uniform float uTime; uniform float uAnimate; uniform float uShell;",
      "uniform mat4 uVP; uniform mat4 uModel; uniform float uTime; uniform float uAnimate; uniform float uShell; uniform float uWake;",
      'full uWake uniform')
    s=once(s,
      " p+=n*uShell; vec4 world=uModel*vec4(p,1.);",
      " p+=n*uShell; p.x+=uWake*smoothstep(-4.8,5.8,p.x); vec4 world=uModel*vec4(p,1.);",
      'full wake offset')
    s=once(s,
      "uniform mat4 uVP;uniform mat4 uModel;uniform float uTime;uniform float uAnimate;uniform float uShell;",
      "uniform mat4 uVP;uniform mat4 uModel;uniform float uTime;uniform float uAnimate;uniform float uShell;uniform float uWake;",
      'safe uWake uniform')
    s=once(s,
      "p+=n*uShell;vec4 w=uModel*vec4(p,1.);",
      "p+=n*uShell;p.x+=uWake*smoothstep(-4.8,5.8,p.x);vec4 w=uModel*vec4(p,1.);",
      'safe wake offset')

    old=""" vec3 color=albedo*(ambient+wrap*surfaceLight*vec3(.64,.675,.69)+diffuse2*vec3(.095,.108,.118));color*=1.-undersideAO-headAO;
 float wet=pow(1.-ndv,4.)*(vMaterial<2.5?1.:0.);"""
    new=""" vec3 color=albedo*(ambient+wrap*surfaceLight*vec3(.64,.675,.69)+diffuse2*vec3(.095,.108,.118));color*=1.-undersideAO-headAO;
 float farSide=smoothstep(.08,.72,-dot(N,L))*(vMaterial<2.5?1.:0.);
 float shoulderOcclusion=smoothstep(-5.45,-3.25,vLocal.x)*(1.-smoothstep(-3.10,-1.70,vLocal.x))*farSide;
 color*=1.-farSide*(.055+.045*uDeep)-shoulderOcclusion*.045;
 float localScatter=pow(max(0.,dot(-L,V)),4.)*(1.-ndv)*(vMaterial<2.5?1.:0.);
 color+=localScatter*(.018+.016*uDeep)*vec3(.31,.37,.40);
 float wet=pow(1.-ndv,4.)*(vMaterial<2.5?1.:0.);"""
    s=once(s,old,new,'body light integration')

    old="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),148.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),92.);
  float edgeFilm=pow(1.-ndv,3.2);
  float cornealVeil=pow(max(0.,dot(N,normalize(L+V))),22.)*.18;
  color+=vec3(.82,.86,.87)*cornea*1.08+vec3(.38,.41,.41)*sideCatch*.14+edgeFilm*.038*vec3(.42,.45,.46)+cornealVeil*vec3(.018,.022,.023);"""
    new="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),118.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),78.);
  float edgeFilm=pow(1.-ndv,2.7);
  float cornealVeil=pow(max(0.,dot(N,normalize(L+V))),16.)*.22;
  float tinyGlint=pow(max(0.,dot(N,normalize(vec3(-.20,.94,.28)))),150.);
  color+=vec3(.84,.88,.89)*cornea*1.16+vec3(.40,.43,.43)*sideCatch*.17+edgeFilm*.046*vec3(.43,.47,.48)+cornealVeil*vec3(.021,.025,.026)+tinyGlint*.22*vec3(.92,.95,.95);"""
    s=once(s,old,new,'eye cornea')

    old=""" if(vMaterial<.5&&mouthMask>.001){
  float lipSpec=pow(max(0.,dot(reflect(-L,N),V)),52.);
  color+=mouthMask*(vec3(.010,.004,.004)+lipSpec*.105*vec3(.72,.70,.68));
 }"""
    new=""" if(vMaterial<.5&&mouthMask>.001){
  float mouthOcclusion=smoothstep(.18,.82,mouthMask);
  float lipSpec=pow(max(0.,dot(reflect(-L,N),V)),68.)*(.35+.65*mouthOcclusion);
  color*=1.-mouthOcclusion*.10;
  color+=mouthMask*(vec3(.007,.0025,.0028)+lipSpec*.12*vec3(.70,.69,.67));
 }"""
    s=once(s,old,new,'mouth cavity')

    old=""" if(vMaterial>9.5&&vMaterial<10.5){
  float slitSpec=pow(max(0.,dot(reflect(-L,N),V)),34.);
  color+=gillFade*slitSpec*.016*vec3(.38,.31,.31);
 }"""
    new=""" if(vMaterial>9.5&&vMaterial<10.5){
  float core=pow(gillFade,1.25),edge=1.-smoothstep(.0,.58,gillFade);
  float slitSpec=pow(max(0.,dot(reflect(-L,N),V)),42.);
  color=mix(color,color*vec3(.72,.60,.60),core*.30);
  color=mix(color,vec3(.070,.073,.070),edge*.26);
  color+=core*slitSpec*.012*vec3(.34,.29,.29);
 }"""
    s=once(s,old,new,'gill lighting')

    s=s.replace("else if(vMaterial<9.5)a=vec3(.0007,.0010,.0012);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159);a=mix(vec3(.070,.072,.069),vec3(.050,.025,.026),.38+.36*gf);}",
                "else if(vMaterial<9.5)a=vec3(.0005,.0007,.0008);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159),gc=pow(gf,1.2);a=mix(vec3(.082,.083,.078),vec3(.040,.022,.023),.25+.52*gc);}",1)
    s=s.replace("if(vMaterial>8.5&&vMaterial<9.5)col+=spec*.42*vec3(.72,.86,.90);",
                "if(vMaterial>8.5&&vMaterial<9.5)col+=spec*.54*vec3(.76,.84,.86)+pow(1.-ndv,2.8)*.018*vec3(.35,.41,.43);",1)

    start=s.find("const VM2R_WATER_SHELL_FS=")
    end=s.find("const OceanMath=(()=>{",start)
    if start<0 or end<0: raise RuntimeError('shell shader block missing')
    bt=chr(96)
    shell="const VM2R_WATER_SHELL_FS="+bt+"""precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;uniform float uTime;uniform float uDensity;uniform float uMode;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
float h(vec2 p){return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);}
float n2(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}
void main(){
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);float ndv=abs(dot(N,V));
 float edge=pow(1.-ndv,1.35);
 float body=max((1.-smoothstep(5.3,7.0,abs(vLocal.x)))*smoothstep(-6.9,-5.7,vLocal.x),.38*(1.-smoothstep(5.6,6.9,abs(vLocal.x))));
 float breakup=.58+.42*n2(vec2(vLocal.x*1.55+uTime*.035,vLocal.z*2.0+vLocal.y*.62));
 float wake=smoothstep(-1.5,5.9,vLocal.x);
 if(uMode>.5){
   float a=(.012+.032*edge+.018*wake)*breakup*uDensity*(1.-uDeep*.12);
   gl_FragColor=vec4(vec3(.0025,.0045,.0065),a);
 }else{
   float a=(.010+.042*edge+.015*wake)*breakup*uDensity*(1.-uDeep*.18);
   vec3 c=mix(vec3(.006,.010,.013),uFog,.84);
   gl_FragColor=vec4(c,a);
 }
}"""+bt+""";

"""
    s=s[:start]+shell+s[end:]

    old="""  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);uniform(r.shell,'uShell',.22);uniform(r.shell,'uDensity',1.0);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',g1Pose(state.shot));gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);"""
    new="""  common(r.shell,cam);uniform(r.shell,'uAnimate',state.reduced?0:1);attributes(r.shell,r.whaleBuffer,meshLayout,40);uniform(r.shell,'uModel',g1Pose(state.shot));gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
  uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.12);uniform(r.shell,'uWake',.24);uniform(r.shell,'uDensity',.82);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  uniform(r.shell,'uMode',0);uniform(r.shell,'uShell',.30);uniform(r.shell,'uWake',.10);uniform(r.shell,'uDensity',.76);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.hero,cam);uniform(r.hero,'uAnimate',state.reduced?0:1);uniform(r.hero,'uShell',0);uniform(r.hero,'uWake',0);"""
    s=once(s,old,new,'dual shell render')

    s=s.replace("'ابدأ VM-1R + VM-2 · ١٢ث'","'ابدأ VM-2R · ١٢ث'")
    s=s.replace("انتهت لقطة VM-1R + VM-2. راجع الجلد والعين والفم والخياشيم واندماج الجسم بالماء.",
                "انتهت لقطة VM-2R. راجع عمق العين والفم والخياشيم والظل الحجمي واندماج الجسم بالماء.")
    s=s.replace("اختبار VM-1R + VM-2: لقطة بصرية كاملة لسطح القرش واندماجه بالماء.",
                "اختبار VM-2R: Contact & Light Integration — حكم بصري على العين والفم والخياشيم وحجم الماء حول الجسم.")
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-2R Contact & Light Integration. No generated images. G2-MESH-C1 anatomy remains locked; only gill surface-detail placement refined. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace('problem-ocean-vm12-v1','problem-ocean-vm2r-v1')
probe=re.sub(r"const META=\{[^\n;]+\};",
             "const META={id:'V7-VM2R',file:'Problem-OCEAN-SHARK-V7-VM2R-CONTACT-LIGHT-INTEGRATION.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-2R probe: visual-first safety-floor measurement, not final performance acceptance. -->\n"+probe
Path(sys.argv[4]).write_text(probe)
print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
