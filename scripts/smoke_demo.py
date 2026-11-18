#!/usr/bin/env python3
"""Run the documented launch for one full cycle and validate its console output."""
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile


def main():
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryFile(mode='w+') as log:
        process = subprocess.Popen(
            ['bash', 'scripts/demo.sh'], cwd=root, stdout=log,
            stderr=subprocess.STDOUT, start_new_session=True)
        try:
            process.wait(timeout=27)
            raise RuntimeError('The demo ended before the full cycle')
        except subprocess.TimeoutExpired:
            pass
        finally:
            if process.poll() is None:
                # Signal launch once; it forwards SIGINT to its child nodes.
                process.send_signal(signal.SIGINT)
                try:
                    process.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
        log.seek(0)
        output = log.read()
    expected = [
        ('CLEAR', '5.00', '1.00'),
        ('SLOWDOWN', '2.00', '0.50'),
        ('STOP', '0.70', '0.00'),
        ('INVALID_INPUT', '-1.00', '0.00'),
    ]
    errors = []
    for state, clearance, velocity in expected:
        pattern = (rf'\b{state}\s+\| clearance={re.escape(clearance)} m'
                   rf' \| goal_vx=1\.00 \| cmd_vx={re.escape(velocity)}')
        if not re.search(pattern, output):
            errors.append(f'Missing {state}: clearance={clearance}, cmd_vx={velocity}')
    if 'Traceback (most recent call last)' in output or 'process has died' in output:
        errors.append('A node failed')
    if output.count('process has finished cleanly') != 4:
        errors.append('The four nodes did not shut down cleanly')
    if errors:
        print(output)
        raise RuntimeError('; '.join(errors))
    print('PASS: complete launch, CLEAR → SLOWDOWN → STOP → INVALID_INPUT, clean shutdown')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
