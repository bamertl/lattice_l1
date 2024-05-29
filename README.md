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

## Random Linear Code creation plus trying to decode the random code via lattice attack 
```bash
sage main.py
``` 

## Install some python dependency in sage
```bash
sage -pip install pytest
```

## Run Tests
```bash
sage -python -m pytest
```

## If you want to call the tests directly for me for some reason had issues
```bash
export PYTHONPATH="/home/lub/Projects/lattice_l1/src:$PYTHONPATH"
sage tests/test_num_error_vector.py 
```

##



## Update Requirements
```bash
pip freeze > requirements.txt
```