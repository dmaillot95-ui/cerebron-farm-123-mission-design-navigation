#!/usr/bin/env python3
import json, hashlib, math, pathlib, sys
req_path=pathlib.Path(sys.argv[1])
req=json.loads(req_path.read_text())
required=["mission_id","task_id","farm_id","operation","payload","input_sha","requested_at"]
missing=[k for k in required if k not in req]
if missing: raise SystemExit("MISSING_FIELDS:"+",".join(missing))
if req["farm_id"]!=123: raise SystemExit("WRONG_FARM")
if req["operation"]!="hohmann_reference": raise SystemExit("UNSUPPORTED_OPERATION")
p=req["payload"]
mu=float(p.get("mu_m3_s2",3.986004418e14)); r1=float(p.get("r1_m",6.778e6)); r2=float(p.get("r2_m",4.2164e7))
a=(r1+r2)/2
v1=(mu/r1)**0.5; vt1=(mu*(2/r1-1/a))**0.5
v2=(mu/r2)**0.5; vt2=(mu*(2/r2-1/a))**0.5
dv1=vt1-v1; dv2=v2-vt2; total=abs(dv1)+abs(dv2)
out={
 "protocol":"CEREBRON_FARM_BRIDGE_V1","farm_id":123,"mission_id":req["mission_id"],"task_id":req["task_id"],
 "operation":req["operation"],"status":"FARM_EXECUTED","engine":"python-stdlib-orbital-mechanics",
 "results":{"dv1_m_s":dv1,"dv2_m_s":dv2,"total_dv_m_s":total},
 "limitations":["two-body circular coplanar Hohmann reference","not mission validation","not physical test"],
 "input_sha":req["input_sha"]
}
raw=json.dumps(out,sort_keys=True,separators=(",",":")).encode()
out["output_sha"]=hashlib.sha256(raw).hexdigest()
pathlib.Path("bridge/artifacts").mkdir(parents=True,exist_ok=True)
pathlib.Path("bridge/artifacts/farm-result.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out))
