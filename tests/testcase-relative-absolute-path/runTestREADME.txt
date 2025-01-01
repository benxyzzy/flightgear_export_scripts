######WHAT THIS TEST DOES##############

This test checks if absolute texture path is used in concated ac3d instead of relative paths

######PERFORMING THE TEST##############

#1) Check Helgo_Toilets.ac for the word "texture", you will see it has a relative path

#2) you will need to set the path environment variable to concat_ac3.py for the to the following line to run the converter

PATHTOCONCATAC3="/home/user/flightgear_tests/flightgear_export_scripts/concat_ac3.py"

#3)

#cd to the directory containing this test, then

4) run ...

FG_ROOT="${PWD}/" FG_SCENERY="${PWD}/" python3 ${PATHTOCONCATAC3} "TestTheLoo.stg" >> "output.ac"

#5) ... now check "output.ac" to see if the output.ac texture path is absolute
# you can do this by running

grep texture output.ac

#If it's absolute, the test has been passed

##############LICENCING FOR THIS TEST#########

This test contains 2 files from flightgear data, Helgo_Toilets.ac and Helgo_Toilets.png  . Both were under the GPLv2 Licence . A COPYING file has been
included