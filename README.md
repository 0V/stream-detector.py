# stream-detector.py
Simple detector for streaming and recording for **Windows**.  
It can detect that a display recorder such as **OBS Studio** or **XSplit** is running.
```python
from streamdetector import StreamDetector

detector = StreamDetector()
print('record? -> %s' % detector.is_record())
```
