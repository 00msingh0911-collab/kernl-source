#!/usr/bin/env python3
"""Add an IPA release to the SideStore/AltStore source (apps.json).

Usage: update_source.py <ipa_path> <download_url> [release_notes_file]
"""
import datetime
import json
import os
import plistlib
import re
import sys
import zipfile

SOURCE = "apps.json"

ipa_path, download_url = sys.argv[1], sys.argv[2]
notes = ""
if len(sys.argv) > 3 and os.path.exists(sys.argv[3]):
    notes = open(sys.argv[3], encoding="utf-8").read().strip()

with zipfile.ZipFile(ipa_path) as z:
    plist_name = next(n for n in z.namelist() if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", n))
    info = plistlib.loads(z.read(plist_name))

bundle_id = info["CFBundleIdentifier"]
version = info.get("CFBundleShortVersionString", "1.0")
build = info.get("CFBundleVersion", version)
min_os = info.get("MinimumOSVersion", "14.0")
name = info.get("CFBundleDisplayName") or info.get("CFBundleName")

with open(SOURCE, encoding="utf-8") as f:
    source = json.load(f)

app = next((a for a in source["apps"] if a["bundleIdentifier"] == bundle_id), None)
if app is None:
    app = source["apps"][0]
    app["bundleIdentifier"] = bundle_id
if name and app.get("name") in (None, "", "APP_NAME"):
    app["name"] = name

entry = {
    "version": version,
    "buildVersion": str(build),
    "date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "localizedDescription": notes or f"Version {version}",
    "downloadURL": download_url,
    "size": os.path.getsize(ipa_path),
    "minOSVersion": min_os,
}
versions = [v for v in app.get("versions", []) if not (v["version"] == version and v.get("buildVersion") == entry["buildVersion"])]
app["versions"] = [entry] + versions

with open(SOURCE, "w", encoding="utf-8") as f:
    json.dump(source, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Added {bundle_id} {version} ({build}), {entry['size']} bytes, iOS {min_os}+")
