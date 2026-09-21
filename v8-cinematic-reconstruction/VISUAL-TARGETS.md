# V8 Visual Reference Decomposition

The four generated reference frames define a **direction**, not a pixel-perfect target.

## Reference A — frontal emergence
Useful traits:
- strong vertical canyon framing;
- bright but localized surface opening;
- shark centered as a heavy dark mass;
- underside readable without flattening the body;
- pectorals visible as mass-bearing planes;
- water volume visible between camera and animal.

Real-time translation:
- camera keeps frontal symmetry longer;
- stronger top/back key separation;
- subtle underside fill;
- deeper side-wall vignette;
- keep particles and haze sparse near face.

## Reference B — three-quarter side hero
Useful traits:
- best anatomy read;
- visible eye, gills, cheek, shoulder and pectoral root in one frame;
- wet specular breakup;
- top light travels across dorsal surface;
- background stays darker than shark highlights.

Real-time translation:
- this becomes the primary hero framing target;
- extend three-quarter window;
- move light peak earlier to coincide with head/shoulder visibility;
- use local head/shoulder sculpt instead of global brightness;
- preserve tail in frame without excessive FOV.

## Reference C — close face
Useful traits:
- readable eye globe;
- mouth cavity has depth;
- skin roughness is directional and uneven;
- lighting gives volume across snout and cheek;
- face feels wet, not glossy plastic.

Real-time translation:
- do not chase pore-level detail;
- increase contrast between cornea, scleral edge/limbal falloff and surrounding skin;
- deepen mouth cavity read using occlusion + insert already present;
- use roughness breakup and angled key instead of extra texture cost.

## Reference D — wider full-body hero
Useful traits:
- whole animal remains readable;
- canyon creates scale;
- tail movement is visible;
- shark sits inside water rather than pasted over it;
- exit path remains cinematic.

Real-time translation:
- keep body/tail in frame through propulsion peak;
- water shell density strongest near silhouette and shoulder;
- exit should transition back into haze instead of simply leaving screen;
- avoid extreme wide-angle distortion.

## Reality constraints
Do not attempt to reproduce:
- offline path-traced caustics;
- dense volumetric raymarching;
- complex subsurface skin;
- high-frequency displacement;
- expensive multi-light shadow maps.

Instead use:
- shot-timed key light;
- normal/roughness variation already in shader;
- local fog/backscatter;
- shell-based water interaction;
- camera/framing;
- geometry already present for eye/gill/mouth depth.
