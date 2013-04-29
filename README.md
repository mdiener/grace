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

To install **Grace** get it from pypi with _pip install grace --user_. You may need to add _~/.local/bin_ to your PATH in order to use grace easily. You can also use _easy_install grace_ but pip is definitely preferred.

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
```shell
grace --new [--type TYPE] [--name [NAME]]
grace --build, -b [--html] [--css] [--js] [--img] [--lib]
grace --deploy, -d
grace --test, -t [--specific-test [NAME]]
grace --zip, -z
grace --bad
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
