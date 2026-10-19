#!/usr/bin/env python3
"""Read-only probe: can the dev-box merge gate run on this computer?

Usage::

    python3 scripts/probe_gate_host.py [--config <gate.toml>]

Runs the gate's platform preflight and its host resource probe with the given
configuration (default: the example configuration with ``systemd_scope``
switched off). Prints the platform, the preflight result and the measured
memory, swap and heavy-process count. Changes nothing, needs no network, no
GitHub access and no repository. Exit 0: the gate's host checks work here.
Exit 10: platform precondition missing. Exit 40: host probe failed.
"""

from __future__ import annotations

import argparse
import importlib.util
import platform
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / "templates" / "devbox_merge_gate.py"
EXAMPLE = ROOT / "templates" / "devbox_merge_gate.example.toml"


def load_gate():
    spec = importlib.util.spec_from_file_location("devbox_merge_gate", GATE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["devbox_merge_gate"] = module
    spec.loader.exec_module(module)
    return module


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path)
    args = parser.parse_args(argv)
    gate = load_gate()
    print(f"python {platform.python_version()} on {platform.platform()}")
    print(f"gate platform: {gate.host_platform()}")
    with tempfile.TemporaryDirectory() as tmp:
        path = args.config
        if path is None:
            path = Path(tmp) / "probe.toml"
            text = EXAMPLE.read_text(encoding="utf-8")
            path.write_text(
                text.replace("systemd_scope = true", "systemd_scope = false", 1),
                encoding="utf-8",
            )
        config = gate.load_config(path)
        try:
            gate.platform_preflight(config)
            print("preflight: ok")
            snapshot = gate.LocalHost(config).resources()
        except gate.GateStop as stop:
            print(f"STOP {stop.code.name}: {stop.message}")
            return int(stop.code)
    print(
        f"memory available: {snapshot.mem_available_kib // 1024} MiB, "
        f"swap free: {snapshot.swap_free_kib // 1024} MiB, "
        f"heavy processes: {len(snapshot.heavy_processes)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
