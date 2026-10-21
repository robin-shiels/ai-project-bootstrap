# AI Bootstrap 3.0.0 – Downloads

Gebaut mit `python3 scripts/build_bootstrap_bundle.py --output-dir dist --source-ref 9bc11a4c752d197aa959e55e5bfd34a2c4d5457b`.

| Datei | Zweck | SHA-256 |
| --- | --- | --- |
| [`START_HIER.md`](START_HIER.md) | in der Desktop-App im Bereich Code (Claude) bzw. Codex (ChatGPT) in eine neue Sitzung geben, dann „Start“ | `b9a8ae736b021b85da01ca8cb02602d7a2ec2880b3d38236eaa0662072bf475f` |
| [`AI-Bootstrap-3.0.0.zip`](AI-Bootstrap-3.0.0.zip) | Offline-Kopie mit Plugin, Standard und Vorlagen; normalerweise nicht nötig | `40892b26e0a051335f00fd00562c7e61796db6fd7b24bf61e6d8ea5a70f2bb4b` |
| [`SHA256SUMS`](SHA256SUMS) | Prüfsummen beider Dateien | – |

Quellstand: `9bc11a4c752d197aa959e55e5bfd34a2c4d5457b` (steht auch in `START_HIER.md` und im `BUNDLE_MANIFEST.json` des ZIP). Spätere Commits ändern nur `dist/` und `docs/`, nicht den Paketinhalt.

Status: **PACKAGE_BUILT**, nicht freigegeben. Real geprüft: Linux-Nullzustand; macOS, Windows, Webchat und der Probelauf mit echtem Merge sind offen. Siehe `docs/results/GUIDED_BOOTSTRAP_V2_ACCEPTANCE.md`. Kein Release, kein Tag.
