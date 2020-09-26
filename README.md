# Home Control Panel

## Repository Index
- [API](https://github.com/COS301-SE-2020/Watchdog-API)
- [Frontend](https://github.com/COS301-SE-2020/Watchdog-FrontEnd)
- [Home Control Panel](https://github.com/COS301-SE-2020/Watchdog)

## Demo Video
- [LynkSolutions-Demo2](https://drive.google.com/file/d/1JfVWYLl65t5PzllO-vNKPR-YlOt7DRnX/view?usp=sharing)

## Documentation
- [Capstone Demo 2 Documentation](https://drive.google.com/file/d/1eBr5il0vBNbcobf96etwTo1S3SHeI1IU/view?usp=sharing)
- [Watchdog User Manual](https://drive.google.com/file/d/1gu36_44IbnKeGjC61VaDXLu3mLKEqTvr/view?usp=sharing)
- [Coding Standards Document]()
- [Project Management Tool (Clubhouse)](https://app.clubhouse.io/lynksolutions/)

## Deployed Website Link
- [Watchdog System](https://master.d18pg5ypwr9xji.amplifyapp.com/)

## Project Description
For the South African household who need an efficient way to ensure their safety and security the Watchdog system is a home security system that utilizes machine 
learning to identify an intruder and alert users and security companies on the potential breach. Unlike traditional surveillance systems that keep a backlog of 
redundant video storage our product utilizes machine learning and a modern cloud architecture to deliver a real-time security system.
## Members
|Member|Student #|Page|LinkedIn|
|------|---------|----|--------|
|Luqmaan Badat|17088519|<https://github.com/luqmaanbadat>|<https://www.linkedin.com/in/luqmaan-badat/>|
|Aboobakr Kharbai|u18037306|<https://abubakrk.github.io>|<https://www.linkedin.com/in/aboobacker-kharbai-7a94961a9/>|
|Jordan Manas|u17080534|<https://u17080534.github.io>|<https://www.linkedin.com/in/jordan-manas-b822651aa/>|
|Ushir Raval|u16013604|<https://urishiraval.github.io>| <https://www.linkedin.com/in/unraval/>|
|Jonathen Sundy|u18079581|<https://jsundy.github.io>|<https://www.linkedin.com/in/jonathen-sundy-79b33b168/>|
|Armin van Wyk|u18008632|<https://github.com/BigMacDaddy007>|<https://www.linkedin.com/in/armin-van-wyk-b714931a9/>|

## Profiles
### Jordan Manas

An avid student of the numerous fields found within Computer Science, with a concentration in the field of Artificial Intelligence. Also being well-versed in Web Development, I recognize that I am capable of fulfilling important roles in the given project. I have experience in developing projects that use almost all of the proposed technologies and am very confident that our final product will be one of quality.

### Jonathen Sundy
![image](https://drive.google.com/uc?export=view&id=10ZNi-LlrJPn8OqM5xFladO6TvPYE30oB)

I have been exposed to an event-driven system that adopted modern cloud architecture that was hosted on Heroku and used a subset of AWS. I will use this knowledge gained to pioneer the system to be loosely coupled that promotes independent events triggering different parts of the system. Hence, I am certain that I will be of great value to the development of the serverless architecture. I am not too coherent with AWS but am motivated and inspired to expand my knowledge!

### Ushir Raval

My exposure varies greatly from desktop applications to web based technologies, all in mostly a corporate “fintech” focused development environment. My skillset ranges from python development to web-based desktop applications using full stack technologies and my personal motto is “measure twice, cut once”. I prize scalable, robust and portable code above all else and intend to primarily contribute to the integration of various technologies such as the front-end to back-end communication etcetera.

### Luqmaan Badat

I am a final year computer science student. I am adaptable, reliable and keen to learn new programming technologies. My interests are software engineering, artificial intelligence and web development. My skills range include web development, full stack development, Java development and using full stack development technologies like docker and circleci. I’ve been exposed to and worked on cloud-based solutions in the medical field. 

### Aboobakr Kharbai

My exposure ranges between desktop applications and web-based technologies. I am very reliable as well as trustworthy. I have a broad range of experience in backend development which includes database management systems, as well as experience in java development. I am one who is always steadfast in deadlines set out and will do anything in my capacity to ensure the work done is before the deadline and also of an industry standard.

### Armin van Wyk

I have been involved in a multitude of projects inside and outside of the EBIT faculty. I have particular interest in front-end multimedia design to back-end REST API and hosting tasks. I have familiarity in databases both with and without SQ. I can use these skills in the request handling and data handling of our projects and ensure validated, clean and lightweight data.


## How to run the code in this repo:
1. Install [poetry](https://pypi.org/project/poetrify/). This is used to manage your Python version.
2. Install all the dependencies by running the following:
```
poetry install
```
3. Run the HCP:
```
poetry run python home_control_system
```

## How do I set up my IDE?

Poetry copies your Python interpreter (the one we specified with pyenv) to a special folder, and installs project dependencies into this folder. This is called a Virtual Environment. If there is a `poetry.lock` file then running `poetry install` will install _exactly_ these dependencies, or (if `poetry.lock` is missing) it will install the dependencies from `pyproject.toml` and "lock" them by creating a new `poetry.lock`.

Running `poetry shell` or `poetry run` appends your project's Python interpreter to the front of your `PATH` variable to ensure that you don't use any others. But your IDE must know the path to this Python interpreter if you want it to correctly lint and provide intellisense for your code.

You can get the path pretty easily:

   ```bash
   poetry run which python
   ```

- If you're using **VSCode** you'll need to install the Python extension and provide the above path to the command `> Select Python Interpreter`.
- If you're using **PyCharm**, then specify it under `Preferences > Project: Project Interpreter`. Future versions of [PyCharm may find it automatically](https://youtrack.jetbrains.com/issue/PY-30702).

In order to point your IDE to PYTHONPATH in your IDE to fix import resolution problems, follow this link (https://stackoverflow.com/questions/17198319/how-to-configure-custom-pythonpath-with-vm-and-pycharm)

On a deploy, it doesn't know anything about our dependencies in `pyproject.toml`—it's old school and looks for a `requirements.txt` instead. So we need to make sure that this file exists and contains the same dependencies as `pyproject.toml`:

   ```bash
   poetry run pip freeze > requirements.txt
   ```

OR

we have installed a pyPi library called **poetrify** that is used to pipe the required dependencies to the requirements.txt. All you need to do is run the following command:

   ```bash
   poetry run poetrify generate -d -s requirements.txt
   ```

If you change dependencies, you'll need to remember to generate this file.