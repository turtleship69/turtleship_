## Intro
So I decided to make a website. Well another one. I guess it can't hurt?  
I guessed wrong.  

If you're curious, you can check out shit code [here](https://github.com/turtleship69/turtleship69.github.io) Just don't ask about the commit names. Don't...  

## The idea
I wanted to make a website that would be able to display my projects as well as have a blog and a few other random stuff. Inspired by my [friend's website](https://www.revisionland.com), I thought I'd write the whole thing in markdown and use a static site generator to convert it to html. HTML would've been easier.  
Very quickly I realised each section would require a custom "compiler". Quotation marks because it's not really being compited but rather converted from markdown to html. Read on for a "brief" explanation of each.  

## The blog
This was fairly ~easy~ simple. I just needed to make a page that would display all the posts in a list and a page for each post. I just iterate though a folder of (folders of) markdown files and convert them to html, with a predefined html template and jinja2. 

## The projects
This was the most complicated part. (So far...) I wanted to be able to display the projects in a list and have a page for each project. I also wanted to be able to have a description.  
Each project gets a folder in the projects folder. The folder contains a yaml file with all the details needed to generate the page and a markdown file with the description. They are formatted as follows:  
```yaml 
title: "Project title"
subtitle: "Project subtitle"
cover: "cover.jpg"
preview type: "image", "embed" or "video"
preview: "preview.jpg", "preview.mp4" or "preview.html"
``` 
I then run though all folders in the projects folder and generate a page for each one. The page is generated using a jinja2 template and the yaml file. 


## Next steps 
This website is stil under construction, and in very early stages. As the website 