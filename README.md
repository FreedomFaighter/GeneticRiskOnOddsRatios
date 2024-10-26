Non-disclosure agreement was never signed by Vitagene and returned to the developer

October 2015 work with Vitagene is the basis for this solution, which, at the time was based on genetics at the allelle level from consumer DNA testing from Ancestry and 23andMe and would only include a single DNA pair in the probability analysis

This extents to actually formulating an open form of the Logistic regression equation solvable by a root seeking algorithm as previously used in the third degree form

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
