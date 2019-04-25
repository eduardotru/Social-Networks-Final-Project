#! /bin/bash
# Bash script to run all the tests for the Social Networks project

arrProb=(0.2 0.2 0.5 0.2 0.05 0.05)
arrInitInf=(3 100 3 3 100 100)
arrTimeInf=(1 1 1 10 1 10)
arrTimeRem=(1 1 1 5 1 5)

for i in {0..5}
do
  echo "Running tests with parameters: " ${arrProb[$i]} ${arrInitInf[$i]} ${arrTimeInf[$i]} ${arrTimeRem[$i]}
  python SIR_Model.py ${arrProb[$i]} ${arrInitInf[$i]} ${arrTimeInf[$i]} ${arrTimeRem[$i]}
  python SIS_Model.py ${arrProb[$i]} ${arrInitInf[$i]} ${arrTimeInf[$i]} ${arrTimeRem[$i]}
  python SIRS_Model.py ${arrProb[$i]} ${arrInitInf[$i]} ${arrTimeInf[$i]} ${arrTimeRem[$i]}
done
