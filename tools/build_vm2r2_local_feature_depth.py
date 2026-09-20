from pathlib import Path
import hashlib,re,sys

def once(s, old, new, label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    s=s.replace("VM-2R.1 — Depth Cue Correction","VM-2R.2 — Local Feature Depth")
    s=s.replace("VM-2R.1 DEPTH CUE CORRECTION","VM-2R.2 LOCAL FEATURE DEPTH")
    s=s.replace("VM2R1_SHARK_SHADERS_SAFE","VM2R2_SHARK_SHADERS_SAFE").replace("VM2R1_SHARK_SHADERS","VM2R2_SHARK_SHADERS")
    s=s.replace("VM2R1_WATER_SHELL_FS","VM2R2_WATER_SHELL_FS")
    s=s.replace("vm2r1-webgl-safe","vm2r2-webgl-safe").replace("vm2r1-full","vm2r2-full")

    # Add real local feature geometry: inner gill cores + shallow mouth insert.
    anchor=""" function add(M,mat){"""
    insert=""" function addGillCores(){
  const xs=[-4.42,-4.22,-4.02,-3.82,-3.62],segs=5;
  function pv(x,y,z,nz,u,v){return [x,y,z,0,0,nz,u,v,11,0]}
  function tri(a,b,c){out.push(...a,...b,...c)}
  for(const side of [-1,1])for(let g=0;g<5;g++)for(let j=0;j<segs;j++){
   const t0=j/segs,t1=(j+1)/segs,baseY=-.60+g*.014,len=.80-g*.018,yy0=baseY+t0*len,yy1=baseY+t1*len;
   const curveAmp=.044+.004*g,curve0=curveAmp*Math.sin(t0*Math.PI),curve1=curveAmp*Math.sin(t1*Math.PI),xx=xs[g]+(g-2)*.008;
   const zz=side*(.991+.014*g),w0=.0025+.0065*Math.sin(t0*Math.PI),w1=.0025+.0065*Math.sin(t1*Math.PI);
   const a=pv(xx+curve0-w0,yy0,zz,side,g/5,t0),b=pv(xx+curve0+w0,yy0,zz,side,g/5,t0),c=pv(xx+curve1+w1,yy1,zz,side,g/5,t1),d=pv(xx+curve1-w1,yy1,zz,side,g/5,t1);
   if(side>0){tri(a,b,c);tri(a,c,d)}else{tri(a,c,b);tri(a,d,c)}
  }
 }
 function addMouthInsert(){
  const segs=10,rows=[-1,0,1];
  function pv(x,y,z,nx,ny,nz,u,v){return [x,y,z,nx,ny,nz,u,v,13,0]}
  function tri(a,b,c){out.push(...a,...b,...c)}
  for(const side of [-1,1])for(let j=0;j<segs;j++){
   const t0=j/segs,t1=(j+1)/segs;
   const x0=-6.10+t0*1.56,x1=-6.10+t1*1.56;
   const taper0=.35+.65*Math.sin(t0*Math.PI),taper1=.35+.65*Math.sin(t1*Math.PI);
   const row=(x,taper,v,u)=>{
    const jawY=-.405+.025*(x+5.30),half=.052*taper;
    const y=jawY+v*half;
    const z=side*(.994+.018*Math.abs(v));
    const nx=-.04,ny=-.28+Math.abs(v)*.08,nz=side*.955;
    return pv(x,y,z,nx,ny,nz,u,(v+1)*.5);
   };
   const a0=row(x0,taper0,-1,t0),a1=row(x0,taper0,0,t0),a2=row(x0,taper0,1,t0);
   const b0=row(x1,taper1,-1,t1),b1=row(x1,taper1,0,t1),b2=row(x1,taper1,1,t1);
   if(side>0){tri(a0,b0,b1);tri(a0,b1,a1);tri(a1,b1,b2);tri(a1,b2,a2)}
   else{tri(a0,b1,b0);tri(a0,a1,b1);tri(a1,b2,b1);tri(a1,a2,b2)}
  }
 }
"""
    s=once(s,anchor,insert+anchor,"feature geometry insertion")

    # Eye globe and cornea shell share the same authored eye topology.
    old="""   }else if(mat>8.5&&mat<9.5){
    // eye globe follows the widened skull; move slightly outward and aft.
    z*=1.14;x+=.10;y+=.015;
   }"""
    new="""   }else if((mat>8.5&&mat<9.5)||(mat>11.5&&mat<12.5)){
    // eye globe and a separate thin corneal shell follow the widened skull.
    z*=1.14;x+=.10;y+=.015;
    if(mat>11.5&&mat<12.5){x+=nn[0]*.030;y+=nn[1]*.030;z+=nn[2]*.030;}
   }"""
    s=once(s,old,new,"cornea eye transform")
    s=once(s,
      " add(A.body,0);add(A.eye,9);addGills();return out",
      " add(A.body,0);add(A.eye,9);addGills();addGillCores();add(A.eye,12);addMouthInsert();return out",
      "feature geometry calls")

    # Ensure all local head features inherit the body's subtle vertical life.
    marker="const VM2R2_SHARK_SHADERS={"
    p=s.find(marker)
    if p<0: raise RuntimeError("hero shader marker missing")
    head=s[:p];tail=s[p:]
    tail=tail.replace("float t=uTime*1.12;\\n if(aMaterial<4.5){","float t=uTime*1.12;\\n if(aMaterial<4.5||aMaterial>8.5){",1)
    s=head+tail

    # Full hero material branch: inner gill core, transparent cornea (separate pass), mouth insert.
    old=""" }else if(vMaterial<10.5){
  // C1 geometric gill ribbons: charcoal-maroon tissue with length falloff, never pure black bars.
  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  float gillCore=pow(gillFade,1.42);
  float gillEdge=1.-smoothstep(.12,.62,gillFade);
  albedo=mix(vec3(.118,.116,.108),vec3(.031,.017,.019),.18+.66*gillCore);
  albedo=mix(albedo,vec3(.135,.132,.123),gillEdge*.34);
  rough=mix(.54,.24,gillCore);
 }else{albedo=vec3(.66,.67,.62);rough=.31;}"""
    new=""" }else if(vMaterial<10.5){
  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  float gillCore=pow(gillFade,1.42);
  float gillEdge=1.-smoothstep(.12,.62,gillFade);
  albedo=mix(vec3(.118,.116,.108),vec3(.031,.017,.019),.18+.66*gillCore);
  albedo=mix(albedo,vec3(.135,.132,.123),gillEdge*.34);
  rough=mix(.54,.24,gillCore);
 }else if(vMaterial<11.5){
  float slot=sin(clamp(vUV.y,0.,1.)*3.14159);
  albedo=mix(vec3(.036,.020,.021),vec3(.010,.006,.007),pow(slot,1.2));
  rough=.31;
 }else if(vMaterial<12.5){
  discard;
 }else if(vMaterial<13.5){
  float center=1.-abs(vUV.y*2.-1.);
  albedo=mix(vec3(.085,.031,.032),vec3(.012,.004,.005),pow(center,.72));
  rough=mix(.24,.085,pow(center,.9));
 }else{albedo=vec3(.66,.67,.62);rough=.31;}"""
    s=once(s,old,new,"full feature materials")

    # Extra full-shader light behavior for inner slit and mouth insert.
    old=""" if(vMaterial>10.5){float enamel=pow(max(0.,dot(reflect(-L,N),V)),45.);color+=enamel*.12*vec3(.90,.92,.89);}"""
    new=""" if(vMaterial>10.5&&vMaterial<11.5){
  float cavity=sin(clamp(vUV.y,0.,1.)*3.14159);
  color*=1.-pow(cavity,1.4)*.24;
 }
 if(vMaterial>12.5&&vMaterial<13.5){
  float wetCenter=1.-abs(vUV.y*2.-1.);
  float cavitySpec=pow(max(0.,dot(reflect(-L,N),V)),78.);
  color*=1.-pow(wetCenter,.8)*.16;
  color+=pow(wetCenter,1.4)*cavitySpec*.095*vec3(.64,.61,.59);
 }
 if(vMaterial>13.5){float enamel=pow(max(0.,dot(reflect(-L,N),V)),45.);color+=enamel*.12*vec3(.90,.92,.89);}"""
    s=once(s,old,new,"full feature lighting")

    # Safe shader material branch mirrors the local depth cues.
    old="else if(vMaterial<9.5)a=vec3(.00045,.0006,.0007);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159),gc=pow(gf,1.45);a=mix(vec3(.105,.105,.098),vec3(.032,.019,.020),.18+.62*gc);}else a=vec3(.80,.81,.76);"
    new="else if(vMaterial<9.5)a=vec3(.00045,.0006,.0007);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159),gc=pow(gf,1.45);a=mix(vec3(.105,.105,.098),vec3(.032,.019,.020),.18+.62*gc);}else if(vMaterial<11.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159);a=mix(vec3(.030,.018,.019),vec3(.008,.005,.006),gf);}else if(vMaterial<12.5)discard;else if(vMaterial<13.5){float mc=1.-abs(vUV.y*2.-1.);a=mix(vec3(.070,.027,.029),vec3(.011,.004,.005),mc);}else a=vec3(.80,.81,.76);"
    s=once(s,old,new,"safe feature materials")

    # A dedicated translucent cornea pass; only material 12 survives.
    anchor="const VM2R2_WATER_SHELL_FS="
    bt=chr(96)
    cornea="const VM2R2_CORNEA_FS="+bt+"""precision mediump float;
uniform vec3 uEye;uniform vec3 uFog;uniform float uDeep;
varying vec3 vWorld;varying vec3 vNormal;varying vec3 vLocal;varying vec2 vUV;varying float vMaterial;
void main(){
 if(vMaterial<11.5||vMaterial>12.5)discard;
 vec3 N=normalize(vNormal),V=normalize(uEye-vWorld);if(dot(N,V)<0.)N=-N;
 vec3 L=normalize(vec3(-.26,1.,.18)),H=normalize(L+V);
 float ndv=max(.001,dot(N,V));
 float fres=pow(1.-ndv,2.25);
 float spec=pow(max(0.,dot(N,H)),105.);
 float side=pow(max(0.,dot(N,normalize(vec3(.42,.34,.84)))),68.);
 float alpha=clamp(.025+fres*.13+spec*.62+side*.08,0.,.72);
 vec3 c=mix(vec3(.050,.060,.064),vec3(.64,.70,.72),spec*.72+fres*.16);
 c=mix(c,uFog,uDeep*.05);
 gl_FragColor=vec4(c,alpha);
}"""+bt+""";

"""
    if anchor not in s: raise RuntimeError("water shader anchor missing")
    s=s.replace(anchor,cornea+anchor,1)

    # Keep body-adjacent darkening stronger than the halo: focus the dark pass with body mask.
    s=s.replace("float a=(.009+.038*edge+.020*wake)*breakup*uDensity*(1.-uDeep*.12);",
                "float a=(.008+.040*edge+.021*wake)*breakup*mix(.55,1.,body)*uDensity*(1.-uDeep*.12);",1)
    s=s.replace("uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.14);uniform(r.shell,'uWake',.30);uniform(r.shell,'uDensity',.98);",
                "uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.13);uniform(r.shell,'uWake',.31);uniform(r.shell,'uDensity',1.06);",1)

    # Compile the dedicated cornea program.
    old="const r={mesh:program(shaderSet.meshVS,shaderSet.meshFS),hero:program(heroShaderSet.meshVS,heroShaderSet.meshFS),shell:program(heroShaderSet.meshVS,VM2R2_WATER_SHELL_FS),back:"
    new="const r={mesh:program(shaderSet.meshVS,shaderSet.meshFS),hero:program(heroShaderSet.meshVS,heroShaderSet.meshFS),cornea:program(heroShaderSet.meshVS,VM2R2_CORNEA_FS),shell:program(heroShaderSet.meshVS,VM2R2_WATER_SHELL_FS),back:"
    s=once(s,old,new,"cornea program resource")

    # Render transparent cornea after opaque shark, before particles.
    old="""gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  common(r.dust,cam);"""
    new="""gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);
  common(r.cornea,cam);uniform(r.cornea,'uAnimate',state.reduced?0:1);uniform(r.cornea,'uShell',0);uniform(r.cornea,'uWake',0);attributes(r.cornea,r.whaleBuffer,meshLayout,40);uniform(r.cornea,'uModel',g1Pose(state.shot));uniform(r.cornea,'uTime',state.time);gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);gl.drawArrays(gl.TRIANGLES,0,geometry.whale.length/10);gl.depthMask(true);gl.disable(gl.BLEND);
  common(r.dust,cam);"""
    s=once(s,old,new,"cornea render pass")

    s=s.replace("'ابدأ VM-2R.1 · ١٢ث'","'ابدأ VM-2R.2 · ١٢ث'")
    s=s.replace("انتهت لقطة VM-2R.1. راجع الخياشيم والعين وعمق الفم وحجم الماء حول الجسم بدون halo.",
                "انتهت لقطة VM-2R.2. راجع العمق الهندسي للخياشيم والعين والفم قبل VM-3.")
    s=s.replace("اختبار VM-2R.1: Depth Cue Correction — حكم بصري قصير قبل VM-3.",
                "اختبار VM-2R.2: Local Feature Depth — آخر فحص قصير قبل VM-3.")
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-2R.2 Local Feature Depth. No generated images. Large-form G2-MESH-C1 anatomy remains locked. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm2r1-v1","problem-ocean-vm2r2-v1")
probe=re.sub(r"const META=\{[^\n;]+\};",
             "const META={id:'V7-VM2R2',file:'Problem-OCEAN-SHARK-V7-VM2R2-LOCAL-FEATURE-DEPTH.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-2R.2 probe: last visual depth gate before VM-3; performance is safety-floor only. -->\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
