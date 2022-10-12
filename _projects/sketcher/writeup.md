## History
This was originally created for [replit creates](https://creates.replit.com/), a month long challenge where you're given a new prompt everyday, and need to make anything to for said prompt.  
On the 11th day, the prompt was "Self-portrait", and I had the idea to make an app which converts a photo into a sketch.  
After a *an amount of work*, I had [found a script](https://python.plainenglish.io/convert-a-photo-to-pencil-sketch-using-python-in-12-lines-of-code-4346426256d4e) to do the conversion.  
Then came the fun part.  
  
I knew the best way to make a UI was to make a web app, so I made a [replit](https://replit.com/@nathanmachane/portrait-to-sketch) and started working on it.  
Armed with experience in flask, and basic html knowledge, it was pretty simple to make the first draft of the website, however, there were several things I wanted to improve before I was satisfied. 
  
Firstly, I wanted to remove the storing of images on the server for a few reasons. In order to do this, i needed a way of passing the image to opencv without saving it to a file, and a way to send it back from memory.  
Passing the image to opencv should have been easy enough, but my dumb ass was passing an image object to a function that tries to open a local file, all i needed to do was swap `cv2.imread()` with `cv2.imdecode()` and it worked. 

Eventually, I started researching serverless functions, and realised it was a better solution as it could scale, and didn't require a server that was active all the time. The original version on replit would go to sleep after 30 minutes of inactivity, and would take a **good** few seconds to wake up, which was annoying every time I wanted to try one picture.  
I settled with azure functions, as they were free for students, and supported python (*cough cough\* netlify *cough cough\*). After way too long of trying to figure out the serverless fuction api, I realised I was overcomplicating things. I went back to my original flask app, and added ported the function from there. [Never rewrite code from scratch](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/). 
  
Then came the html to access the function...  
I want to die.  
I had to use a form to send the image, and then use javascript to send the image to the function, and then display the result. Or so I thought.  
THE PREVIEW IS IN AN IFRAME FFS. I CAN JUST CHANGE THE IFRAME URL.  
Here's the thing: the url I need to send the form data on takes a post request. I was trying to use JS to embed the responce by editing the html, then by having a hidden image which shows itself- why? It's an iframe.  

Anyway I'm an idiot, I spent way longer than I needed to on this, over way too long, I'm done. ~~Besides, I still need to write the blog compiler.~~ 