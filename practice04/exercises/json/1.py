import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

for item in data["imdata"]:
    attr = item["l1PhysIf"]["attributes"]
    dn = attr["dn"]
    descr = attr["descr"]
    speed = attr["speed"]
    mtu = attr["mtu"]

    print(f"{dn:50} {descr:20} {speed:8} {mtu:6}")
