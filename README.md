grace
=====

*DOES NOT WORK COMPLETELY YET! PLEASE ONLY USE TO TEST OR TRY OUT! THIS NOTICE WILL BE REMOVED AS SOON AS I THINK IT REACHED A PRODUCTIVE POINT.*

**Grace** is a development toolkit for JavaScript, HTML and SCSS (Sass CSS).
The name **grace** comes from a sweet puppy, which is always coming to my room whenever I start working to get the little attention that is left.

What Does It Do?
================

**Grace** enables you to write proper JavaScript without worrying about concatenating your classes together or having to deal with other problems. There is also a built in SCSS parser, so you can write nice CSS and don't need to convert it on your own, **grace** does that for you.
The goal is that you do not have to worry about things going on around your project, but that you an concentrating on writing pure JavaScript and HTML.

How It Works
============

Install
-------

To install grace, pull it from github create an alias for the respective executable in your shell rc file. I provide a compiled binary for debian wheezy 64 bit and Ubuntu 12.04 64 bit. At a later point I will try to incorporate more OS's and more distributions. If someone is willing to take up this task, feel free to make a pull request. You can also reference the executable.py, but then you need to have the respective python libraries installed.

Setup
-----

The first step would be to create a new project. This can be done by invoking grace with the parameter new and an optional project name. If the project name is ommitted, it will be set to _MyProject_.
```shell
grace new YourProjectName
```
This create a new folder in your current folder with the correct structure and files needed. From here on you can go to your folder and start using **grace** from in there.

Building Your Project
---------------------

To build your project, you have to invoke grace with the build task. You can also specify what exact build step you want to execute.
```shell
grace build
```
or
```shell
grace build:javascript
```

Available Commands
------------------
```shell
grace help
grace new [projectname]
grace build
grace build:javascript
grace build:html
grace build:css
grace build:libraries
grace build:images
grace clean
```
