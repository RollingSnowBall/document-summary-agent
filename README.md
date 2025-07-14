# document-summary-agent

This repository provides utilities for parsing financial documents.

## Parsing 10-K Risk Factors

The script `scripts/parse_risk_factors.py` extracts the **Item 1A - Risk Factors** section from a 10-K HTML document. The section is split into paragraph chunks and stored as JSON.

### Usage

```bash
python scripts/parse_risk_factors.py path/to/10k.html output.json
```

Each entry in the resulting JSON array contains:

- `item`: the item name (`"Item 1A - Risk Factors"`)
- `index`: chunk index
- `start_pos`: character offset within the section
- `text`: paragraph text


