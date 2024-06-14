# lattice_l1

## Setup
Gotta have sage installed currently

## Install some python dependency in sage
```bash
sage -pip install pytest
```

## Run plot for all numbers in the spectrum from -q/2 to q/2 as error_vectors (everything above)
```bash
sage simulate_with_negative.py 
```

## Run plot for whole band 0-q
```bash
sage simulate_whole_band.py
```

## Plot
```bash
sage src/analysis/plot_stats.py csv_name.csv destination_plot_name
```
##

## Run Tests
```bash
sage -python -m pytest
```

## If you want to call the tests directly for me for some reason had issues
```bash
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