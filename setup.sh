rm -rf env 2>/dev/null

python3 -m venv env

cd env
source bin/activate
cd ..

pip install -r requirements.txt || exit 2
