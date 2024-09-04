In angle run folder there is the Arduino code written in c/c++. Upload it to the Arduino by selecting the Board and PORT(make sure you remember the port because we will need it)

Now you need go to CMD/Terminal to your folder's location/path and then follow the following steps

1. python -m venv .env
2. if using linux distro:
     source .env/bin/activate
   if using windows:
     .env\Scripts\activate
4. pip install -r requirements.txt
5. python sendAngle.py
