[]{#AlgorithmSpecs.xhtml}

[Algorithm Specs:]{.c4}

[ ]{.c2}

[Supplement recommendation is determined by:]{.c2}

[ ]{.c2}

[Genetics]{.c2}

[Lifestyle questionnaire]{.c2}

[]{.c2}

[Databases Needed:]{.c4}

-   [Prevalence]{.c2}
-   [Online variable (for Pooled OR)]{.c2}
-   Disease genetics  ( [
    [https://docs.google.com/spreadsheets/d/1D3nc2CITd71JmlaGbcHj8yaEcv_ZLvSkr3qT4TkVJS8/edit?usp=sharing](https://www.google.com/url?q=https://docs.google.com/spreadsheets/d/1D3nc2CITd71JmlaGbcHj8yaEcv_ZLvSkr3qT4TkVJS8/edit?usp%3Dsharing&sa=D&source=editors&ust=1712789321007117&usg=AOvVaw0CHJRntoPlX3RljQtstiNA){.c5}
    ]{.c9} [) ]{.c2}

```{=html}
<!-- -->
```
-   [SNP]{.c2}
-   [GeneName]{.c2}
-   [Genotype]{.c2}
-   [DiseaseName]{.c2}
-   [Gender]{.c2}
-   [Ethnicity]{.c2}
-   [OR]{.c2}

```{=html}
<!-- -->
```
-   [Supplement Reference Database]{.c2}

```{=html}
<!-- -->
```
-   [SupplementName]{.c2}
-   [Disease]{.c2}
-   [Dosage]{.c2}
-   [Average Score]{.c2}

```{=html}
<!-- -->
```
-   [Vitagene Supplements]{.c2}

```{=html}
<!-- -->
```
-   [SupplementName]{.c2}
-   [Dosage]{.c2}

```{=html}
<!-- -->
```
-   [Contraindications (will provide later)]{.c2}
-   [Nutrient Depletions (will provide later)]{.c2}

[]{.c2}

[Genetic Module: ]{.c4}

-   [Read user's DNA (SNP/genotype) ]{.c2}

```{=html}
<!-- -->
```
-    available in 2 formats:\
    [
    ![](images/image2.png){style="width: 265.00px; height: 179.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}
    ]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 265.00px; height: 179.00px;"}

```{=html}
<!-- -->
```
-   [
    ![](images/image1.png){style="width: 392.00px; height: 161.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);"}
    ]{style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 392.00px; height: 161.00px;"}
-   [Based on the user's DNA, look into the pooled OR]{.c2}

```{=html}
<!-- -->
```
-   [(Age and sex can be grabbed from our user DB)]{.c2}
-   [every disease is populated with a pooled OR]{.c2}
-   CT and TC are the same- order of genotype is irrelevant. [(check on
    this already being handled)]{.c4}
-   [output: every disease's pooled OR over 1.0]{.c2}

```{=html}
<!-- -->
```
-   [Each disease from above output is matched in the supplement
    reference database]{.c2}

```{=html}
<!-- -->
```
-   [output: supplements, dosage, disease]{.c2}
-   [If the supplement shows up twice in the output, take the higher
    dosage]{.c2}

[]{.c2}

[Lifestyle Module:]{.c10}
