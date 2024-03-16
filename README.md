$$P\left(D\|G_{i}\right)$$ 

is the probability of disease prevelance on the genotype 

$$G_{i}$$

$$P\left(D\right)=\sum_{n=1}^3 P\left(D\|G_{i}\right)P\left(G_{i}\right)$$

$$OR_{i}=\frac{X_{i}\left(1-X_{1}\right)}{X_{1}\left(1-X_{i}\right)}$$

$$P\left(D\right)=X_{1}P\left(G_{1}\right)+\frac{X_{1}OR_{2}}{1-X_{1}+X_{1}OR_{2}}P\left(G_{2}\right)+\frac{X_{1}OR_{3}}{1-X_{1}+X_{1}OR_{3}}P\left(G_{3}\right)$$

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
