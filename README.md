# The Dull Parts

A Flask app skeleton that handles: 

- Database Initialization
- Authentication, Roles and Profiles
- Password Change/Recovery
- A Tiny Administration Menu

The Dull Parts is meant to provide a good start on all the admin and user handling bits of a small app that you can just drop your awesome idea into and customize to your needs. It uses several very common flask modules.

- Flask-Auth for authentication and roles (uses SQLite for dev, requires an SQL database and redis for production)
- Flask-SQLAlchemy for ORM duties
- Flask-Restful for the API (optional, it depends on your Profiles)
- Flask-WhooshAlchemy for Profile searches
- Flask-Mail (pre-configured for gmail account)

All templates use Bootstrap out of the box. It's not required, but you'll probably want to make a few changes if you pull it out.

If you have a working knowledge of Flask and python, this skeleton might save you a few days.

# Why? WHY?
I use Flask on a daily basis to create small apps for work. Sometimes I find I need a combination of features that a micro-framework does not supply out of the box, but still does not inspire me to descend into the various bolgia of a "full-featured" framework.

The mighty Django, for instance, has very thoroughly-thought-out "admin" features. A project may not wish to use this feature at all (see the excellent [Saleor](https://github.com/mirumee/saleor) storefront for a good example). Unfortunately, all that stuff still lives in your code, and who knows what it's going to get up to?

So, this is not the life's work of a genius coder! Just some techniques I have found useful, and is offered in the hopes that I can save someone else time and energy.

## Quick Start 
1. Fork this repository
1. Clone repository and create a virtual environment.
1. Set the environment variables as described in [Environment](#environment).
1. Using the ADMIN_SECRET_KEY as an endpoint, browse to http://localhost/admin/init/<ADMIN_SECRET_KEY>
1. Create your root user.
1. Log in.
1. Complete root profile.
1. Add your fantastic code.

If this is a little sparse for you, see [Detailed Setup and Deployment Suggestions](https://github.com/kphretiq/the-dull-parts/wiki/Detailed-Setup-and-Deployment-Suggestions)

## <a name="environment">Environment</a>
I suggest using [autoenv](https://github.com/kennethreitz/autoenv) and creating an .env file.

### Example .env File
```bash
APP_SECRET_KEY="backinnagasakiwherethefellowschewtobaccy";
ADMIN_SECRET_KEY="andthewomenwickywackywoo";
SQLALCHEMY_DATABASE_URI="sqlite:////$(pwd)/dullparts.db";
SQLALCHEMY_DATABASE_NAME="dullparts";
SESSION_TYPE="sqlalchemy"
MAIL_USERNAME="someuser@gmail.com";
MAIL_PASSWORD="secretpassword";
SIGN_UP_SENDER="someuser@gmail.com";
SIGN_UP_MESSAGE="Exiting App! It Excites One!"
```
#### postgresql+psycopg2
You'll need to run redis, as the session key is too large for sqlalchemy session to handle
```bash
SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://dullparts:password@localhost/dullparts";
SESSION_TYPE="redis"
```
#### mysql
You'll need to run redis, as the session key is too large for sqlalchemy session to handle
```bash
SQLALCHEMY_DATABASE_URI="mysql+pymysql://dullparts:password@localhost/dullparts";
SESSION_TYPE="redis"
```
### Tables
Tables are defined in App/Models.py. You are supplied with three tables:

- User: The user authentication table supplied by Flask-Auth
- Profile: Table for user data, with relation to User table so roles are available.
- TempAuth: A temporary table used to supply keys for initializing user and updating passwords.

## Authentication
- Flask-Auth handles authentication and assignment of roles.
- sqlite with a SESSION_TYPE of "sqlalchemy" is fine for development
- redis handles session in production. Use SESSION_TYPE "redis".

see App/Routes/Auth.py and App/Roles.py
