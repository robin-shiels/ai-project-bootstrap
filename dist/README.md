# AI Bootstrap 2.1.0 – Downloads

Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref a13e0737f09b962edb5e643bc43df4fa2aac933d`.

| Datei | Zweck | SHA-256 |
| --- | --- | --- |
| [`START_HIER.md`](START_HIER.md) | in einen neuen ChatGPT- oder Claude-Chat hochladen oder einfügen, dann „Start“ | `6eab59b4a35d48355180518ebf0d12e1399ca43ee4da70c46a73e67a05015853` |
| [`AI-Bootstrap-2.1.0.zip`](AI-Bootstrap-2.1.0.zip) | vollständiges Paket; wird im Schritt `handover` entpackt | `da3816a93dfb554e1e4b0bcc977401f1efa441eddb045119ce682b1785c14e6b` |
| [`SHA256SUMS`](SHA256SUMS) | Prüfsummen beider Dateien | – |

Quellstand: `a13e0737f09b962edb5e643bc43df4fa2aac933d` (steht auch in `START_HIER.md` und im `BUNDLE_MANIFEST.json` des ZIP). Spätere Commits auf diesem Branch ändern nur `dist/` und `docs/`, nicht den Paketinhalt.

Status: **PACKAGE_BUILT**, nicht freigegeben. Real geprüft sind nur Teile der beiden Linux-Wege; siehe `docs/results/GUIDED_BOOTSTRAP_V1_ACCEPTANCE.md`. Kein Release, kein Tag.
