$$P\left(D\|G_{i}\right)$$ 

is the probability of disease prevelance on the genotype 

$$G_{i}$$

$$P\left(D\right)=\sum_{n=1}^3 P\left(D\|G_{i}\right)P\left(G_{i}\right)$$

$$OR_{i}=\frac{X_{i}\left(1-X_{1}\right)}{X_{1}\left(1-X_{i}\right)}$$

$$P\left(D\right)=XP\left(G_{1}\right)+\frac{XOR_{2}}{1-X+XOR_{2}}P\left(G_{2}\right)+\frac{XOR_{3}}{1-X+XOR_{3}}P\left(G_{3}\right)$$

Or, generally describing

$$P\left(D\right)=\sum_{o=1}^{\inf}{\frac{XOR_{o}}{1-X+XOR_{o}}P\left(G_{o}\right)}$$

$$\sum_{o=1}^{∞}{\frac{XOR_{o}}{1-X+XOR_{o}}P\left(G_{o}\right)}-P\left(D\right)=0$$

$$\sum_{o=1}^{∞}{\frac{XOR_{o}}{1-X+XOR_{o}}P\left(G_{o}\right)}=P\left(D\right)$$

A stochastic model might be describe with a distribution of each 

$$OR_{o} \in \left(0\lt i\lt ∞ \right)$$

positive only style of distribution constrainted by the definition of odds ratios

$P\left(D\right)\in B\left(\alpha,\beta\right)$ in the style of beta distributions

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
