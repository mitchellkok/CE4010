# CE4010 Applied Cryptography Course Project Topic #2: "TellNTU"

## Project Brief 

#### Motivation For Project: 
While platforms such as NTU Confessions and NTU Reddit are widely available for NTU students to post their grievances anonymously, these platforms go unnoticed by authorities within NTU. 'TellNTU' is here to bridge the gap - to give NTU students a platform to reach out to the authorities anonymously and to give the authorities a space to respond to grievances from NTU students and build a more transparent and cohesive campus experience.


## Instructions for Code Usage

#### Setting up the environment
1. Ensure Python 3.9.x is installed
2. Install the required libraries using `pip install -r requirements.txt`;


#### Running the code
1. After setting up the environment, run `python app.py`
2. From the terminal, ctrl+click the link shown: *Running on http://x.x.x.x:1025/*
3. The application's main page should be opened in your default browser

Site Preview: <kbd> <img width="960" alt="Capture" src="https://user-images.githubusercontent.com/65217872/143465633-d3c393d4-d846-4a3e-89a4-cfa507809e6d.PNG"> </kbd>


4. You may login using the following account details:\
\
&nbsp;&nbsp;&nbsp;&nbsp;UserType: *Student*\
&nbsp;&nbsp;&nbsp;&nbsp;Username/Email: *sallyyeo@gmail.com*\
&nbsp;&nbsp;&nbsp;&nbsp;Password: *sally123*\
\
&nbsp;&nbsp;&nbsp;&nbsp;UserType: *Staff*\
&nbsp;&nbsp;&nbsp;&nbsp;Username/Email: *och@gmail.com*\
&nbsp;&nbsp;&nbsp;&nbsp;Password: *123*

5. Suggested Test Cases:

>Student:
>- Adding New Confession *(NOTE: Current system only supports confessions without commas and paragraphing)*
>- Liking Other Confessions
>- Liking Authority Redressals
>
>
>Staff:
>- Redressing New Confession *(NOTE: Current system only supports redressals without commas and paragraphing)*
>- Liking Other Confessions
>- Liking Authority Redressals


## Notes
#### 'TellNTU' is secured by Fernet Symmetric Key Encryption
- The Key is generated using os.urandom(), a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG) suitable for cryptographic use
- CSV Files are only decrypted by app.py (the key is never shared with any other party, minimising opportunity for key leakage) 
- CSV Files remain encrypted between function calls (at no instance does the plain text reveal itself) 
- CSV data is displayed selectively by app.py (only relevant data is displayed via the HTML files, the rest are hidden within the python script)

## References/Libraries
cryptography==36.0.0\
Flask==2.0.2
