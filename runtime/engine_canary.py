import json, math, hashlib, pathlib, platform
MU=3.986004418e14
r1=6378.137e3+200e3
r2=6378.137e3+35786e3
v1=math.sqrt(MU/r1); v2=math.sqrt(MU/r2)
a=(r1+r2)/2
vt1=math.sqrt(MU*(2/r1-1/a)); vt2=math.sqrt(MU*(2/r2-1/a))
dv1=vt1-v1; dv2=v2-vt2; total=dv1+dv2
expected=3935.0
ok=abs(total-expected)<30.0
out={"farm":123,"engine":"python-stdlib-orbital-mechanics","engine_version":platform.python_version(),"test":"LEO200_TO_GEO_HOHMANN","mu_m3_s2":MU,"r1_m":r1,"r2_m":r2,"dv1_m_s":dv1,"dv2_m_s":dv2,"total_dv_m_s":total,"reference_m_s":expected,"tolerance_m_s":30.0,"status":"REAL_ENGINE_CANARY_OK" if ok else "FAIL","epistemic_status":"NUMERICAL_REFERENCE_CANARY_NOT_PHYSICAL_VALIDATION"}
raw=json.dumps(out,sort_keys=True).encode(); out["result_sha256"]=hashlib.sha256(raw).hexdigest()
pathlib.Path("artifacts").mkdir(exist_ok=True); pathlib.Path("artifacts/f123_engine_canary.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out)); raise SystemExit(0 if ok else 1)
