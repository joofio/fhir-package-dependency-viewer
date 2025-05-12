#!/usr/bin/env python3
import json
from datetime import datetime

import requests

# Step 1: Download
url = "https://fhir.org/guides/stats2/registry.json"
response = requests.get(url)
raw = response.json()
packages = raw["packages"]

# Step 2: Extract simplified data
output = []
existing_ids = set()
dep_ids = set()

for key, val in packages.items():
    if "#" not in key:
        continue
    name, version = key.split("#")
    deps = val.get("dependencies", {})
    dep_list = [f"{dep}#{v}" for dep, v in deps.items()]
    output.append(
        {"id": key, "name": name, "version": version, "dependencies": dep_list}
    )
    existing_ids.add(key)
    dep_ids.update(dep_list)

# Step 3: Add missing dependencies as nodes with no deps
missing_dep_ids = dep_ids - existing_ids
for dep_id in sorted(missing_dep_ids):
    if "#" in dep_id:
        name, version = dep_id.split("#")
        output.append(
            {"id": dep_id, "name": name, "version": version, "dependencies": []}
        )

# Step 4: Add timestamp
output_data = {"created": datetime.now().isoformat(), "packages": output}

# Step 5: Save to file
with open("slim_fhir_graph.json", "w") as f:
    json.dump(output_data, f, indent=2)
