# fixm4b development notes

- Python 3.12+ and Poetry.
- No spaCy/NLTK required.
- Offline tests by default; network OL/GR only when UAs are set.

```bash
poetry install
poetry run pytest
poetry run fixm4b --help
poetry run fixm4b config new
```
