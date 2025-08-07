# AML Transaction Flagger 🛡

This Python project automatically detects and flags suspicious financial transactions using:

- Client risk levels
- High transaction amounts
- Offshore/risky countries

## Features
- SQLite database integration
- Dynamic rule-based detection
- CSV export for audit/reporting

## Tech Stack
- Python
- SQLite

## Sample Output
```python
(1, 'Ali Rehman', 15000.0, 'Panama', 'Yes', 'Client Risk, Risky Country, High Amount')
