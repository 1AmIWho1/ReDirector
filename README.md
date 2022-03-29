# ReDirector

### The goal
To provide service 
Предоставить пользователю сервис, на котором можно быстро создать сокращенную ссылку

### Software requirements
Develop Flask-application, providing simple link-shortening service. Minimum requirements:

- add new links and create aliases for them (short links)
- redirect user by aliases registered in the system
- show 404 page if alias is not correct

### Technological stack:
- python
- flask
- wtforms
- apscheduler
- hashids
- sqlite

### How to set up project:
1. Clone repository:
```bash
git clone https://github.com/1AmIWho1/pent.git
```
2. Update pip: 
```bash
pip install --upgrade pip
```
3. Install required packages: 
```bash
pip install -r requirements.txt
```
4. Create your own `.env` (you may use `.env.example`)
5. Run server:
```bash
python wsgi.py
```
