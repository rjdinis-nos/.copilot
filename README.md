# GitHub Copilot Customizations

A collection of custom agents, prompts, and instructions to supercharge your GitHub Copilot experience in VS Code.

## Features

This repository contains reusable Copilot customizations to enhance your development workflow:

- **Custom Agents**: Specialized agents for project initialization and setup
- **Instructions**: Best practices and coding standards for various languages

## Available Customizations

| Type | Title | Description |
|------|-------|-------------|
| Agent | [UV Python Init](customizations/agents/uv_python_init.agent.md) | Creates a new Python project structure with best practices and essential files |
| Instruction | [Python](customizations/instructions/python.instructions.md) | Python coding conventions and guidelines |
| Prompt | [Security Review](customizations/prompts/security_review.prompt.md) | Security review prompt for code analysis focusing on OWASP Top 10 vulnerabilities. Scans code for input validation issues, authentication flaws, hardcoded secrets, injection risks, weak cryptography, error handling problems, and vulnerable dependencies while providing line-specific vulnerability reports with risk severity levels and secure code fixes. |

## License

See [LICENSE](LICENSE) for details.

## 🔗 Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [Custom Instructions Guide](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

