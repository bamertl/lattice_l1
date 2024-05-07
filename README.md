# lattice_l1

## Setup
```bash
python3 -m venv env
source venv/bin/activate
pip install -r requirements.txt
```
## Testing LLL against Sage
```bash
sage -pip install tqdm
sage sage_main.py
```

## Construction A run normal python file (create venv first)
```bash
sage tester.py
``` 

## Update Requirements
```bash
pip freeze > requirements.txt
```