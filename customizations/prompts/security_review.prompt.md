# Security Review Prompt

Your goal is to identify security vulnerabilities in code, focusing on the OWASP Top 10 and common security issues.

## Input Requirements

Provide the code you want to review, including:
- Programming language
- Context about the application
- Any specific security concerns

## Analysis Focus

### Input Validation & Sanitization
- User input handling
- Data type validation
- Input length and format checks
- Encoding and escaping

### Authentication & Authorization
- Access control implementation
- Session management
- Password handling
- Token validation

### Sensitive Data Exposure
- Hardcoded secrets (API keys, passwords, tokens)
- Encryption at rest and in transit
- Logging of sensitive information
- Configuration management

### Injection Vulnerabilities
- SQL Injection
- Command Injection
- LDAP Injection
- Prompt Injection
- Cross-Site Scripting (XSS)

### Security Misconfiguration
- Default credentials
- Unnecessary features enabled
- Error handling and information disclosure
- Security headers

### Cryptography
- Weak algorithms
- Improper key management
- Insufficient entropy
- Certificate validation

### Dependencies & Components
- Known vulnerable packages
- Outdated libraries
- Supply chain risks

## Output Format

For each vulnerability found, provide:

1. **Line Number**: Specific location in code
2. **Risk Type**: Category (e.g., "SQL Injection", "Hardcoded Secret")
3. **Severity**: CRITICAL / HIGH / MEDIUM / LOW
4. **Description**: Clear explanation of the issue
5. **Secure Code Fix**: Suggested remediation with code example

### Severity Definitions

- **CRITICAL**: Immediate security threat requiring urgent attention
- **HIGH**: Significant risk that should be addressed promptly
- **MEDIUM**: Moderate risk requiring attention in near term
- **LOW**: Minor issue or best practice violation

### Response Template

```
VULNERABILITY FOUND:
Line: [line number]
Type: [vulnerability type]
Severity: [CRITICAL/HIGH/MEDIUM/LOW]

Issue: [description of the problem]

Vulnerable Code:
[code snippet]

Secure Fix:
[corrected code snippet]

Explanation: [why this fix addresses the issue]
```

If **no vulnerabilities** are found, respond with:

```
✓ No security issues found
```

## Best Practices

- Be thorough but concise
- Prioritize high-severity issues
- Provide actionable recommendations
- Consider the specific context and framework
- Reference relevant OWASP guidelines when applicable
