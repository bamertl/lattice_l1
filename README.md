# lattice_l1

## Setup
Gotta have sage installed currently

## Install some python dependency in sage
```bash
sage -pip install pytest
```

## Run a simulation
the first part might not be needed but sage for some reason sometimes has a bit an issue (replace the path with your path)
```bash
export PYTHONPATH="/home/lub/Projects/lattice_l1/src:$PYTHONPATH"
sage simulate.py 
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

## Setup (not important atm)
```bash
python3 -m venv env
source venv/bin/activate
pip install -r requirements.txt
```
### Update Requirements (as we work with sage for now unused)
```bash
pip freeze > requirements.txt
```