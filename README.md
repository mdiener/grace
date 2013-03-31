grace
=====

**Grace** is a development toolkit for JavaScript, HTML and SCSS (Sass CSS).
The name **grace** comes from a sweet puppy, which is always coming to my room whenever I start working to get the little attention that is left.

What Does It Do?
================

**Grace** enables you to write proper JavaScript without worrying about concatenating your classes together or having to deal with other problems. There is also a built in SCSS parser, so you can write nice CSS and don't need to convert it on your own, **grace** does that for you.
The goal is that you do not have to worry about things going on around your project, but that you an concentrating on writing pure JavaScript and HTML.

How It Works
============

Setup
-----

The first step would be to create a new project. This can be done by invoking grace with the parameter new and an optional project name. If the project name is ommitted, it will be set to _MyProject_.
```shell
grace new YourProjectName
```
This create a new folder in your current folder with the correct structure and files needed. From here on you can go to your folder and start using **grace** from in there.

Building Your Project
---------------------

To build your project, you have to invoke grace with the build task. The build task takes two options: project and test. If you ommit both, both will be built after each other. The project option will build your project and allow
