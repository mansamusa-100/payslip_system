echo "======> INSTALLING REQUIREMENT <======"
pip install -r requirements.txt
echo "======> REQUIREMENT INSTALLED <======"

echo "======> COLLECTING STATIC FILES <======"
python manage.py collectstatic --noinput --clear
echo "======> STATIC FILES COLLECTED <======"

echo "======> MAKE-MIGRATIONS <======"
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "======> MAKE-MIGRATIONS END <======"
