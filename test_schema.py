#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = subprocess.run([sys.executable, str(HERE / 'miapi.py'), '--self-test', '--compact'], capture_output=True, text=True, check=True)
r = json.loads(p.stdout)
assert r['schema'] == 'desarrollamo.miapi.v1'
assert r['self_test'] is True
assert r['request']['header_values_recorded'] is False
print('MiAPI schema OK')
