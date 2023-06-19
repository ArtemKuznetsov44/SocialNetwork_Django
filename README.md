# SocialNetwork_Django
This is a third course project: **Social Network**

<hr/>

**To start project:**
1. Clone this repository.
2. Open in source-code editor.
3. Create Python virtual environment with command:  
   ```python -m venv venvName```  - For Windows  
   ```python3 -m venv venvName``` - Fro Linux 
5. Start virtual environment with command:   
   ```.\venv\Scripts\activate``` - For Windows   
   ```source venvName\bin\activate``` - For Linux  
6. If your virtual environment is activated, start a dependencies installation proccess:   
   ```pip install -r requirenments.txt``` - This file contains all required dependencies.
7. After installation proccess, switch to the app directory:   
   ```cd .\social_network\```
8. Use this command to start the project:
   ```python manage.py runserver```
<hr/>

Also you may need to create your own migraions: 
1. When venv is active and you in the app directory:   
   ```python manage.py makemigraions``` - This command will create all migraions.   
   ```python manage.py migrate``` - This command will execute migrations. 
