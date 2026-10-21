# AI Bootstrap 2.1.0 – Downloads

Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref 91c305b753adb9ff2b0a659f2e8232259add2a74`.

| Datei | Zweck | SHA-256 |
| --- | --- | --- |
| [`START_HIER.md`](START_HIER.md) | in einen neuen ChatGPT- oder Claude-Chat hochladen oder einfügen, dann „Start“ | `d7e552795bd2be1d4395ee5e467e430953d7526376e2874f8a65282fa9889d16` |
| [`AI-Bootstrap-2.1.0.zip`](AI-Bootstrap-2.1.0.zip) | vollständiges Paket; wird im Schritt `handover` entpackt | `8282fd7b4bc5f987a505034a757bfd9e35d7b67dae8f8af5b233b4195fe9173b` |
| [`SHA256SUMS`](SHA256SUMS) | Prüfsummen beider Dateien | – |

Quellstand: `91c305b753adb9ff2b0a659f2e8232259add2a74` (steht auch in `START_HIER.md` und im `BUNDLE_MANIFEST.json` des ZIP). Spätere Commits auf diesem Branch ändern nur `dist/` und `docs/`, nicht den Paketinhalt.

Status: **PACKAGE_BUILT**, nicht freigegeben. Real geprüft sind nur Teile der beiden Linux-Wege; siehe `docs/results/GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`. Kein Release, kein Tag.
