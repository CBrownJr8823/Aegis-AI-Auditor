import re
from typing import Any


SEVERITY_WEIGHTS = {
    "Critical": 30,
    "High": 20,
    "Medium": 10,
    "Low": 4,
    "Info": 0,
}


def _line_number(text: str, start_index: int) -> int:
    return text.count("\n", 0, start_index) + 1


def _excerpt(text: str, start_index: int, end_index: int) -> str:
    line_start = text.rfind("\n", 0, start_index) + 1
    line_end = text.find("\n", end_index)
    if line_end == -1:
        line_end = len(text)
    value = text[line_start:line_end].strip()
    return value[:220] if value else "Matched security-sensitive pattern"


def _finding(
    *,
    rule_id: str,
    title: str,
    severity: str,
    category: str,
    framework: str,
    description: str,
    remediation: str,
    text: str,
    match: re.Match[str],
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "title": title,
        "severity": severity,
        "category": category,
        "framework": framework,
        "description": description,
        "remediation": remediation,
        "location": {"line": _line_number(text, match.start())},
        "evidence": _excerpt(text, match.start(), match.end()),
    }


def _first_matches(pattern: str, text: str, flags: int = 0, limit: int = 3) -> list[re.Match[str]]:
    return list(re.finditer(pattern, text, flags))[:limit]


