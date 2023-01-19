## Find a time to meet with your group that works for everyone
I'd had this idea on my mind for a while, but after a few months of trying to plan a reunion with my old [yearbook committee](/blog/the%20story%20behind/Yearbook.html) and chronic weekend bordem, I decided to implement it. 

## Basic overview
### UX 
You can create an event, and share the link with your friends. They can then join the event, and say when they are free. The server will then show you when everyone is free. 
Or you can join an event, and say when you are free. The server will then show you when everyone is free. 
### Implementation
There's a massive dictionary of all events. When a new event is created the event creator is the first member in the group. When the link to the event is shared, the server first checks if the user has a session cookie.  
If not, they are a new user, and asked when they are free. If they do, the server checks if said cookie has already joined the event.  
If not, they are asked when they are free.  
If yes, they are shown the the times that everyone has said they are free.  

## The code
As usual, the code is on [GitHub](https://github.com/turtleship69/group-planner). Feel free to contribute :)