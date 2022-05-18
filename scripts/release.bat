call conda activate base

cd ..

del /s /q dist
del /s /q build

call conda remove -y --name ffhelper-py39 --all

call conda create -y -n ffhelper-py39 python=3.9
call conda run -n ffhelper-py39 python -m pip wheel -w dist --verbose .

call pip install twine
call twine upload dist/ffhelper*.whl --verbose



