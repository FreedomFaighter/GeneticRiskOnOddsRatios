Pooled-Odds-Ratio
=================

1. Installation
---------------
Create a virtual environment:
```
virtualenv -p python2.7 venv
```

Activate it:
```
source venv/bin/activate
```

Install requirements from the file:
```
pip linstall -r requirements.txt
```

Exit:
```
deactivate
```

2. Running
----------
Activate environment:
```
source venv/bin/activate
```

Run the script:
```
python geneticPooledOdds.py {ID} {FILE_NAME.txt} {AGE} {SEX} {Excel File with Odds Ratio Information}
```

Example:
```
python geneticPooledOdds.py 5 myfile.txt 18 Female Prevelance_of_Disease.xlsx
```

Exit virtual environment:
```
deactivate
```
