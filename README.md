# kernl source

SideStore / AltStore source for **kernl**.

## Install

In SideStore, go to **Sources → +** and add:

```
https://raw.githubusercontent.com/00msingh0911-collab/kernl-source/main/apps.json
```

## Releasing a new version

1. Bump the version in Xcode and build the IPA.
2. Either:
   - create a GitHub Release here (tag like `v1.1`), attach the `.ipa`, write release notes and publish, or
   - upload the `.ipa` into the `ipa/` folder (e.g. `ipa/kernl-1.1.ipa`) on `main`; the commit description becomes the release notes.
3. The **Update SideStore source** workflow reads the IPA's Info.plist and adds the version to `apps.json` automatically.

If the workflow doesn't run, trigger it manually from the Actions tab with the release tag.
