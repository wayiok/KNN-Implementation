echo "------------------------------------"
echo "-----------------------LECTURA------"
echo "------------------------------------"
python PrimerPaso.py
echo "------------------------------------"
echo "-----------------------ETL----------"
echo "------------------------------------"
python SegundoPaso.py
echo "------------------------------------"
echo "-----------------------K-NN---------"
echo "------------------------------------"
python TercerPaso.py
echo "------------------------------------"
echo "-----------------------INJECTION----"
echo "------------------------------------"
python CuartoPaso.py