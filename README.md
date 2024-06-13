# Steps to Follow

1. Install all necessary dependencies:
   ```bash
   pip install -r requirements.txt
2. Navigate to the src directory:
   ```bash
   cd src
3. Start the Uvicorn server:
   ```bash
   uvicorn main:app --reload
4. Go to http://localhost:8000 to access your backend. Authentication is added for all APIs exposed on Swagger.
   ```bash
5. Make sure u have databse named as "application" in postgresql
   if not then create a databse and mention its name in db_session.py file insted of "application" and also change the user and pssword accordingly

   
   


