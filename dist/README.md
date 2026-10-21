# AI Bootstrap 2.1.0 – Downloads

Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref fffd4ad17ae62f981e0c8a338f656223ffb4e280`.

| Datei | Zweck | SHA-256 |
| --- | --- | --- |
| [`START_HIER.md`](START_HIER.md) | in einen neuen ChatGPT- oder Claude-Chat hochladen oder einfügen, dann „Start“ | `ad5dc55701e4dc39a20bcb51303022ac4daa4df94748cd894b1bd0993478fc2d` |
| [`AI-Bootstrap-2.1.0.zip`](AI-Bootstrap-2.1.0.zip) | vollständiges Paket; wird im Schritt `handover` entpackt | `d83fa387da9e8cd4d124bd95a16159e35d04f59dd4d424afbe215649acb599e1` |
| [`SHA256SUMS`](SHA256SUMS) | Prüfsummen beider Dateien | – |

Quellstand: `fffd4ad17ae62f981e0c8a338f656223ffb4e280` (steht auch in `START_HIER.md` und im `BUNDLE_MANIFEST.json` des ZIP). Spätere Commits auf diesem Branch ändern nur `dist/` und `docs/`, nicht den Paketinhalt.

Status: **PACKAGE_BUILT**, nicht freigegeben. Real geprüft sind nur Teile der beiden Linux-Wege; siehe `docs/results/GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`. Kein Release, kein Tag.
