---
description: Build the package and prepare for PyPI release
---

1. Build the source and wheel distributions:
```bash
uv build
```

2. To publish, create a git tag and push it:
```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```
