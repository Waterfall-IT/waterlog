# waterlog

## Installation
```bash
pip install git+https://github.com/Waterfall-IT/waterlog.git
```

## Usage
```python
from waterlog import Logger, LogLevel
logger = Logger('logs/my_app.log', LogLevel.DEBUG)
logger.info('Logger loaded successfully!')
```