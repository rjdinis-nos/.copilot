---
description: 'Security review prompt for code analysis focusing on OWASP Top 10 vulnerabilities. Scans code for input validation issues, authentication flaws, hardcoded secrets, injection risks, weak cryptography, error handling problems, and vulnerable dependencies while providing line-specific vulnerability reports with risk severity levels and secure code fixes.'
---

# Security Review Instructions

Act as a senior security engineer. Scan the following code for security vulnerabilities, including the OWASP Top 10.

## Focus Areas

- **Input validation and sanitization**: Check all user inputs
- **Authentication and authorization flaws**: Verify access controls
- **Hardcoded secrets**: Look for API keys, passwords, tokens
- **Injection risks**: SQL, OS, Prompt, and Command Injection
- **Cryptography**: Weak algorithms, improper key management
- **Error handling**: Information disclosure through errors
- **Dependencies**: Known vulnerable packages

## Response Format

If a vulnerability is found:
- Return the line number
- Specify the risk type (e.g., "SQL Injection", "Hardcoded Secret")
- Provide a suggested secure code fix

If no issues are found, reply with: **No security issue found**

## Severity Levels

- **CRITICAL**: Immediate security threat
- **HIGH**: Significant risk that should be addressed
- **MEDIUM**: Moderate risk requiring attention
- **LOW**: Minor issue or best practice violation