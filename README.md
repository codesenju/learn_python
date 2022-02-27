# Paython Paramiko

## To use the python paramiko module, install it from the packages folder:

```powershell
pip install .\packages\paramiko-2.9.2-py2.py3-none-any.whl
```

## Run http server
#### this serves files relative to the current directory:
```powershell
python -m http.server 8000
```

## The option **--directory** specifies a directory to which it should serve the files

```powershell
python -m http.server --directory /tmp/
```

## How to run a fileserver as a windows service
```powershell
C:\nssm-2.24\win64\nssm.exe install 'fileserver' 'C:\Python310\python.exe' '-m http.server 8000 --directory C:\Temp
```

## Run paramiko-module.py
##
```powershell
py .\paramiko-module.py <host> <username> '<password>'  'powershell.exe ls D:\DevOps\Deployments\tests'
```