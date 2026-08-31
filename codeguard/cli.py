"""
CodeGuard CLI — entry point.
 
Usage:
    codeguard scan <path>            Scan a file or folder
    codeguard scan <path> --explain  Also add AI-generated explanations
    codeguard scan <path> --json     Output findings as JSON
"""
 
import argparse
import json
import sys
 
from .scanner import scan_path
from .explainer import explain
 
SEVERITY_COLOR = {
    "high": "\033[91m",   # red
    "medium": "\033[93m", # yellow
    "low": "\033[94m",    # blue
    "info": "\033[90m",   # gray
}
RESET = "\033[0m"
BOLD = "\033[1m"
 
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}
 
 
def print_report(findings, use_explain: bool):
    if not findings:
        print(f"{BOLD}CodeGuard{RESET}: no issues found. ✅ (or use --explain / -v for more detail)")
        return
 
    findings = sorted(findings, key=lambda f: SEVERITY_ORDER.get(f.severity, 9))
 
    counts = {"high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
 
    print(f"\n{BOLD}CodeGuard scan results{RESET}")
    print(f"  {SEVERITY_COLOR['high']}{counts['high']} high{RESET}  "
          f"{SEVERITY_COLOR['medium']}{counts['medium']} medium{RESET}  "
          f"{SEVERITY_COLOR['low']}{counts['low']} low{RESET}\n")
 
    for f in findings:
        color = SEVERITY_COLOR.get(f.severity, "")
        print(f"{color}[{f.severity.upper()}]{RESET} {BOLD}{f.title}{RESET}")
        print(f"  {f.file}:{f.line_number}")
        if f.line_text:
            print(f"  > {f.line_text}")
        explanation = explain(f) if use_explain else f.why
        print(f"  Why: {explanation}")
        print(f"  Fix: {f.fix}\n")
 
 
def print_json(findings):
    output = [
        {
            "file": f.file,
            "line": f.line_number,
            "rule_id": f.rule_id,
            "severity": f.severity,
            "title": f.title,
            "why": f.why,
            "fix": f.fix,
        }
        for f in findings
    ]
    print(json.dumps(output, indent=2))
 
 
def main():
    parser = argparse.ArgumentParser(prog="codeguard", description="Local security scanner for AI-generated code.")
    subparsers = parser.add_subparsers(dest="command", required=True)
 
    scan_parser = subparsers.add_parser("scan", help="Scan a file or folder")
    scan_parser.add_argument("path", help="File or folder to scan")
    scan_parser.add_argument("--explain", action="store_true", help="Use AI to explain findings in plain language (requires ANTHROPIC_API_KEY)")
    scan_parser.add_argument("--json", action="store_true", help="Output findings as JSON instead of a terminal report")
 
    args = parser.parse_args()
 
    if args.command == "scan":
        try:
            findings = scan_path(args.path)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
 
        if args.json:
            print_json(findings)
        else:
            print_report(findings, use_explain=args.explain)
 
        # Exit code reflects severity, useful for CI use later
        if any(f.severity == "high" for f in findings):
            sys.exit(2)
        elif findings:
            sys.exit(1)
        else:
            sys.exit(0)
 
 
if __name__ == "__main__":
    main()
 