=====
Grace
=====

**DOES NOT WORK COMPLETELY YET! PLEASE ONLY USE TO TEST OR TRY OUT! THIS NOTICE WILL BE REMOVED AS SOON AS I THINK IT HAS REACHED A PRODUCTIVE POINT.**

**Grace** is a development toolkit for JavaScript, HTML and SCSS (Sass CSS).
The name **Grace** comes from a sweet puppy, which is always coming to my room whenever I start working to get the little attention that is left.

What Does It Do?
================

**Grace** enables you to write proper JavaScript without worrying about concatenating your classes together or having to deal with other problems. There is also a built in SCSS parser, so you can write nice CSS and don't need to convert it on your own, **Grace** does that for you.
The goal is that you do not have to worry about things going on around your project, but that you an concentrating on writing pure JavaScript and HTML.

How It Works
============

Install
-------

Grace can be installed on all operating systems by pulling it from pypi (https://pypi.python.org/pypi) with _pip_ or _easy_install_. The following instructions are written for Windows 8 (and 7), Mac OS X 10.3 and Debian derivates (Ubuntu, etc.).

### Windows

Generally, you have two options on Windows: Use the provided executables or use your python environment.

#### Executables

For Windows there are standalone executables available under http://www.webdiener.ch/grace.

#### Python Environment

However, if you want to get the newest versions, or want to integrate **Grace** into your python environment, you can pull them from pipy or use the source code to install it.

1. Install Python through their executable (http://www.python.org/download/releases/)
2. You may want to add Python and the script directory to your Path environment. To do that, follow the link to a guide: http://www.itechtalk.com/thread3595.html
2. Now you have multiple options. You can either go to your console and execute _easy_install.exe grace_ or get a better installer (pip) first by issuing _easy_install.exe pip_
3. If you chose to get pip, you can now use it install grace: _pip.exe install grace_
4. After you have installed grace this way, you can then use it in the command line with _python.exe C:\Python27\Scripts\grace --new_

The good thing about pip is, that it offers you an option to remove installed python modules again.

### Mac OS X

To use **Grace** on a Mac OS X system you first need to install the command line tools from Xcode. This is necessary to automatically build python modules on your system.

1. Install _command line tools_ from Xcode. To see how to do that, follow this link: http://docwiki.embarcadero.com/RADStudio/XE4/en/Installing_the_Xcode_Command_Line_Tools_on_a_Mac
2. Get pip from PyPi _sudo easy_install pip_
3. Get **Grace**: _sudo pip install grace_
4. **Grace** can now be used from the command line with: _grace --new_

### Linux

On any newer Linux derivate, their should be a python 2.7.4 installation present. If it is lower than 2.7.4 these instructions might not work for you, but grace itself will still work.

1. Install pip from the command line: _sudo apt-get install python-pip_
2. Install grace: _pip install grace --user_ (No sudo needed, --user install everything in your home directory!)
3. Add _~/.local/bin_ to your path variable
4. Use grace: _grace --new_

There is also a standalone executable for Windows (7 and 8) available. Grab it from http://www.webdiener.ch/grace.

Setup
-----

The first step would be to create a new project. This can be done by invoking **Grace** with the parameter new and an optional project name. If the project name is ommitted, it will be set to _MyProject_.
```shell
grace new YourProjectName
```
This create a new folder in your current folder with the correct structure and files needed. From here on you can go to your folder and start using **Grace** from in there.

Config
------

A config file will be placed into your project directory. This config file has a few mandatory options and can be used to further adjust **Grace** commands to your need. The following is a list with mandatory (in bold) and optional keys:
* **name**: The name of your project, will be prefilled with what you put on the command line when creating a new project with _grace new_
* version: The version of your project, will be prefilled with _0.1_
* deployment_path: The path where your project should be deployed, upon called _grace deploy_
* zip_path: The path where the zip file should be placed upon called _grace zip_

Building Your Project
---------------------

To build your project, you have to invoke **Grace** with the build task. You can also specify what exact build step you want to execute.
```shell
grace -b
```
or
```shell
grace -b --js
```

Building Tests
--------------

To build tests, execute the command _grace --test_. If you supply a test name, grace will only build that test and ignore all other. For now you can not supply multiple tests. Either one or all will be built. With the _grace --test --deploy_ you can build and instantly deploy your test to the deployment_path specified in the config file.

Available Commands
------------------

Help output of grace:

```shell
usage: grace [-h] [--new] [--name NAME] [--type TYPE] [--build] [--deploy]
             [--zip] [--test] [--html] [--js] [--css] [--img] [--lib]
             [--specific-test SPECIFIC_TEST] [--clean] [--bad]

Tasks to execute

optional arguments:
  -h, --help            show this help message and exit
  --new                 Create a new project in the current directory with a
                        project name or `MyProject` as default.
  --name NAME           Provide a name for the project. Only used with --new
                        option.
  --type TYPE           Decide what type of project you want to create. Only
                        used with --new
  --build, -b           Build the project.
  --deploy, -d          Deploy the project.
  --zip, -z             Zip the project.
  --test, -t            Build the tests.
  --html                Only use html for the task.
  --js                  Only use js for the task.
  --css                 Only use css for the task.
  --img                 Only use images for the task.
  --lib                 Only use libraries for the task.
  --specific-test SPECIFIC_TEST
                        Only build the specified test
  --clean, -c           Clean the build environment
  --bad                 Execute all tasks: build, test, deploy, zip.
```

JavaScript Setup
----------------

It is important that you follow the JavaScript setup, or you will not be able to use **Grace**. You can either write all your code in the provided application.js file, or use the structure to split it up. It is highly recommended to split your JavaScript code into single classes, giving each class its own file. This way you will have a much better overview. To do this, **Grace** parse your application.js file and sees if the first line as a _//include MyClass_ in it. This is the starting point, meaning that your first class file should be something like a _main_ in other languages. In every JavaScript file you create, you can add the _//include Path/To/Class/File_ at the beginning, to include another file. It is important that you do not add the .js at the end. The following is an example set up:

application.js
```javascript
//include MyMain

jQuery(document).ready(function() {
    main = new MyProject.MyMain()
});
```

MyMain.js
```javascript
//include utils/MyUtils.js

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
