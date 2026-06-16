# Contributing to Aji OS

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

## Development Setup

See [SETUP.md](./SETUP.md) for complete instructions.

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Format with `black`
- Lint with `flake8`

```bash
cd backend
black .
flake8 .
```

### JavaScript/React (Frontend)
- Use ESLint
- Format with Prettier
- Follow React best practices

```bash
cd frontend
npm run lint
```

## Creating Plugins

Plugins provide extensible functionality:

```python
# backend/plugins/example.py
from typing import Dict, Any

class ExamplePlugin:
    NAME = "example"
    DESCRIPTION = "Example plugin"
    TRIGGERS = ["command", "trigger"]
    
    @staticmethod
    async def execute(command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute plugin command
        
        Args:
            command: User command
            args: Command arguments
            
        Returns:
            Result dict with status and data
        """
        try:
            # Implementation
            return {
                "status": "success",
                "message": "Command executed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
```

Plugin guidelines:
1. Inherit from PluginBase or follow the interface
2. Define NAME, DESCRIPTION, TRIGGERS
3. Implement async execute method
4. Return consistent result format
5. Handle errors gracefully
6. Add docstrings

## Adding React Components

```javascript
// frontend/src/components/MyComponent.jsx
import React from 'react'

function MyComponent(props) {
  return (
    <div className="...">
      {/* Component content */}
    </div>
  )
}

export default MyComponent
```

Best practices:
1. Functional components with hooks
2. Use Tailwind CSS for styling
3. Leverage useStore for state
4. Add PropTypes for validation
5. Write clear JSDoc comments

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

- Update README.md for major features
- Add docstrings to all functions
- Include usage examples
- Document API endpoints

## Commit Messages

```
Type: Brief description

Optional longer explanation if needed.

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
```
feat: Add weather plugin
fix: Resolve voice recognition timeout
docs: Update API documentation
```

## Pull Request Process

1. Update README.md with any new features
2. Update requirements.txt or package.json if dependencies added
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback
6. Merge when approved

## Reporting Issues

When reporting bugs:
1. Describe the issue clearly
2. Include steps to reproduce
3. Provide system information (OS, Python version, etc.)
4. Include error logs
5. Suggest a fix if possible

## Feature Requests

1. Describe the feature
2. Explain the use case
3. Consider implementation approach
4. Discuss with maintainers before coding

## Code Review

We review all contributions for:
- Code quality and style
- Security and performance
- Documentation
- Test coverage
- Alignment with project goals

## License

By contributing, you agree that your code will be licensed under the MIT License.

## Questions?

Open a discussion or issue on GitHub!
