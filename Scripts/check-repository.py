#!/usr/bin/env python3
"""Check AEGIS links, screenshot integrity, excluded artifacts and secret patterns."""

import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {
    '.key', '.pem', '.pfx', '.p12', '.ppk', '.kdbx', '.keystore', '.jks',
    '.iso', '.vdi', '.vmdk', '.vbox', '.vbox-prev', '.ova', '.ovf', '.sav',
    '.pcap', '.pcapng', '.evtx', '.har', '.log',
}
FORBIDDEN_NAMES = {'id_rsa', 'id_ed25519', 'id_ecdsa', 'client.keys', 'config.xml'}
SECRET_PATTERNS = {
    'private key': re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED |DSA )?PRIVATE KEY-----'),
    'GitHub token': re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b'),
    'API secret': re.compile(rb'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b'),
    'AWS access key': re.compile(rb'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'credential URL': re.compile(rb'https?://[^\s/:]+:[^\s/@]+@'),
    'literal credential': re.compile(
        rb'''(?im)^\s*(?:password|passwd|api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*["']?([A-Za-z0-9_+/=.!@#$%-]{8,})'''
    ),
}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def secret_findings(data, label):
    findings = []
    if b'\0' in data:
        return findings
    for kind, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(data):
            if kind == 'literal credential' and match.group(1).lower() in {
                b'placeholder', b'changeme', b'redacted', b'example-value',
            }:
                continue
            line = data[:match.start()].count(b'\n') + 1
            findings.append(f'{label}:{line}: possible {kind} (value withheld)')
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--history', action='store_true', help='also inspect reachable historical text blobs')
    args = parser.parse_args()
    names = git('ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')
    paths = sorted({ROOT / name for name in names if name and (ROOT / name).is_file()})
    errors = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        lower = path.name.lower()
        if (path.suffix.lower() in FORBIDDEN_SUFFIXES or lower in FORBIDDEN_NAMES
                or (lower.startswith('.env') and lower != '.env.example')
                or any(part.lower() in {'secrets', 'credentials', 'private', 'auth'} for part in path.relative_to(ROOT).parts)):
            errors.append(f'{rel}: excluded artifact type')
        data = path.read_bytes()
        errors.extend(secret_findings(data, rel))
        if path.suffix == '.md':
            text = data.decode('utf-8-sig')
            for target in re.findall(r'!?\[[^\]]*\]\(([^)\n]+)\)', text):
                target = target.strip().strip('<>')
                parsed = urlsplit(target)
                if parsed.scheme or not parsed.path:
                    continue
                linked = (path.parent / unquote(parsed.path)).resolve()
                if not linked.is_relative_to(ROOT) or not linked.exists():
                    errors.append(f'{rel}: missing or out-of-repository link: {target}')

    manifest = ROOT / 'Screenshots' / 'SHA256SUMS.txt'
    images = {p.name: p for p in paths if p.parent == ROOT / 'Screenshots' and p.suffix == '.png'}
    expected_names = set()
    seen_hashes = {}
    if not manifest.exists():
        errors.append('Screenshots/SHA256SUMS.txt: missing manifest')
    else:
        for row in manifest.read_text(encoding='utf-8').splitlines():
            if not row.strip():
                continue
            match = re.fullmatch(r'([a-f0-9]{64})  ([^/\\]+\.png)', row)
            if not match:
                errors.append('Screenshots/SHA256SUMS.txt: invalid manifest row')
                continue
            expected, name = match.groups()
            if name in expected_names:
                errors.append(f'{name}: duplicate manifest entry')
            expected_names.add(name)
            if name not in images:
                errors.append(f'{name}: manifest image missing')
                continue
            actual = hashlib.sha256(images[name].read_bytes()).hexdigest()
            if actual != expected:
                errors.append(f'{name}: checksum mismatch')
            if actual in seen_hashes:
                errors.append(f'{name}: duplicate image of {seen_hashes[actual]}')
            seen_hashes[actual] = name
        if set(images) != expected_names:
            errors.append('Screenshot files and manifest entries differ')

    historical_count = 0
    if args.history:
        object_rows = git('rev-list', '--objects', '--all').decode().splitlines()
        for row in object_rows:
            oid, _, name = row.partition(' ')
            if not name:
                continue
            if git('cat-file', '-t', oid).strip() != b'blob':
                continue
            historical_data = git('cat-file', 'blob', oid)
            if b'\0' in historical_data:
                continue
            historical_count += 1
            errors.extend(secret_findings(historical_data, f'history {oid[:12]} {name}'))

    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: {len(paths)} repository files; local links; {len(images)} screenshot hashes; no duplicate images or common secret-pattern findings.')
    if args.history:
        print(f'PASS: {historical_count} reachable historical text blobs checked for common secret patterns.')
    print('Scope: static repository hygiene; not live lab validation or exhaustive secret detection.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
