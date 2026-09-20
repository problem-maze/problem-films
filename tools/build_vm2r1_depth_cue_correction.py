from pathlib import Path
import hashlib,re,sys

def once(s, old, new, label):
    if old not in s:
        raise RuntimeError("missing patch: "+label)
    return s.replace(old,new,1)

def patch(s):
    s=s.replace("VM-2R — Contact & Light Integration","VM-2R.1 — Depth Cue Correction")
    s=s.replace("VM-2R CONTACT / LIGHT INTEGRATION","VM-2R.1 DEPTH CUE CORRECTION")
    s=s.replace("VM2R_SHARK_SHADERS_SAFE","VM2R1_SHARK_SHADERS_SAFE").replace("VM2R_SHARK_SHADERS","VM2R1_SHARK_SHADERS")
    s=s.replace("VM2R_WATER_SHELL_FS","VM2R1_WATER_SHELL_FS")
    s=s.replace("vm2r-webgl-safe","vm2r1-webgl-safe").replace("vm2r-full","vm2r1-full")

    # Phone visual proof must be clean: remove status/top controls during the 12-second run.
    css=".visual-run .narrative,.visual-run .console,.visual-run .edition,.visual-run .depth,.visual-run .footnote,.visual-run .brand,.visual-run #sound{opacity:0;pointer-events:none}"
    if css in s:
        s=s.replace(css,css+".visual-run .status,.visual-run header{opacity:0;pointer-events:none}",1)

    # Gill ribbons: taper width at both ends and pull the detail closer to the body.
    old="""   const zz=side*(1.006+.017*g),w=.019;
   const a=pv(xx+curve0-w,yy0,zz,side,g/5,t0),b=pv(xx+curve0+w,yy0,zz,side,g/5,t0),c=pv(xx+curve1+w,yy1,zz,side,g/5,t1),d=pv(xx+curve1-w,yy1,zz,side,g/5,t1);"""
    new="""   const zz=side*(.998+.014*g),w0=.008+.014*Math.sin(t0*Math.PI),w1=.008+.014*Math.sin(t1*Math.PI);
   const a=pv(xx+curve0-w0,yy0,zz,side,g/5,t0),b=pv(xx+curve0+w0,yy0,zz,side,g/5,t0),c=pv(xx+curve1+w1,yy1,zz,side,g/5,t1),d=pv(xx+curve1-w1,yy1,zz,side,g/5,t1);"""
    s=once(s,old,new,"gill taper")

    # Mouth: narrower/darker cavity, restrained moist lip.
    old="""  float mouthCavity=mx*exp(-pow(mouthCenter*9.4,2.));
  float lipBand=mx*exp(-pow((abs(mouthCenter)-.105)*24.,2.));
  mouthMask=max(mouthCavity,lipBand*.72);
  albedo=mix(albedo,vec3(.034,.010,.011),mouthCavity*.78);
  albedo=mix(albedo,vec3(.155,.075,.070),lipBand*.26);
  rough=mix(rough,.14,mouthCavity*.86);rough=mix(rough,.24,lipBand*.56);"""
    new="""  float mouthCavity=mx*exp(-pow(mouthCenter*10.7,2.));
  float mouthDepth=pow(mouthCavity,1.32);
  float lipBand=mx*exp(-pow((abs(mouthCenter)-.096)*27.,2.));
  mouthMask=max(mouthDepth,lipBand*.66);
  albedo=mix(albedo,vec3(.018,.005,.006),mouthDepth*.90);
  albedo=mix(albedo,vec3(.128,.060,.057),lipBand*.22);
  rough=mix(rough,.105,mouthDepth*.92);rough=mix(rough,.22,lipBand*.50);"""
    s=once(s,old,new,"mouth depth")

    # Eye base: a deeper near-black globe with a visible limbal falloff, still non-cartoon.
    old="""  eyeFace=smoothstep(.20,.90,abs(N.z));
  float irisRing=smoothstep(.30,.54,eyeFace)*(1.-smoothstep(.72,.965,eyeFace));
  float limbal=1.-smoothstep(.72,.98,eyeFace);
  albedo=vec3(.00045,.00065,.00078)+irisRing*vec3(.0048,.0052,.0047);
  albedo*=.82+.18*limbal;
  rough=.018;"""
    new="""  eyeFace=smoothstep(.18,.92,abs(N.z));
  float irisRing=smoothstep(.28,.50,eyeFace)*(1.-smoothstep(.70,.965,eyeFace));
  float limbal=1.-smoothstep(.64,.97,eyeFace);
  float globeLift=pow(eyeFace,2.0);
  albedo=vec3(.00032,.00046,.00055)+irisRing*vec3(.0038,.0041,.0037)+globeLift*vec3(.0012,.00145,.0015);
  albedo*=.74+.26*limbal;
  rough=.012;"""
    s=once(s,old,new,"eye base")

    # Gill material: skin-like ends, dark recessed center.
    old="""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  float gillCore=pow(gillFade,.72);
  albedo=mix(vec3(.090,.088,.082),vec3(.040,.022,.023),.28+.48*gillCore);
  rough=mix(.48,.27,gillCore);"""
    new="""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  float gillCore=pow(gillFade,1.42);
  float gillEdge=1.-smoothstep(.12,.62,gillFade);
  albedo=mix(vec3(.118,.116,.108),vec3(.031,.017,.019),.18+.66*gillCore);
  albedo=mix(albedo,vec3(.135,.132,.123),gillEdge*.34);
  rough=mix(.54,.24,gillCore);"""
    s=once(s,old,new,"gill material")

    # Stronger but still tiny corneal cue on the phone.
    old="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),118.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),78.);
  float edgeFilm=pow(1.-ndv,2.7);
  float cornealVeil=pow(max(0.,dot(N,normalize(L+V))),16.)*.22;
  float tinyGlint=pow(max(0.,dot(N,normalize(vec3(-.20,.94,.28)))),150.);
  color+=vec3(.84,.88,.89)*cornea*1.16+vec3(.40,.43,.43)*sideCatch*.17+edgeFilm*.046*vec3(.43,.47,.48)+cornealVeil*vec3(.021,.025,.026)+tinyGlint*.22*vec3(.92,.95,.95);"""
    new="""  float cornea=pow(max(0.,dot(reflect(-L,N),V)),96.);
  float sideCatch=pow(max(0.,dot(reflect(-L2,N),V)),70.);
  float edgeFilm=pow(1.-ndv,2.45);
  float cornealVeil=pow(max(0.,dot(N,normalize(L+V))),13.)*.25;
  float cornealBand=exp(-pow((ndv-.72)*7.5,2.));
  float tinyGlint=pow(max(0.,dot(N,normalize(vec3(-.20,.94,.28)))),135.);
  color+=vec3(.84,.88,.89)*cornea*1.20+vec3(.40,.43,.43)*sideCatch*.18+edgeFilm*.052*vec3(.43,.47,.48)+cornealVeil*vec3(.023,.027,.028)+cornealBand*.012*vec3(.48,.52,.53)+tinyGlint*.28*vec3(.92,.95,.95);"""
    s=once(s,old,new,"cornea")

    # Mouth lighting: deepen center without creating a black painted smile.
    old="""  float mouthOcclusion=smoothstep(.18,.82,mouthMask);
  float lipSpec=pow(max(0.,dot(reflect(-L,N),V)),68.)*(.35+.65*mouthOcclusion);
  color*=1.-mouthOcclusion*.10;
  color+=mouthMask*(vec3(.007,.0025,.0028)+lipSpec*.12*vec3(.70,.69,.67));"""
    new="""  float mouthOcclusion=smoothstep(.14,.76,mouthMask);
  float mouthCore=pow(mouthOcclusion,1.35);
  float lipSpec=pow(max(0.,dot(reflect(-L,N),V)),72.)*(.28+.72*mouthOcclusion);
  color*=1.-mouthCore*.17;
  color+=mouthMask*(vec3(.0045,.0018,.0020)+lipSpec*.13*vec3(.69,.68,.66));"""
    s=once(s,old,new,"mouth lighting")

    # Gills: increase depth cue at the center; soften edges back toward body colour.
    old="""  float core=pow(gillFade,1.25),edge=1.-smoothstep(.0,.58,gillFade);
  float slitSpec=pow(max(0.,dot(reflect(-L,N),V)),42.);
  color=mix(color,color*vec3(.72,.60,.60),core*.30);
  color=mix(color,vec3(.070,.073,.070),edge*.26);
  color+=core*slitSpec*.012*vec3(.34,.29,.29);"""
    new="""  float core=pow(gillFade,1.48),edge=1.-smoothstep(.08,.62,gillFade);
  float slitSpec=pow(max(0.,dot(reflect(-L,N),V)),48.);
  color=mix(color,color*vec3(.61,.52,.53),core*.40);
  color=mix(color,vec3(.105,.108,.102),edge*.34);
  color+=core*slitSpec*.010*vec3(.32,.28,.28);"""
    s=once(s,old,new,"gill depth lighting")

    # Local water cues: stronger than VM-2R, but silhouette-focused to avoid a halo.
    s=s.replace("float localScatter=pow(max(0.,dot(-L,V)),4.)*(1.-ndv)*(vMaterial<2.5?1.:0.);\\n color+=localScatter*(.018+.016*uDeep)*vec3(.31,.37,.40);",
                "float localScatter=pow(max(0.,dot(-L,V)),4.)*pow(1.-ndv,1.25)*(vMaterial<2.5?1.:0.);\\n color+=localScatter*(.026+.021*uDeep)*vec3(.31,.37,.40);",1)
    s=s.replace("float waterWrap=pow(1.-ndv,2.1)*(.040+uDeep*.030);",
                "float waterWrap=pow(1.-ndv,2.35)*(.058+uDeep*.038);",1)

    # Dual shell stays asymmetric; raise density/extent moderately instead of making a symmetric glow.
    s=s.replace("uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.12);uniform(r.shell,'uWake',.24);uniform(r.shell,'uDensity',.82);",
                "uniform(r.shell,'uMode',1);uniform(r.shell,'uShell',.14);uniform(r.shell,'uWake',.30);uniform(r.shell,'uDensity',.98);",1)
    s=s.replace("uniform(r.shell,'uMode',0);uniform(r.shell,'uShell',.30);uniform(r.shell,'uWake',.10);uniform(r.shell,'uDensity',.76);",
                "uniform(r.shell,'uMode',0);uniform(r.shell,'uShell',.34);uniform(r.shell,'uWake',.14);uniform(r.shell,'uDensity',.90);",1)
    s=s.replace("float edge=pow(1.-ndv,1.35);","float edge=pow(1.-ndv,1.60);",1)
    s=s.replace("float a=(.012+.032*edge+.018*wake)*breakup*uDensity*(1.-uDeep*.12);",
                "float a=(.009+.038*edge+.020*wake)*breakup*uDensity*(1.-uDeep*.12);",1)
    s=s.replace("float a=(.010+.042*edge+.015*wake)*breakup*uDensity*(1.-uDeep*.18);",
                "float a=(.007+.048*edge+.018*wake)*breakup*uDensity*(1.-uDeep*.18);",1)

    # Safe path receives the key eye/gill visibility corrections.
    s=s.replace("else if(vMaterial<9.5)a=vec3(.0005,.0007,.0008);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159),gc=pow(gf,1.2);a=mix(vec3(.082,.083,.078),vec3(.040,.022,.023),.25+.52*gc);}",
                "else if(vMaterial<9.5)a=vec3(.00045,.0006,.0007);else if(vMaterial<10.5){float gf=sin(clamp(vUV.y,0.,1.)*3.14159),gc=pow(gf,1.45);a=mix(vec3(.105,.105,.098),vec3(.032,.019,.020),.18+.62*gc);}",1)
    s=s.replace("if(vMaterial>8.5&&vMaterial<9.5)col+=spec*.54*vec3(.76,.84,.86)+pow(1.-ndv,2.8)*.018*vec3(.35,.41,.43);",
                "if(vMaterial>8.5&&vMaterial<9.5)col+=spec*.62*vec3(.78,.85,.87)+pow(1.-ndv,2.55)*.024*vec3(.38,.43,.45);",1)

    s=s.replace("'ابدأ VM-2R · ١٢ث'","'ابدأ VM-2R.1 · ١٢ث'")
    s=s.replace("انتهت لقطة VM-2R. راجع عمق العين والفم والخياشيم والظل الحجمي واندماج الجسم بالماء.",
                "انتهت لقطة VM-2R.1. راجع الخياشيم والعين وعمق الفم وحجم الماء حول الجسم بدون halo.")
    s=s.replace("اختبار VM-2R: Contact & Light Integration — حكم بصري على العين والفم والخياشيم وحجم الماء حول الجسم.",
                "اختبار VM-2R.1: Depth Cue Correction — حكم بصري قصير قبل VM-3.")
    return s

build=patch(Path(sys.argv[1]).read_text())
build="<!-- VM-2R.1 Depth Cue Correction. No generated images. G2-MESH-C1 large-form anatomy remains locked. -->\n"+build
Path(sys.argv[3]).write_text(build)
bb=build.encode();sha=hashlib.sha256(bb).hexdigest();size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace("problem-ocean-vm2r-v1","problem-ocean-vm2r1-v1")
probe=re.sub(r"const META=\{[^\n;]+\};",
             "const META={id:'V7-VM2R1',file:'Problem-OCEAN-SHARK-V7-VM2R1-DEPTH-CUE-CORRECTION.html',sha256:'%s',bytes:%d};"%(sha,size),probe,1)
probe="<!-- VM-2R.1 probe: visual-first safety-floor measurement, not final performance acceptance. -->\n"+probe
Path(sys.argv[4]).write_text(probe)

print("BUILD_BYTES",size)
print("BUILD_SHA256",sha)
print("PROBE_BYTES",len(probe.encode()))
print("PROBE_SHA256",hashlib.sha256(probe.encode()).hexdigest())
