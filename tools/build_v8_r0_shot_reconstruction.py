from pathlib import Path
import hashlib
import re
import sys


VM4_BUILD_SHA256 = "ad35eb8645da646d06f315a5b18c595fe74c2ceb49f472fccfaf9cf1c5ce0bce"
VM4_PROBE_SHA256 = "f5515103a3d36104e8672771bebaa1138f4c7ec481d4cf8da5e8174f7688c97b"
BUILD_NAME = "Problem-OCEAN-SHARK-V8-R0-SHOT-RECONSTRUCTION.html"
PROBE_NAME = "Problem-OCEAN-SHARK-V8-R0-SHOT-RECONSTRUCTION-PROBE.html"


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


def patch_common(value):
    value = value.replace("VM-4 — Cinematic Master", "V8-R0 — Shot Reconstruction")
    value = value.replace("VM-4 CINEMATIC MASTER", "V8-R0 SHOT RECONSTRUCTION")
    value = value.replace("vm4-webgl-safe", "v8r0-webgl-safe")
    value = value.replace("vm4-full", "v8r0-full")

    value = once(
        value,
        "Problem — The Ocean Within / Shark V7 G3 Skin / Eye / Mouth Materials",
        "Problem — Ocean Shark V8-R0 / Shot Reconstruction",
        "document title",
    )
    value = once(
        value,
        "<b>MOONLIGHT STUDIES / SHARK V7 G3</b>",
        "<b>OCEAN SHARK V8 / REFERENCE RECONSTRUCTION</b>",
        "edition subtitle",
    )
    value = once(
        value,
        '<button class="chapter" data-time="0" aria-current="true"><span>01</span>ظهور</button><button class="chapter" data-time="3" aria-current="false"><span>02</span>اقتراب</button><button class="chapter" data-time="6" aria-current="false"><span>03</span>مرور</button><button class="chapter" data-time="9" aria-current="false"><span>04</span>خروج</button>',
        '<button class="chapter" data-time="0" aria-current="true"><span>01</span>ظهور</button><button class="chapter" data-time="2.6" aria-current="false"><span>02</span>اقتراب</button><button class="chapter" data-time="5.2" aria-current="false"><span>03</span>بطولة</button><button class="chapter" data-time="10.4" aria-current="false"><span>04</span>خروج</button>',
        "chapter controls",
    )
    value = once(
        value,
        '<div class="transport"><button id="journey" aria-pressed="false">ابدأ G2-MESH · ١٢ث</button>',
        '<div class="transport"><button id="journey" aria-pressed="false">ابدأ V8-R0 · ١٢ث</button>',
        "initial journey label",
    )
    value = once(
        value,
        "PROBLEM · SHARK V7 · V8-R0 SHOT RECONSTRUCTION MATERIALS",
        "PROBLEM · OCEAN SHARK V8-R0 · SHOT RECONSTRUCTION",
        "footnote",
    )

    old_keys = """ const keys=[
  [0,.15,2.92,13.70,0,.03,.34],
  [2.8,.10,2.42,12.55,-.05,-.03,.38],
  [5.6,1.72,1.52,10.95,-.78,-.08,.42],
  [8.0,5.50,.88,9.55,-2.20,-.06,.46],
  [9.45,7.82,.66,9.03,-3.15,-.03,.49],
  [10.55,8.34,.70,9.18,-3.82,.00,.51],
  [11.35,7.30,.91,9.63,-4.30,.06,.53],
  [12,5.36,1.38,10.15,-4.66,.12,.55]
 ];"""
    new_keys = """ const keys=[
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
    value = once(value, old_keys, new_keys, "R0 camera keys")

    old_shot = """  const b=keys[i],c=keys[i+1],a=keys[Math.max(0,i-1)],d=keys[Math.min(keys.length-1,i+2)];const f=(t-b[0])/(c[0]-b[0]);
  const vals=[1,2,3,4,5,6].map(k=>.5*(2*b[k]+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f));
  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*fit*zoom,(vals[1]+orbitY*12)*zoom,dz*fit*zoom],target=[vals[3],vals[4],0];
  const ci=Math.max(0,Math.min(1,(t-7.15)/1.85)),co=Math.max(0,Math.min(1,(11.85-t)/1.35));
  const cin=(ci*ci*(3-2*ci))*(co*co*(3-2*co));
  const fov=.67+.035*cin;
  return {...camera(eye,target,aspect,fov),deep:Math.max(0,Math.min(1,vals[5])),target,cin};"""
    new_shot = """  const b=keys[i],c=keys[i+1],a=keys[Math.max(0,i-1)],d=keys[Math.min(keys.length-1,i+2)];const f=(t-b[0])/(c[0]-b[0]);
  const vals=[1,2,3,4,5,6,7].map(k=>.5*(2*b[k]+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f));
  const fit=Math.max(1,.95/aspect),ca=Math.cos(orbitX),sa=Math.sin(orbitX),dx=vals[0]*ca+vals[2]*sa,dz=vals[2]*ca-vals[0]*sa;
  const eye=[dx*fit*zoom,(vals[1]+orbitY*12)*zoom,dz*fit*zoom],target=[vals[3],vals[4],vals[5]];
  const fi=Math.max(0,Math.min(1,(t-5.90)/1.35)),fo=Math.max(0,Math.min(1,(11.00-t)/1.20));
  const frame=(fi*fi*(3-2*fi))*(fo*fo*(3-2*fo));
  const fov=.67+.022*frame;
  return {...camera(eye,target,aspect,fov),deep:Math.max(0,Math.min(1,vals[6])),target,frame};"""
    value = once(value, old_shot, new_shot, "target-depth tracking and FOV pulse")

    value = once(
        value,
        "function cinematicCue(t){const a=clamp((t-7.15)/1.85,0,1),b=clamp((11.85-t)/1.35,0,1),sa=a*a*(3-2*a),sb=b*b*(3-2*b);return sa*sb;}",
        "function cinematicCue(t){const a=clamp((t-5.40)/1.20,0,1),b=clamp((9.15-t)/.80,0,1),sa=a*a*(3-2*a),sb=b*b*(3-2*b);return sa*sb;}",
        "hero light timing",
    )
    value = once(
        value,
        "const c=state.shot<3?0:state.shot<6?1:state.shot<9?2:3;",
        "const c=state.shot<2.6?0:state.shot<5.2?1:state.shot<10.4?2:3;",
        "chapter timing",
    )
    value = value.replace("'ابدأ VM-4 · ١٢ث'", "'ابدأ V8-R0 · ١٢ث'")
    value = value.replace(
        "انتهت لقطة VM-4. راجع framing الاقتراب والـclose pass والضوء والخروج مع الحفاظ على حركة VM-3R1.",
        "انتهت لقطة V8-R0. راجع الظهور والـhero frame والمرور القريب والخروج مع الحفاظ على حركة VM-3R1.",
    )
    value = value.replace(
        "اختبار VM-4: Cinematic Master — framing، close pass، ضوء الرأس والكتفين، والخروج النهائي.",
        "اختبار V8-R0: Shot Reconstruction — ظهور أمامي، hero frame، مرور قريب، ذيل، ثم خروج قصير للضباب.",
    )
    value = value.replace(
        "['03 / CLOSE PASS','هنا نحكم على الخامة.','الجلد والعين والفم والخياشيم تمر أمامك تحت نفس الضوء.','CLOSE PASS']",
        "['03 / HERO + CLOSE PASS','تظهر الكتلة كاملة.','الرأس والكتف والعين والخياشيم والجسم تبقى مقروءة خلال نافذة الضوء.','HERO WINDOW']",
    )
    return value


def patch_probe(value, build_sha256, build_bytes):
    value = value.replace(
        "<!-- VM-4 probe: cinematic visual gate; performance remains safety-floor only. -->",
        "<!-- V8-R0 phone probe: shot reconstruction visual gate; telemetry reports engine timing only. -->",
        1,
    )
    value = value.replace(
        "/* G2 anatomy probe: one 12-second measured shot, no second animation clock. */",
        "/* V8-R0 phone probe: one measured 12-second shot, no second animation clock. */",
        1,
    )
    value = value.replace("__G2R1", "__V8R0")
    value = value.replace("G2R1Probe", "V8R0Probe")
    value = value.replace("g2Probe", "v8r0Probe")
    value = value.replace("problem-ocean-vm4-v1", "problem-ocean-v8-r0-v1")
    value = re.sub(
        r"const META=\{[^\n;]+\};",
        "const META={id:'V8-R0',file:'%s',sha256:'%s',bytes:%d};"
        % (BUILD_NAME, build_sha256, build_bytes),
        value,
        count=1,
    )
    value = value.replace(
        "G3 probe locks interaction during the 12-second material proof. G3 PASS also requires close-pass visual inspection.",
        "V8-R0 probe locks interaction during the 12-second shot. Telemetry is engine timing, not screen-recording FPS; phone visual acceptance remains separate.",
    )
    value = value.replace("G2-MESH · shot measured — JSON", "V8-R0 · shot measured — JSON")
    value = value.replace("G2-MESH · invalid — repeat", "V8-R0 · invalid — repeat")
    value = value.replace("G2-MESH · warm-up 3s", "V8-R0 · warm-up 3s")
    value = value.replace(
        "G2-MESH · measuring 12s anatomy continuity",
        "V8-R0 · measuring 12s reconstructed shot",
    )
    value = value.replace("G2-v7-anatomy-phone.json", "V8-R0-phone-probe.json")
    value = value.replace("Start G2", "Start V8-R0")
    value = value.replace("G2 V7 · LOCKED", "V8-R0 · READY")
    return value


def main(argv):
    if len(argv) != 5:
        raise SystemExit(
            "usage: build_v8_r0_shot_reconstruction.py "
            "VM4_BUILD VM4_PROBE OUTPUT_BUILD OUTPUT_PROBE"
        )

    source_build = require_source(argv[1], VM4_BUILD_SHA256, "VM-4 build")
    source_probe = require_source(argv[2], VM4_PROBE_SHA256, "VM-4 probe")

    build = patch_common(source_build)
    build = (
        "<!-- V8-R0 Shot Reconstruction. VM-3R1 propulsion, authored anatomy, "
        "materials and water architecture preserved. -->\n" + build
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
