Grace
=====

**DOES NOT WORK COMPLETELY YET! PLEASE ONLY USE TO TEST OR TRY OUT! THIS NOTICE WILL BE REMOVED AS SOON AS I THINK IT REACHED A PRODUCTIVE POINT.**

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

To install **Grace**, pull it from github create an alias for the respective executable in your shell rc file. You will need the libsass library to use **Grace**. For now it will most likely only work on Linux (Debian, mostly) distributions. Mac users should be able to use it, but I am not sure what errors you might encounter. So far it will not work on Windows, however, I do plan to support all three platforms in the future.

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
grace build
```
or
```shell
grace build:javascript
```

Dizmo
-----

**Grace** can also be conveniently used to build and manage dizmos. It allows you to create dizmos, takes care of the plist file for you (you only have to worry about the keys you actually want to adjust, except the mandatory bundle). All commands except help and clean can be used with dizmo as a modifier.
Upon building a new dizmo, there will be a special config file placed in your project directory. It contains only _bundle_ as a key, which represents the bundle your dizmo belongs to. You can then add any other key dizmo supports in that file, and it will be placed into your Info.plist upon building of the dizmo.

**The config file provided needs to include the version of your project, otherwise the building of a dizmo will fail**.

Available Commands
------------------
```shell
grace help
grace [dizmo] new {projectname}
grace [dizmo] build
grace [dizmo] build:javascript
grace [dizmo] build:html
grace [dizmo] build:css
grace [dizmo] build:libraries
grace [dizmo] build:images
grace [dizmo] deploy
grace [dizmo] zip
grace clean
```
