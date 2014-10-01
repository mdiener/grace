=====
Grace
=====

**Please know that Grace is still in a beta stage. If you discover a bug please report it the respective github page (grace/grace-dizmo).**

**Grace** is a development toolkit for JavaScript, HTML and SCSS (Sass CSS).
The name **Grace** comes from a sweet puppy, which is always coming to my room whenever I start working to get the little attention that is left.

License
=======

Grace is released under a GPL license. You can read the full license in the attached LICENSE.txt file.

What Does It Do?
================

**Grace** enables you to write proper JavaScript without worrying about concatenating your classes together or having to deal with other problems. There is also a built in SCSS parser, so you can write nice CSS and don't need to convert it on your own, **Grace** does that for you.
The goal is that you do not have to worry about things going on around your project, but that you an concentrating on writing pure JavaScript and HTML.

How It Works
============

Install
-------

Grace can be installed on all operating systems by pulling it from pypi (https://pypi.python.org/pypi) with *pip* or *easy_install*. The following instructions are written for Windows 8 (and 7), Mac OS X 10.3 and Debian derivates (Ubuntu, etc.).

### Windows

Generally, you have two options on Windows: Use the provided executables or use your python environment.

#### Executables

There are no current executable available for Windows right now. As soon as I have time I will create new one and provide them to you. If someone wants to take this step over, please feel free to do so! I always have trouble building these and would appreciate any help I can get there.

#### Python Environment

However, if you want to get the newest versions, or want to integrate **Grace** into your python environment, you can pull them from pipy or use the source code to install it.

1. Install Python through their executable (http://www.python.org/download/releases/)
2. You may want to add Python and the script directory to your Path environment. To do that, follow the link to a guide: http://www.itechtalk.com/thread3595.html
2. Now that you have installed Python, you should get yourself a decent package installer for it. Head over to http://pip.readthedocs.org/en/latest/installing.html and follow the instructions.
3. You can now use pip to install grace: *pip.exe install grace*
4. After you have installed grace this way, you can then use it in the command line with *python C:\Python27\Scripts\grace new*

The good thing about pip is, that it offers you an option to remove installed python modules again.

### Mac OS X

To use **Grace** on a Mac OS X system you first need to install the command line tools from Xcode. This is necessary to automatically build python modules on your system.

1. Install *command line tools* from Xcode. To see how to do that, follow this link: http://docwiki.embarcadero.com/RADStudio/XE4/en/Installing_the_Xcode_Command_Line_Tools_on_a_Mac
2. Get pip from PyPi *sudo easy_install pip*
3. Get **Grace**: *sudo pip install grace*
4. **Grace** can now be used from the command line with: *grace new*

### Linux

On any newer Linux distribution, there should be a python installation present. If it is lower than 2.7.4 these instructions might not work for you, but grace itself will still work.

1. Install pip from the command line: *sudo apt-get install python-pip*
2. Install grace: *pip install grace --user* (No sudo needed, --user install everything in your home directory!)
3. Add *~/.local/bin* to your path variable
4. Use grace: *grace new*

Setup
-----

The first step would be to create a new project. This can be done by invoking **Grace** with the parameter new. **Grace** will then ask for you project name and what type of project (by default the default) you want to create.
```shell
grace new
```
After filling out the required information,**Grace** creates a new folder in your current folder with the correct structure and files needed. From here on you can go to your folder and start using **Grace** from in there.

Porting
-------

If you have an older version of **Grace** (<0.2.0) you can update it using the command _grace port_. This will create the required manage.py file in your project folder.

Config
------

There are two configuration file present. The global one can be found in the current user's home directory (*.graceconfig*) and contains (more about each value further down):
* deployment_path
* zip_path
* doc_path
* minify_js
* minify_css
All these values apply to all your **Grace** projects and can be overwritten on a project to project basis.

The other configuration file will be placed in the local directory of you project. This file has a few mandatory options and can be used to further adjust **Grace** commands to your need. The following is a list with mandatory (in bold) and optional keys:
* **name**: The name of your project, will be prefilled with what you put on the command line when creating a new project with *grace new*
* **version**: The version of your project, will be prefilled with "0.1"
* deployment_path: The path where your project should be deployed, upon calling *python manage.py deploy*
* zip_path: The path where the zip file should be placed upon calling *python manage.py zip*
* doc_path: The path where the JavaScript docs will be built to. Called with *python manage.py doc*
* minify_js: Specify wether grace should try to minified your JavaScript
* minify_css: Specify wether grace should try to minify your css files
* js_name: The name that the result of the concatenation of all your JavaScript files will have

Building Your Project
---------------------

To build your project, you have to use the provided manage.py file with the build task.
```shell
python manage.py build
```

Building Tests
--------------

To build tests, execute the command python manage.py test_. With _python manage.py test:deploy_ you can build and instantly deploy your test to the deployment_path specified in the config file.

Available Commands
------------------

For grace

```shell
usage: grace [command]

Commands
  help            show this help message and exit
  new             Create a new project in the current directory
  port            Port from an older grace version to the newest
```

For the manage.py file
```
usage: python manage.py [command]

Commands
  build           Builds the project and places the output in ./build/ProjectName.
  deploy          First build and then deploy the project to the path
                  specified in the deployment_path option in your project.cfg file.
  jsdoc           Build the jsDoc of the project.
  zip             Build and then zip the output and put it into the path
                  specified by the zip_path option in your project.cfg file.
  test            Build all the tests.
  clean           Clean the build output.
  test:deploy     Build and then deploy the tests.
  test:zip        Build and then zip the tests
  st              Can be used with any command to show the full stack trace
                  (in case of an error).
```

JavaScript Setup
----------------

It is important that you follow the JavaScript setup, or you will not be able to use **Grace**. You can either write all your code in the provided application.js file, or use the structure to split it up. It is highly recommended to split your JavaScript code into single classes, giving each class its own file. This way you will have a much better overview. To do this, **Grace** parses your application.js file and sees if the first line as a *//= require MyClass* in it. This is the starting point, meaning that your first class file should be something like a *main* in other languages. In every JavaScript file you create, you can add the *//= require Path/To/Class/File* at the beginning, to include another file. It is important that you do not add the .js at the end. The following is an example set up:

application.js
```javascript
//= require MyMain

jQuery(document).ready(function() {
    main = new MyProject.MyMain()
});
```

MyMain.js
```javascript
//= require utils/MyUtils.js

Class('MyProject.MyMain', {
    has: {
        log: {
            is: 'r',
            init: MyProject.utils.MyUtils.logWithType
        }
    }

    after: {
        initialize: function() {
            var self = this;

            self.draw('circle'))
        }
    }
});
```

utils/MyUtils.js
```javascript
Class('MyProject.utils.MyUtils', {
    my: {
        methods: {
            logWithType: function(val) {
                console.log(jQuery.type(val), val);
            }
        }
    }
});
```

The folder structure for this would look as following:
<pre>
MyProject
|-- project.cfg
|-- manage.py
`-- src
    |-- index.html
    |-- javascript
    |   |-- MyMain.js
    |   `-- utils
    |       `-- MyUtils.js
    `-- lib
        |-- jquery
        |   `-- jquery.min.js
        `-- joose
            `-- joose.min.js
</pre>

For more information on Joose and the class system go to http://joose.it/.
