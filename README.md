# DC Sonar User Layer

It is part of the [dc-sonar](https://github.com/ST1LLY/dc-sonar) project.

## Deploy for development

Clone the [dc-sonar-user-layer](https://github.com/ST1LLY/dc-sonar-user-layer)

```bash
git clone https://github.com/ST1LLY/dc-sonar-user-layer.git
```

### Windows

Open Powershell.

Go to the created dc-sonar-user-layer folder:

```
cd {YOUR_PATH}
```

Create Python virtual environment:

```powershell
&"C:\Program Files\Python310\python.exe" -m venv venv
```

Active created venv:

```
.\venv\Scripts\Activate.ps1
```

Install pip packages:

```
pip install -r .\requirements.txt
```

Open the dc-sonar-user-layer folder in IDE - PyCharm, for example.

### Ubuntu

Go to the folder where the directory with the source is located.

Deactivate the previous venv if it uses:

```shell
deactivate
```

Create venv:

```shell
python3.10 -m venv venv-user-layer
```

Activate created venv:

```shell
source venv-user-layer/bin/activate
```

Install dependencies:

```shell
pip install -r dc-sonar-user-layer/requirements.txt
```

Deactivate venv:

```
deactivate
```

### Config

Copy `dc_sonar_web/sensitive_settings_blank.py` to `dc_sonar_web/sensitive_settings.py`

Set the params:

`S_DATABASES` contains value for [DATABASES](https://docs.djangoproject.com/en/4.0/ref/settings/#databases) in `dc_sonar_web/settings.py` used for DB connection.

`S_SECRET_KEY` contains value for [SECRET_KEY](https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/#secret-key) in `dc_sonar_web/settings.py` .

`S_SIGNING_KEY` contains value for Simple JWT [SIGNING_KEY](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#signing-key)  in `dc_sonar_web/settings.py`.

`S_AES_256_KEY` contains value for `AES_256_KEY` in `dc_sonar_web/settings.py` using for decryption and  encryption saved passwords of accounts have been bruted.

Example:

```python
S_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'web_app_db',
        'USER': 'dc_sonar_user_layer',
        'PASSWORD': 'f}jod5?y3R>,RsLqmAt-e5G*sujRL1+?1Wip!YX:e86n>]suA3n)V!:YqeE~*LVN',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

S_SECRET_KEY = 'q5W04kBYo5-e1N]yyJJ+MD_L>~+ERn:M9JPAVbMNiC>9ZMWzkd>+9qtsvAPdc?)F'
S_SIGNING_KEY = 'r?r:f2dP,N0k!HW?_TJ?z_d}Fu0Z?n]Qrv_6U}qtvyT%jm8C5?]s#@E2W6oKc3uc'
S_AES_256_KEY = '8^xjD=0v3Lk_1QNZW+1sb6u)oDQw0nhcPvu^gh:jHCyR*}jn+_T#Ak%*>3p_yvZe'
```

Before the first run, it is needed to init models.

Open terminal.

Activate venv:

```shell
source venv-user-layer/bin/activate
```

Go to the project directory:

```shell
cd dc-sonar-user-layer/
```

Run the migrate command:

```shell
python manage.py migrate
```

[Create](https://docs.djangoproject.com/en/1.8/intro/tutorial02/#creating-an-admin-user) Django admin user.

### Run

Open terminal.

Execute commands for running Django backend:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/
python manage.py runsslserver 0.0.0.0:8000
```

Open terminal.

Execute commands for running ntlm_brute_info_getter:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/user_cabinet
python ntlm_brute_info_getter.py
```

Open terminal.

Execute commands for running ntlm_dump_info_getter:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/user_cabinet
python ntlm_dump_info_getter.py
```

Open terminal.

Execute commands for running no_exp_pass_info_getter:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/user_cabinet
python no_exp_pass_info_getter.py
```

Open terminal.

Execute commands for running reused_pass_info_getter:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/user_cabinet
python reused_pass_info_getter.py
```

Open terminal.

Execute commands for running sheduled tasks setter:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/
celery -A dc_sonar_web beat -l info
```

Open terminal.

Execute commands for running sheduled tasks performer:

```
source venv-user-layer/bin/activate
cd dc-sonar-user-layer/
celery -A dc_sonar_web worker -l info
```

Django admin is located on https://localhost:8000/admin/.

Django REST API is located on https://localhost:8000/api/user-cabinet/domain/.

## Versions

### 2022.7.27-1

The initial version.