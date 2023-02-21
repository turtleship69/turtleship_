#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this file is respinsible for compiling all markdown files into a Jekyll site to be hosted on github pages

import json
import os
import shutil
from pathlib import Path
import jinja2
import markdown
import yaml
from pprint import pprint

# every folder name starting with _ contains source files which need to be compiled, the folder name after _ is the path it is to be compiled to

# the following are the folders which contain source files
source_folders = ["_blog", "_fun", "_portfolio", "_projects"]

# the following are the folders which contain source files which are to be compiled to the root of the site
root_folders = ["_home"]


def Compile():
    # this function compiles all the source files into the _site folder
    # the _site folder is then copied to the root of the project and pushed to github pages

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("_templates"),
        # autoescape=jinja2.select_autoescape()
    )

    def blog():
        print("compiling blog\n\n\n")
        # this function compiles all the blog posts into the _site folder by inserting the compiled content into template.html

        # create a dictionary with the names of each group of blog posts as keys and the content of each group as values
        blog_posts = {}
        for folder in os.listdir("_blog"):
            if os.path.isdir("_blog/" + folder):
                blog_posts[folder] = []
                for file in os.listdir("_blog/" + folder):
                    if file.endswith(".md"):
                        blog_posts[folder].append(file)

        print(str(os.listdir("_blog")))
        print(blog_posts)
        os.mkdir("_site/blog")

        categoryList = []
        for category in blog_posts:
            categoryList.append(
                {"title": category, "href": f"/blog/{category}/"})
        print("category list" + str(categoryList))
        compiledhtml = env.get_template("blog_index.html").render(
            title="Browse all categories", links=categoryList)  # , subtitle=f""
        with open("_site/blog/index.html", "w") as s:
            s.write(compiledhtml)

        # iterate through each folder in the blog_posts dictionary
        for folder in blog_posts:
            # iterate through each file in the folder
            os.mkdir(f"_site/blog/{folder}")
            for file in blog_posts[folder]:
                # open the file
                with open("_blog/" + folder + "/" + file, "r") as f:
                    # read the file
                    blogPost = f.read()
                    # compile the markdown into html
                    compiledBlogPost = markdown.markdown(blogPost)
                    # insert the compiled content into template.html using jinja2
                    compiledBloghtml = env.get_template("blog_posts.html").render(
                        content=compiledBlogPost, links=categoryList)
                    # save the compiled file in the _site folder
                    # print(os.path.join(os.getcwd(), "_site", "blog", folder, file.replace(".md", ".html"))) # /home/runner/turtleship/_site/blog/misc/why.html
                    #open(os.path.join(os.getcwd(), "_site", "blog", folder, file.replace(".md", ".html")), 'a').close()
                    with open(os.path.join(os.getcwd(), "_site", "blog", folder, file.replace(".md", ".html")), "w") as s:
                        s.write(compiledBloghtml)

        """iterate though every folder and get a list of all posts in that directory and save it to a dictionary called links in the form
        {
            "category": [{"title": title, "link": link}, {"title": title, "link": link}],
            "category2": [{"title": title, "link": link}, {"title": title, "link": link}]
        }
        insert a title, subtitle, and list in the form {"title":title, "subtitle":subtitle, "link":[{"href":link, "title":title}]} into each folder in index.html using "indexTemplate.html" as a jinja2 template"""

        for category in blog_posts:
            links = []
            for file in blog_posts[category]:
                links.append({"title": file.replace(
                    ".md", ""), "href": f"/blog/{category}/{file.replace('.md', '.html')}"})
            compiledhtml = env.get_template("blog_index.html").render(
                title=category, links=links)  # , subtitle=f""
            with open("_site/blog/" + category + "/index.html", "w") as s:
                s.write(compiledhtml)
            print(links)

    def home():
        print("compiling home\n\n\n")
        # open directory.json
        # for each item in directory.json, if type is file, copy to site root, if type is page, compile and copy to site root
        with open("_home/directory.json", "r") as d:
            directory = json.load(d)
        for item in directory:
            if directory[item]["type"] == "file":
                shutil.copy("_home/" + item, "_site/" + item)
            elif directory[item]["type"] == "page":
                with open("_home/" + item, "r") as f:
                    content = f.read()
                compiledContent = markdown.markdown(content)
                compiledhtml = env.get_template("home.html").render(content=compiledContent)
                with open("_site/" + item.split(".")[0] + ".html", "w") as s:
                    s.write(compiledhtml)

    def projects():
        print("compiling projects\n\n\n")
        # load template.html from _projects folder and save it as a jinja2 template in memory
        #with open("_projects/template.html", "r") as template:
        template = env.get_template("projects_pages.html")
        os.mkdir("_site/projects")
        # go though every folder in _projects and look for a file called "project.yaml"
        # if a file called "project.yaml" is found, add the folder to a dictionary with the path of the folder as the key and the content of the "project.yaml" file as the value
        projects = {}
        for folder in os.listdir("_projects"):
            if os.path.isdir("_projects/" + folder) and folder[0] != ".":
                if os.path.isfile("_projects/" + folder + "/project.yaml"):
                    with open("_projects/" + folder + "/project.yaml", "r") as f:
                        projects["_projects/" + folder] = yaml.load(f, Loader=yaml.FullLoader)
        pprint(projects)
        """for each item in the dictionary, create a folder in the _site folder with the same name as the folder in _projects
        then create a file called "index.html" in the folder and save a rendered version of the template with the content inserted using jinja2
        title, subtitle, and cover are basic variables which are to be inserted into the template
        if preview type is static, embed the image linked in "preview" in the dictionary
        if preview type is animated, embed the video linked in "preview" in the dictionary
        if preview type is embed/iframe, create either an iframe or embed with a link to the url in "preview" 
        writeup.md should be rendered, then inserted into writeup in the template"""
        for project in projects:
            os.mkdir("_site/" + project[1:])
            preview = ""
            if projects[project]["preview"] == "na":
                preview = ""
            elif projects[project]["preview type"] == "static":
                projects[project]["preview"] = f'<img src="{projects[project]["preview"]}">'
                preview = projects[project]["preview"]
            elif projects[project]["preview type"] == "animated":
                projects[project]["preview"] = f'<video src="{projects[project]["preview"]}">'
                preview = projects[project]["preview"]
            elif projects[project]["preview type"].split("/")[0] == "embed":
                if projects[project]["preview type"].split("/")[-1] == "local":
                    # copy the file to the _site/project folder
                    shutil.copyfile(projects[project]["preview"], "_site/" +
                                    project[1:] + "/" + projects[project]["preview"].split("/")[-1])
                #projects[project]["preview"] = f'<embed src="{projects[project]["preview"]}">'
                preview = projects[project]["preview"]
            elif projects[project]["preview type"].split("/")[0] == "iframe":
                if projects[project]["preview type"].split("/")[-1] == "local":
                    # copy the file to the _site/project folder
                    shutil.copyfile(project + "/" + projects[project]["preview"], "_site/" +
                                    project[1:] + "/" + projects[project]["preview"].split("/")[-1])
                projects[project]["preview"] = f'<iframe src="{projects[project]["preview"]}" width="50%" height="500px"></iframe>'
                preview = projects[project]["preview"]
            # copy cover image to _site/projects/project folder
            cover = ""
            if projects[project]["cover"] != "na":
                shutil.copyfile(project + "/" + projects[project]["cover"], "_site/" +
                                project[1:] + "/" + projects[project]["cover"].split("/")[-1])
                cover = f"\n<img src=\"{projects[project]['cover']}\" alt=\"cover icon for {projects[project]['title']}\" width=\"50%\" height=\"50%\">"
            with open(project + "/writeup.md", "r") as writeup:
                projects[project]["writeup"] = markdown.markdown(writeup.read())
            with open("_site/projects/" + project.split("/")[-1] + "/index.html", "w") as file:
                print("Cover: " + cover)
                file.write(template.render(title=projects[project]["title"], subtitle=projects[project]["subtitle"],
                           cover=cover, preview=preview, writeup=projects[project]["writeup"]))
        # create a file called "index.html" in the _site/projects folder and save a rendered version of the template "_projects/indexTemplate.html" with the content inserted using jinja2
        # the content should be a list of all the projects in the form {"title":title, "link":link}
        #with open("_projects/indexTemplate.html", "r") as t:
        #    template = t.read()
        links = []
        for project in projects:
            links.append(
                {"title": projects[project]["title"], "href": f"/projects/{project.split('/')[-1]}"})
        with open("_site/projects/index.html", "w") as s:
            s.write(env.get_template("projects_index.html").render(
                title="Projects", links=links))

    # compile site
    blog()
    projects()
    home()


if __name__ == "__main__":

    # clear the _site folder
    if Path('_site').exists():
        shutil.rmtree("_site")
    os.mkdir("_site")

    Compile()