def run_security_scan(target_text: str) -> dict[str, Any]:
    """Run deterministic static security checks against LLM and agent workflow text."""
    if not isinstance(target_text, str) or not target_text.strip():
        raise ValueError("target_text must be a non-empty string")

    findings: list[dict[str, Any]] = []
    text = target_text.strip()

    rules = [
        {
            "pattern": r"(?i)(?:sk|rk|pk)_[a-z0-9]{16,}|(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']",
            "rule_id": "AEGIS-LLM-001",
            "title": "Potential hardcoded credential",
            "severity": "Critical",
            "category": "Sensitive Information Disclosure",
            "framework": "OWASP LLM06 / NIST AI RMF GOVERN",
            "description": "A likely API key, token, or secret appears directly in source text. Embedded credentials can be exposed through repositories, logs, prompts, and client-side bundles.",
            "remediation": "Move secrets to a managed secret store or environment variables, rotate the exposed credential, and add secret scanning to CI.",
        },
        {
            "pattern": r"(?i)(?:system_prompt|system_message|SYSTEM_PROMPT)\s*[:=]\s*[\"'][\s\S]{20,}?[\"']",
            "rule_id": "AEGIS-LLM-002",
            "title": "System prompt embedded in application code",
            "severity": "Medium",
            "category": "System Prompt Leakage",
            "framework": "OWASP LLM07 / NIST AI RMF MAP",
            "description": "A lengthy system instruction is embedded directly in the target. This increases the chance that privileged behavior, operational policies, or sensitive workflow instructions are disclosed.",
            "remediation": "Keep privileged instructions server-side, minimize sensitive business logic in prompts, and enforce authorization independently of model output.",
        },
        {
            "pattern": r"(?<![\w.])eval\s*\(",
            "rule_id": "AEGIS-LLM-003",
            "title": "Dangerous eval() execution",
            "severity": "Critical",
            "category": "Insecure Output Handling",
            "framework": "OWASP LLM02 / NIST AI RMF MANAGE",
            "description": "eval() can execute attacker-controlled expressions when its input is influenced by a model, user, retrieved document, or tool response.",
            "remediation": "Remove eval(). Use strict schemas, allow-listed operations, safe parsers such as json.loads(), and server-side validation before execution.",
        },
        {
            "pattern": r"(?i)(?:exec\s*\(|subprocess\.(?:run|call|Popen)\s*\(|os\.system\s*\()",
            "rule_id": "AEGIS-LLM-004",
            "title": "Potential unrestricted command execution",
            "severity": "High",
            "category": "Excessive Agency",
            "framework": "OWASP LLM08 / NIST AI RMF MANAGE",
            "description": "The workflow appears able to execute code or operating-system commands. Agent-controlled parameters may produce unsafe actions or command injection.",
            "remediation": "Use a constrained tool gateway, explicit allow-lists, structured parameters, least-privilege service accounts, approval gates, and immutable audit logs.",
        },
        {
            "pattern": r"(?i)(ignore\s+(?:all\s+)?previous\s+instructions|disregard\s+(?:all\s+)?previous\s+instructions|reveal\s+(?:the\s+)?system\s+prompt|jailbreak|developer\s+message)",
            "rule_id": "AEGIS-LLM-005",
            "title": "Prompt-injection indicator",
            "severity": "High",
            "category": "Prompt Injection",
            "framework": "OWASP LLM01 / NIST AI RMF MEASURE",
            "description": "The input contains a known prompt-injection phrase. Untrusted instructions can redirect agents, exfiltrate context, or trigger unauthorized tool calls.",
            "remediation": "Separate trusted system instructions from untrusted content, label data provenance, constrain tool permissions, validate tool arguments, and test with adversarial prompt suites.",
        },
        {
            "pattern": r"(?i)(?:requests\.(?:get|post|request)\s*\([^\n]{0,300}(?:user_input|prompt|query|message)|fetch\s*\([^\n]{0,300}(?:userInput|prompt|query|message))",
            "rule_id": "AEGIS-LLM-006",
            "title": "User-controlled outbound request risk",
            "severity": "High",
            "category": "SSRF and Tool Abuse",
            "framework": "OWASP LLM05 / NIST AI RMF MANAGE",
            "description": "A user- or prompt-derived value may be used to initiate a network request. This can enable SSRF, internal service access, or ungoverned data egress.",
            "remediation": "Validate URLs against an allow-list, block private and link-local address ranges, enforce egress controls, use short timeouts, and log all tool invocations.",
        },
        {
            "pattern": r"(?i)(?:temperature\s*[:=]\s*(?:1(?:\.0+)?|[1-9]\d*\.?\d*)|do\s+not\s+validate|disable\s+(?:guardrails|moderation|validation))",
            "rule_id": "AEGIS-LLM-007",
            "title": "Weak model safety configuration",
            "severity": "Medium",
            "category": "Model Misconfiguration",
            "framework": "OWASP LLM09 / NIST AI RMF GOVERN",
            "description": "The target suggests elevated generation randomness or disabled validation controls in a security-sensitive workflow.",
            "remediation": "Apply task-appropriate deterministic settings, enforce schema validation, introduce policy checks, and monitor unsafe-output and tool-call failure rates.",
        },
        {
            "pattern": r"(?i)(?:retrieve|retriever|vectorstore|similarity_search|rag)[\s\S]{0,180}(?:prompt|context)[\s\S]{0,180}(?:llm|model|chat)",
            "rule_id": "AEGIS-LLM-008",
            "title": "RAG context trust boundary requires review",
            "severity": "Low",
            "category": "Training Data and Retrieval Poisoning",
            "framework": "OWASP LLM03 / NIST AI RMF MAP",
            "description": "The target appears to pass retrieved content into an LLM context. Retrieved text may contain malicious instructions or untrusted data.",
            "remediation": "Track document provenance, sanitize retrieved content, isolate it with clear delimiters, apply content filtering, and prevent retrieved text from authorizing actions.",
        },
    ]

    for rule in rules:
        for match in _first_matches(rule["pattern"], text, re.IGNORECASE | re.MULTILINE):
            findings.append(
                _finding(
                    rule_id=rule["rule_id"],
                    title=rule["title"],
                    severity=rule["severity"],
                    category=rule["category"],
                    framework=rule["framework"],
                    description=rule["description"],
                    remediation=rule["remediation"],
                    text=text,
                    match=match,
                )
            )

    score = min(100, sum(SEVERITY_WEIGHTS[item["severity"]] for item in findings))
    if score >= 50:
        risk_level = "High"
    elif score >= 15:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    severity_breakdown = {
        severity: sum(1 for item in findings if item["severity"] == severity)
        for severity in ("Critical", "High", "Medium", "Low")
    }

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "summary": {
            "total_findings": len(findings),
            "severity_breakdown": severity_breakdown,
            "frameworks": ["OWASP Top 10 for LLM Applications", "NIST AI RMF"],
        },
        "findings": findings,
        "recommendation": (
            "Block deployment until critical findings are remediated and validate agent tools with least-privilege controls."
            if risk_level == "High"
            else "Address identified controls before production rollout and add this scan to your CI/CD security gate."
        ),
    }
