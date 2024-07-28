# Dog-petshop

Firstly, sorry it took me so long to make this application - I had gotten busy with work recently and finally got some time off to make this application. I can feel i have gotten a little rusty, but i warm up quickly so that wouldnt be a problem for more than a day 

### Your description:

 a Flask app, to set up a dog shop with gems. So I need to have some breeds, names and prices so if you enter the shop you can buy a pet :)


# How to start

* Just run: 
``` python client.py ```
    * I have made it so the app.py is automatically run by client.py so its easier to start up.

### Flow

1. You will be presented with a startmenu and you will choose to Login as i have already made an account for you 
username: ```Ruben``` password: ```hello```
    
    - You can also register your own account if you want!

2. Once you are in you will want to see the list of dogs ```Option 1```, i kept this list short to make it easier on the eyes.

3. When you see a dog you like, you press ```Option 2``` to initiate the buy phase, and input the dogs id

4. If you have sufficient funds (gems) you'll now own a new dog, congrats! :D

    * To reset everything start the application and choose ```option 4```, this reverts all dogs to ```AVAILABLE``` and resets your gem-balance



# Features

- Shop where you can buy a dog using gems for currency
- Dogs have names, prices and breeds
- Simple application with no frontend
- Flask application in the console
- textfile databases (open them to see your useraccount)
    * DB.txt(keeps the dogs)
    * user.txt (keeps the users)


# Extra ideas

I decided to keep it simple as you asked me to, but i could expand upon the application with code optimization like:
    
* Replacing the current filewrite system with something more efficient 
    * Using a filewrite system that does not truncate the files as they're opened
* Optimizing the API-calls
    * Removing extra steps i included to show understanding

## Features i wanted to do but decided to leave out

As mentioned i dont want to overdo it, so i exluded:
* Admin-page (in the console) to where you can add or remove dogs/users
    * But that would cause the code to get complex with conditions
* Giving more options like being able to inspect a particular dog and read about it and its background
