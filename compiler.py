#!/usr/bin/env python
# -*- coding: utf-8 -*-

#this file is respinsible for compiling all markdown files into a Jekyll site to be hosted on github pages

#from curses.ascii import isdigit
import os
import sys
import re
import shutil
import subprocess
import datetime
import time
import json
import argparse
import glob
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import markdown


#every folder name starting with _ contains source files which need to be compiled, the folder name after _ is the path it is to be compiled to

#the following are the folders which contain source files
source_folders = ["_blog", "_fun", "_portfolio", "_projects"] 

#the following are the folders which contain source files which are to be compiled to the root of the site
root_folders = ["_home"]


def Compile():
    #this function compiles all the source files into the _site folder
    #the _site folder is then copied to the root of the project and pushed to github pages

    def blog():
        #this function compiles all the blog posts into the _site folder by inserting the compiled content into template.html

        with open("_blog/template.html", "r") as t:
            template = t.read()

        #create a dictionary with the names of each group of blog posts as keys and the content of each group as values
        blog_posts = {}
        for folder in os.listdir("_blog"):
            blog_posts[folder] = []
            if os.path.isdir("_blog/" + folder):
                for file in os.listdir("_blog/" + folder):
                    if file.endswith(".md"):
                        blog_posts[folder].append(file)

        print(str(os.listdir("_blog")))
        print(blog_posts)

        #iterate through each folder in the blog_posts dictionary
        for folder in blog_posts:
            #iterate through each file in the folder
            for file in blog_posts[folder]:
                #open the file
                with open("_blog/" + folder + "/" + file, "r") as f:
                    #read the file
                    content = f.read()
                    #compile the markdown into html
                    content = markdown.markdown(content)
                    #insert the compiled content into template.html
                    content = template.replace("{{ content }}", content)
                    #save the compiled file in the _site folder
                    print(os.path.join(os.getcwd(), "_site", folder, file.replace(".md", ".html")))
                    open(os.path.join(os.getcwd(), "_site", folder, file.replace(".md", ".html")), 'a').close()
                    with open(os.path.join(os.getcwd(), "_site", folder, file.replace(".md", ".html")), "w") as s:
                        s.write(template)


    def home():
        #iterate through all files in _home folder and compile them to the root of the _site folder
        #all files are to be compiled and replace the "{{ content }}" placeholder in the template.html file
        with open("_home/template.html", "r") as template:
            template = template.read()
        for file in os.listdir("_home"):
            filename = os.fsdecode(file)
            if filename.endswith(".md"):
                with open("_home/" + filename, "r") as content:
                    content = markdown.markdown(content.read())
                with open("_site/" + filename[:-3] + ".html", "w") as file:
                    file.write(template.replace("{{ content }}", content))
                continue


    #clear the _site folder
    shutil.rmtree("_site")
    os.mkdir("_site")

    blog()
    home()



if __name__ == "__main__":
    Compile()