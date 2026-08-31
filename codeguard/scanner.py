"""
CodeGuard scanner — the rule engine.
 
Reads source files as plain text (never executes them), matches each
line against a database of known-risky patterns, and returns a list
of findings. No network access and no code execution happen here.
"""
 
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List
 
RULES_PATH = Path(__file__).parent / "rules.json"
 
 
@dataclass
class Finding:
    file: str
    line_number: int
    line_text: str
    rule_id: str
    severity: str
    title: str
    why: str
    fix: str
 
 
def load_rules() -> List[dict]:
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        rules = json.load(f)
    # Pre-compile regex patterns once for speed
    for rule in rules:
        rule["_compiled"] = re.compile(rule["pattern"])
    return rules
 
 
def scan_file(filepath: Path, rules: List[dict]) -> List[Finding]:
    """Scan a single file's text against every rule. Returns findings.
 
    Files that can't be read as text are reported as unreadable rather
    than silently skipped (fail safe, not silent).
    """
    findings = []
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [
            Finding(
                file=str(filepath),
                line_number=0,
                line_text="",
                rule_id="unreadable-file",
                severity="info",
                title="Could not read file",
                why=f"Error: {e}",
                fix="Check file encoding/permissions and re-run the scan.",
            )
        ]
 
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for rule in rules:
            if rule["_compiled"].search(line):
                findings.append(
                    Finding(
                        file=str(filepath),
                        line_number=i,
                        line_text=line.strip(),
                        rule_id=rule["id"],
                        severity=rule["severity"],
                        title=rule["title"],
                        why=rule["why"],
                        fix=rule["fix"],
                    )
                )
    return findings
 
 
def scan_path(path: str) -> List[Finding]:
    """Scan a single file or every file in a folder (recursively).
 
    Only text-like source file extensions are scanned; binaries and
    unrelated files are skipped without being reported as findings.
    """
    rules = load_rules()
    target = Path(path)
    findings: List[Finding] = []
 
    scannable_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".rb", ".php",
        ".go", ".c", ".cpp", ".cs", ".env", ".yml", ".yaml", ".json",
    }
 
    if target.is_file():
        findings.extend(scan_file(target, rules))
    elif target.is_dir():
        for filepath in sorted(target.rglob("*")):
            if filepath.is_file() and filepath.suffix in scannable_extensions:
                findings.extend(scan_file(filepath, rules))
    else:
        raise FileNotFoundError(f"No such file or directory: {path}")
 
    return findings
 