A more complex and statistically valid approach adjusts individual SNP
odds ratios by accounting disease prevalence and is based on a
statistical set of equations (refer to 23andMe White Paper 23-01 \[2\])

In this approach the overall odds ratio is computed by first adjusting
the reported SNP odds ratios and combining them as:

$$Combined\ OR = \ \prod_{i}^{}{adjusted\ {OR}_{i}}$$

To obtain adjusted ORs, we start by solving the following set of
equations for values P(D\|G), or the probability of disease given
genotype:

$$P(D) = \ P\left( D \middle| G_{1} \right)P\left( G_{1} \right) + P\left( D \middle| G_{2} \right)P\left( G_{2} \right) + P\left( D \middle| G_{3} \right)P(G_{3})$$

$$OR_{2} = \frac{\frac{P(D|G_{2})}{(1 - P(D|G_{2}))}}{\frac{P(D|G_{1})}{(1 - P(D|G_{1}))}}$$

$$OR_{3} = \frac{\frac{P(D|G_{3})}{(1 - P(D|G_{3}))}}{\frac{P(D|G_{1})}{(1 - P(D|G_{1}))}}$$

Where, D stands for disease, P(D) is disease prevalence, $G_{1}$, $G_{2}$,
$G_{3}$ are the three SNP genotypes ordered in such a way that G~1~ is a
low-risk homozygote, and $OR_{1}$, $OR_{2}$, $OR_{3}$ are corresponding genotype
odds ratio where $OR_{1} = 1$ by definition. All of these quantities are
known to us, so we can plug them in the above set of three equations to
obtain
$P\left( D \middle| G_{1} \right),\ P\left( D \middle| G_{2} \right),\ P\left( D \middle| G_{3} \right)$,
that is, the probability of the disease given the three genotypes.

To obtain adjusted odds ratios, we use the computed P(D\|G) using the
following equations:

$$adjusted\ OR_{1} = \frac{\frac{P(D|G_{1})}{(1 - P(D|G_{1}))}}{\frac{P(D)}{(1 - P(D))}}$$

$$adjusted\ OR_{2} = \frac{\frac{P(D|G_{2})}{(1 - P(D|G_{2}))}}{\frac{P(D)}{(1 - P(D))}}$$

$$adjusted\ OR_{3} = \frac{\frac{P(D|G_{3})}{(1 - P(D|G_{3}))}}{\frac{P(D)}{(1 - P(D))}}$$

As you can see, the odds ratios are adjusted in a way to be calculated
relative to the average risk of the disease in the population.

This approach takes into account the prevalence of the disease in
adjusting the odds rations. However, this adjustment is really small,
and generally the prevalence of the disease is not evident in the
obtained adjusted OR. In addition, this approach is statistically sound
and accepted by the wider scientific community. For more info on this
approach, please refer to \[2\].

1.  <https://gavinband.wordpress.com/2010/11/03/genotype-counts-odds-ratios-and-models-of-risk/>

2.  <https://23andme.https.internapcdn.net/res/pdf/HIC-SXIYiYqXreldAxO5yA_23-01_Estimating_Genotype_Specific_Incidence.pdf>

3.  <http://courses.washington.edu/b516/lectures_2009/Odds_Ratios.pdf>
