import json,hashlib,pathlib,platform
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from poliastro.maneuver import Maneuver
r1=(Earth.R+200*u.km);r2=42164*u.km
o1=Orbit.circular(Earth,alt=200*u.km);o2=Orbit.circular(Earth,alt=(r2-Earth.R));man=Maneuver.hohmann(o1,r2);dv=sum(abs(x[1]).to_value(u.m/u.s) for x in man.impulses)
ref=3931.857009294854;err=abs(dv-ref);ok=err<5
out={"farm":123,"external_engine":"poliastro","poliastro_version":"0.17.0","python":platform.python_version(),"test":"LEO200_TO_GEO_HOHMANN_EXTERNAL_REPRODUCTION","external_total_dv_m_s":dv,"internal_reference_dv_m_s":ref,"absolute_delta_m_s":err,"status":"EXTERNAL_REPRODUCTION_OK" if ok else "FAIL","scope":"INDEPENDENT_SOFTWARE_IMPLEMENTATION_NOT_PHYSICAL_VALIDATION"}
raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f123_external_reproduction.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
