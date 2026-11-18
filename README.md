# GroundCheck

GroundCheck is a tiny, dependency-free screening tool for a common RAG failure:
answers that contain claims the retrieved passages do not appear to support.
It splits an answer into sentences, finds the closest context for each claim,
and flags low-overlap claims for human review.

> GroundCheck is a transparent lexical baseline, not a semantic entailment,
> factuality, or safety detector. Matching words do not prove a claim is true;
> paraphrases may be flagged even when they are correct. Review flagged claims
> and calibrate the threshold on your own data before using this in production.

## Quick start

Requires Python 3.10 or later.

```bash
python -m pip install -e .
groundcheck examples/input.json
```

Or run it without installing the command:

```bash
PYTHONPATH=src python -m groundcheck.cli examples/input.json
```

Input is a JSON object with an answer and the retrieved context passages:

```json
{
  "answer": "The Apollo 11 mission landed on the Moon in 1969.",
  "contexts": [
    "Apollo 11 first landed humans on the Moon in 1969."
  ]
}
```

Output includes each claim's best overlap score, status, and supporting passage
when the score meets the threshold. Scores use Jaccard overlap over
case-insensitive word tokens after removing a small set of common stop words.
The default threshold is `0.2`; change it with `--threshold`, which accepts
values from `0` to `1`.

## Python API

```python
from groundcheck import check_answer

report = check_answer(
    "The library opened in 1998.",
    ["The public library opened in 1998."],
)
print(report.to_dict())
```

## Development

```bash
python -m pip install -e ".[test]"
python -m pytest
```

## Contributing

Bug reports and focused improvements are welcome. Please include a test for
behavior changes and keep the limitations of lexical matching clear.

## License

MIT. See [LICENSE](LICENSE).
