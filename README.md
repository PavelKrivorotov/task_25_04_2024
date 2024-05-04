## Preview

This application provides personal information to registered users. To view account information, the user need
*Login* or *Register*.

<picture>
  <img alt="The image of the login page" src="./pictures/picture-1.png">
</picture>

After authentication success, the user will see the personal account information.

<picture>
  <img alt="The image of the profile page" src="./pictures/picture-2.png">
</picture>

The administration functionality as also available. The Admin can show extended informations
aboutn users.

<picture>
  <img alt="The image of the login page" src="./pictures/picture-3.png">
</picture>


## Installation

1) Clone this repository:

```bash
git clone https://github.com/PavelKrivorotov/task_25_04_2024.git
```

## Usage

1) Run containers in work directory:
  
  ```bash
  docker compose up
  ```

2) Open this url adress in browser (Frontend):

 ```bash
 http://127.0.0.1:80
 ```

3) Open this url, if you want show API (Backend)

```bash
http://127.0.0.1:8000/docs
```

## Default

This following settings are available by default
1) Jobs
   - Junior
     - id: **077c2e60-2a21-41c6-9b99-fce84d490a3a**
   - Middle
     - id: **acd00cd4-f548-4804-bbe2-31a72adebd78**
   - Senior
     - id: **815b87e7-cc34-45dc-b520-38bc32372962**
3) Admins
   - username: **admin**
   - password: **admin**

## Testing

1) In running application containers

```bash
docker compose exec backend sh
```

2) In container terminal

```bash
/bin/sh ./run-tests.sh
```

## Hard mode (Linux)

### If you want run application without Docker:

1) Clone this repository

```bash
git clone https://github.com/PavelKrivorotov/task_25_04_2024.git
```

#### Run database (postgres > v13):

1) Start database

```bash
sudo systemctl start postgresql
```

2) Connect to database

```bash
psql -U postgres -h 127.0.0.1 -p 5432
```

4) Create database

```bash
postgres# CREATE DATABASE task_25_04_2024;
```

#### Run backend (python > v3.10.0):

1) In work directory

```bash
cd backend
```

2) Create virtual environment

```bash
virtualenv venv
```

3) Activate virtual environment

```bash
source venv/bin/activate
```

4) Install requirements

```bash
(venv) pip install -r requirements.txt
```

5) Run start project script

```bash
(venv) /bin/sh ./run-project.sh
```

#### Run tests:

```bash
(venv) /bin/sh ./run-tests.sh
```

#### Run frontend (node > v18.0):

1) In work directory

```bash
cd frontend
```

2) Install requirements

```bash
npm install
```

3) Run vue application in dev mode

```bash
npm run dev
```
