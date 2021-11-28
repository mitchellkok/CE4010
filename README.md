# CE4010 Applied Cryptography Course Project<br/>Topic #2 : "TellNTU"

## Project Brief 

#### Motivation For Project: 
While platforms such as NTU Confessions and NTU Reddit are widely available for NTU students to post their grievances anonymously, these platforms go unnoticed by authorities within NTU. 'TellNTU' is here to bridge the gap - to give NTU students a platform to reach out to the authorities anonymously and to give the authorities a space to respond to grievances from NTU students and build a more transparent and cohesive campus experience.


## Implementation Details
#### 'TellNTU' is secured by Fernet Symmetric Key Encryption
Since the encrypted data is only accessed by the application, there is no need for an encryption key to be shared. Hence symmetric key encryption was suitable as the key resides only with the application. We settled on Fernet, which is based on 128-bit AES in CBC mode, for our data encryption. It was ideal for our project for the following reasons:
1. Key Security
    - Key generated using os.urandom(), which is a Cryptographically Secure Pseudo-Random Number Generator (CSPRNG) suitable for cryptographic use.
    - CSV files are only decrypted by app.py; the key is never shared with any other party, minimising opportunity for key leakage.

 2. Information Disclosure
    - All decyption is done within the application, meaning that there is no plaintext in transit at any point in time.
    - CSV files remain encrypted between function calls (i.e. CSV files do not remain decrypted for the whole duration that app.py is running).
    - CSV data is displayed selectively by app.py; only relevant data is displayed via the HTML files, and the rest is hidden within the Python script.

3. Data Verification
    - CSV files are verified using the HMAC tail when the application is first started, and with every subsequent access to the files within the application.

#### 'TellNTU' is powered by Flask web framework
This implementation runs on a Flask local development server, although the final aim would be to deploy the application to the cloud.

## Instructions for Code Usage

#### Setting up the environment
1. Ensure Python 3.9.x is installed
2. Install the required libraries using `pip install -r requirements.txt`;


#### Running the code
1. After setting up the environment, run `python app.py`
2. From the terminal, ctrl+click the link shown: *Running on http://x.x.x.x:1025/*
3. The application's main page should be opened in your default browser

Site Preview: <kbd> <img width="960" alt="Capture" src="https://user-images.githubusercontent.com/65217872/143465633-d3c393d4-d846-4a3e-89a4-cfa507809e6d.PNG"> </kbd>


4. You may login using the following account details or register your own Student account:\
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

## Libraries Used
- cffi==1.15.0
- click==8.0.3
- cryptography==36.0.0
- Flask==2.0.2
- itsdangerous==2.0.1
- Jinja2==3.0.3
- MarkupSafe==2.0.1
- pycparser==2.21
- Werkzeug==2.0.2

