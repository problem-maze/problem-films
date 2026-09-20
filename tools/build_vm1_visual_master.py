from pathlib import Path
import hashlib,re,sys

def patch(s):
    s=s.replace('G3 — Skin / Eye / Mouth Materials','VM-1 — Creature & Color Master')
    s=s.replace('G3 SKIN / EYE / MOUTH','VM-1 CREATURE / COLOR MASTER')
    s=s.replace('G3_SHARK_SHADERS_SAFE','VM1_SHARK_SHADERS_SAFE').replace('G3_SHARK_SHADERS','VM1_SHARK_SHADERS')
    s=s.replace('g3-webgl-safe','vm1-webgl-safe').replace('g3-full','vm1-full')
    # Visual-first safety floor: keep balanced/post on for the 4 GB / 4-core target;
    # only truly constrained devices begin on the low profile.
    s=s.replace(
        "const lowDevice=(deviceMemory>0&&deviceMemory<=3)||(deviceCores>0&&deviceCores<=4);",
        "const lowDevice=(deviceMemory>0&&deviceMemory<=2)||(deviceCores>0&&deviceCores<=2);"
    )
    s=s.replace("autoScale=lowDevice?.92:1.20","autoScale=lowDevice?.88:1.06")

    old="""  float uvAngular=sin(vUV.y*6.28318),geomAngular=clamp((vLocal.y+.04)/max(.36,length(vLocal.yz)),-1.,1.),angular=(vPart>199.&&vPart<240.)?geomAngular:uvAngular,belly=1.-smoothstep(-.29,.17,angular),flank=smoothstep(-.12,.46,angular)*(1.-smoothstep(.62,.95,angular));
  float boundaryNoise=(noise(vUV*vec2(29.,17.))-.5)*.12;belly=1.-smoothstep(-.29+boundaryNoise,.17+boundaryNoise,angular);
  vec3 dorsal=vec3(.078,.122,.140),mid=vec3(.20,.275,.295),ventral=vec3(.585,.615,.610);
  albedo=mix(dorsal,ventral,belly);albedo=mix(albedo,mid,flank*.22);
  float macro=fbm(vUV*vec2(27.,16.));float cloud=fbm(vUV*vec2(8.,13.)+vec2(2.1,5.7));
  albedo*=.74+skin*.28+macro*.13;albedo*=.94+cloud*.10;
  float lateralLine=exp(-pow(abs(angular)*19.,2.))*smoothstep(.10,.83,vUV.x);albedo*=1.-lateralLine*.035;
  float headMask=1.-smoothstep(.16,.42,vUV.x),mott=fbm(vUV*vec2(16.,31.));albedo*=1.-headMask*smoothstep(.61,.88,mott)*.11;
  float scar=step(.935,noise(vUV*vec2(19.,37.)))*smoothstep(.12,.90,vUV.x);albedo*=1.-scar*.15;rough=mix(.43,.70,scar);"""
    new="""  float radial=max(.42,length(vLocal.yz)),angular=clamp((vLocal.y+.015)/radial,-1.,1.);
  float macro=fbm(vec2(vLocal.x*.58,abs(vLocal.z)*.74+vLocal.y*.21));
  float boundary=-.105+(macro-.5)*.055+sin(vLocal.x*.43)*.012;
  float belly=1.-smoothstep(boundary-.17,boundary+.20,angular);
  float flank=smoothstep(boundary+.06,boundary+.42,angular)*(1.-smoothstep(.70,.96,angular));
  vec3 dorsal=vec3(.052,.061,.064),mid=vec3(.155,.170,.171),ventral=vec3(.505,.510,.492);
  albedo=mix(dorsal,ventral,belly);albedo=mix(albedo,mid,flank*.18);
  float cloud=fbm(vec2(vLocal.x*.22+3.1,vLocal.z*.32-vLocal.y*.14));
  albedo*=.93+(macro-.5)*.10+(cloud-.5)*.055;
  float lateralLine=exp(-pow(abs(angular-.04)*15.,2.))*smoothstep(-3.8,4.7,vLocal.x);albedo*=1.-lateralLine*.018;
  float headMask=1.-smoothstep(-5.25,-3.5,vLocal.x),mott=fbm(vec2(vLocal.x*.54,vLocal.z*.80));
  albedo*=1.-headMask*smoothstep(.69,.94,mott)*.045;
  float scar=smoothstep(.965,.995,noise(vec2(vLocal.x*2.1,vLocal.z*3.7)))*smoothstep(-3.8,4.8,vLocal.x);
  albedo*=1.-scar*.08;
  rough=clamp(.49+(macro-.5)*.10+(mapRough-.5)*.08+scar*.11,.38,.64);
  float mx=smoothstep(-6.45,-5.82,vLocal.x)*(1.-smoothstep(-4.70,-4.18,vLocal.x));
  mouthMask=mx*exp(-pow((angular+.39)*7.2,2.));
  albedo=mix(albedo,vec3(.042,.018,.018),mouthMask*.58);rough=mix(rough,.19,mouthMask*.72);"""
    if old not in s:
        raise RuntimeError('VM1 body source block not found')
    s=s.replace(old,new,1)

    s=s.replace("""  eyeFace=smoothstep(.34,.90,abs(N.z));
  float irisRing=smoothstep(.42,.66,eyeFace)*(1.-smoothstep(.82,.985,eyeFace));
  albedo=vec3(.0012,.0018,.0021)+irisRing*vec3(.008,.010,.009);
  rough=.035;""","""  eyeFace=smoothstep(.24,.88,abs(N.z));
  float irisRing=smoothstep(.36,.58,eyeFace)*(1.-smoothstep(.76,.96,eyeFace));
  albedo=vec3(.0007,.0010,.0012)+irisRing*vec3(.006,.0065,.0058);
  rough=.022;""",1)
    s=s.replace("""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  albedo=mix(vec3(.082,.090,.087),vec3(.050,.014,.018),.48+.42*gillFade);
  rough=.24;""","""  gillFade=sin(clamp(vUV.y,0.,1.)*3.14159);
  albedo=mix(vec3(.070,.072,.069),vec3(.050,.025,.026),.38+.36*gillFade);
  rough=.34;""",1)

    s=s.replace("vec3 L=normalize(vec3(-.30,1.,.22)),L2=normalize(vec3(.54,.26,.88));",
                "vec3 L=normalize(vec3(-.26,1.,.18)),L2=normalize(vec3(.48,.30,.82));",1)
    s=s.replace("vec3 ambient=vec3(.22,.34,.40)*(1.-uDeep*.34);",
                "vec3 ambient=vec3(.155,.182,.205)*(1.-uDeep*.30);",1)
    s=s.replace("wrap*surfaceLight*vec3(.70,.79,.82)+diffuse2*vec3(.14,.19,.21)",
                "wrap*surfaceLight*vec3(.64,.675,.69)+diffuse2*vec3(.095,.108,.118)",1)
    s=s.replace("wet*.018*vec3(.52,.78,.90)","wet*.026*vec3(.66,.72,.76)",1)
    s=s.replace("microSpec*.035*surfaceLight*vec3(.78,.92,1.)",
                "microSpec*.019*surfaceLight*vec3(.80,.86,.90)",1)
    s=s.replace("c*wrap*.050*surfaceLight*(1.-uDeep*.58)*vec3(.72,.95,1.0)",
                "c*wrap*.026*surfaceLight*(1.-uDeep*.62)*vec3(.72,.78,.80)",1)
    s=s.replace("thin*.055*vec3(.23,.42,.46)","thin*.032*vec3(.27,.33,.35)",1)
    s=s.replace("vec3(.73,.84,.88)*cornea*.72+vec3(.30,.39,.40)*sideCatch*.16+edgeFilm*.022*vec3(.33,.46,.48)",
                "vec3(.78,.84,.87)*cornea*.88+vec3(.34,.38,.39)*sideCatch*.18+edgeFilm*.030*vec3(.38,.43,.44)",1)
    s=s.replace("mouthMask*(vec3(.016,.007,.006)+lipSpec*.095*vec3(.70,.78,.79))",
                "mouthMask*(vec3(.010,.004,.004)+lipSpec*.125*vec3(.74,.76,.75))",1)
    s=s.replace("gillFade*slitSpec*.035*vec3(.52,.38,.38)",
                "gillFade*slitSpec*.022*vec3(.46,.34,.34)",1)
    s=s.replace("backscatter*vec3(.030,.080,.105)","backscatter*vec3(.022,.040,.050)",1)

    # Safe path receives the same large-form colour logic, at lower shader cost.
    s=s.replace(
      "float belly=smoothstep(-.12,.48,-vLocal.y);float mott=h(vUV*31.+vLocal.xz*.7);a=mix(vec3(.055,.095,.11),vec3(.52,.545,.535),belly);a*=.88+mott*.15;",
      "float radial=max(.42,length(vLocal.yz));float hn=clamp((vLocal.y+.015)/radial,-1.,1.);float bd=-.105+(h(vec2(vLocal.x*.38,abs(vLocal.z)*.32))-.5)*.05;float belly=1.-smoothstep(bd-.17,bd+.20,hn);float mott=h(vec2(vLocal.x*.7,vLocal.z*.52)+vLocal.y*.12);a=mix(vec3(.052,.061,.064),vec3(.505,.510,.492),belly);a*=.96+(mott-.5)*.07;",
      1
    )
    s=s.replace("a=vec3(.0015,.0022,.0025)","a=vec3(.0007,.0010,.0012)",1)
    s=s.replace("a=mix(vec3(.080,.087,.084),vec3(.050,.014,.018),.48+.42*gf)",
                "a=mix(vec3(.070,.072,.069),vec3(.050,.025,.026),.38+.36*gf)",1)

    # Dark Moonlight grade. VM1 changes colour response only; no new water system yet.
    repl={".002,.011,.018":".003,.005,.008",".037,.105,.145":".050,.066,.080",
          ".64,.70,.84":".76,.78,.83",".24,.32,.36":".34,.37,.40",
          ".09,.135,.16":".070,.086,.100",".078,.115,.135":".052,.066,.078",
          ".055,.12,.14":".038,.050,.060",".19,.37,.45":".135,.175,.205",
          ".035,.10,.13":".028,.042,.052",".42,.57,.65":".50,.56,.61",
          ".62,.78,.83":".66,.71,.75",".58,.84,.92":".68,.74,.79"}
    for a,b in repl.items(): s=s.replace(a,b)

    oldpost="vec3 c=texture2D(uScene,vUV).rgb;c+=texture2D(uScene,vUV+d).rgb*.13+texture2D(uScene,vUV-d).rgb*.13;"
    newpost="vec3 c=texture2D(uScene,vUV).rgb;c=(c+texture2D(uScene,vUV+d).rgb*.10+texture2D(uScene,vUV-d).rgb*.10)/1.20;float lum=dot(c,vec3(.2126,.7152,.0722));c=mix(vec3(lum),c,.78);c*=vec3(.96,.985,1.025);c=c/(vec3(1.)+c*.16);"
    s=s.replace(oldpost,newpost,1).replace("lens*.10","lens*.055",1).replace("*.24;c*=vig","*.20;c*=vig",1)
    s=s.replace("uniform(p,'uFog',[.018*(1-cam.deep*.3),.062*(1-cam.deep*.4),.089*(1-cam.deep*.3)])",
                "uniform(p,'uFog',[.010*(1-cam.deep*.20),.024*(1-cam.deep*.28),.034*(1-cam.deep*.24)])")
    return s

base=patch(Path(sys.argv[1]).read_text())
base="<!-- VM-1 Visual-First: Creature & Color Master. No generated images. Anatomy locked to G2-MESH-C1. -->\\n"+base
Path(sys.argv[3]).write_text(base)
bb=base.encode(); sha=hashlib.sha256(bb).hexdigest(); size=len(bb)

probe=patch(Path(sys.argv[2]).read_text())
probe=probe.replace('problem-ocean-g3-v1','problem-ocean-vm1-v1').replace("id:'V7-G3'","id:'V7-VM1'")
probe=re.sub(r"file:'[^']+',sha256:'[0-9a-f]{64}',bytes:\d+",
             "file:'Problem-OCEAN-SHARK-V7-VM1-CREATURE-COLOR-MASTER.html',sha256:'%s',bytes:%d"%(sha,size),probe,1)
probe="<!-- VM-1 probe: visual-first build identity locked. No generated images. -->\\n"+probe
Path(sys.argv[4]).write_text(probe)
print('BUILD_BYTES',size)
print('BUILD_SHA256',sha)
print('PROBE_BYTES',len(probe.encode()))
print('PROBE_SHA256',hashlib.sha256(probe.encode()).hexdigest())
