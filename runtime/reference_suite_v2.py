import json,math,hashlib,pathlib,platform
MU=3.986004418e14; RE=6378137.0
cases=[{"name":"LEO400","r":RE+400e3},{"name":"GEO","r":42164e3},{"name":"LEO200_GEO_HOHMANN","r1":RE+200e3,"r2":42164e3}]
out=[]
for c in cases:
 if "r" in c:
  r=c["r"]; v=math.sqrt(MU/r); T=2*math.pi*math.sqrt(r**3/MU); v2=2*math.pi*r/T
  out.append({"name":c["name"],"velocity_m_s":v,"period_s":T,"crosscheck_velocity_m_s":v2,"delta_m_s":abs(v-v2)})
 else:
  r1,r2=c["r1"],c["r2"]; a=(r1+r2)/2; v1=math.sqrt(MU/r1);v2=math.sqrt(MU/r2);vt1=math.sqrt(MU*(2/r1-1/a));vt2=math.sqrt(MU*(2/r2-1/a));dv1=vt1-v1;dv2=v2-vt2
  out.append({"name":c["name"],"dv1_m_s":dv1,"dv2_m_s":dv2,"total_dv_m_s":dv1+dv2,"transfer_time_s":math.pi*math.sqrt(a**3/MU)})
checks={"circular_identity_max_delta_m_s":max(x.get("delta_m_s",0) for x in out),"hohmann_reference_error_m_s":abs(out[2]["total_dv_m_s"]-3935.0)}
passed=checks["circular_identity_max_delta_m_s"]<1e-9 and checks["hohmann_reference_error_m_s"]<30
res={"farm":123,"stage":"S6_REFERENCE_TEST_CANDIDATE","engine":"python-orbital-reference-suite-v2","python":platform.python_version(),"cases":out,"checks":checks,"status":"REFERENCE_SUITE_OK" if passed else "FAIL","scope":"ANALYTIC_REFERENCE_SUITE_NOT_EXTERNAL_SIMULATOR_OR_PHYSICAL_VALIDATION"}
raw=json.dumps(res,sort_keys=True).encode();res["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f123_reference_suite.json").write_text(json.dumps(res,indent=2)+"\n");print(json.dumps(res));raise SystemExit(0 if passed else 1)
