Model was developed circa November 2015 based on the presentation of genetic analysis collected during disease studies

$$P\left(D\|G_{i}\right)$$ 

is the probability of disease prevelance on the genotype 

$$G_{i}$$

$$P\left(D\right)=\sum_{n=1}^3 P\left(D\|G_{i}\right)P\left(G_{i}\right)$$

$$OR_{i}=\frac{X_{i}\left(1-X_{1}\right)}{X_{1}\left(1-X_{i}\right)}$$

$$P\left(D\right)=X_{1}P\left(G_{1}\right)+\frac{X_{1}OR_{2}}{1-X_{1}+X_{1}OR_{2}}P\left(G_{2}\right)+\frac{X_{1}OR_{3}}{1-X_{1}+X_{1}OR_{3}}P\left(G_{3}\right)$$

The other side would be treatments such as various forms of Therapy or Exercise that reduce the odds ratio where the odds ratios presented during the statistical analysis were in the range of (0,1) which would reduce the respective odds of contracting or experiencing such an illness

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
