# ReDirector

### The goal
To provide link-shortening service 

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
4. Customize projects to your needs: 
- In `config.py` you may change `DEBUG` на `False`
- In`config.py` write a secret key in variable `SECRET_KEY`
- Set domen name in `app/views.py` in variable `domen`
5. Run server:
```bash
python run.py
```
