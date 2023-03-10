# CS50 MEET
#### Video Demo:  <URL HERE>
#### Description:

      Hello and this is my **CS50 final project** which I am going to cover in detail, explaining the idea behind the project and how it will change the way you take the CS50 course online/in-person. If you are taking the Harvard CS50 course and you feel like you're alone, you don't have any friends to connect with and take the course 
with, well CS50 MEET is here for you. 
  
  ### THE GOAL
      The goal of this project is to bring all CS50 students together to connect, make friends, socialize, and help each other throughout the course, especially for those who are in different parts of the world and might feel alone and don't have anyone to talk to. This helps to cancel out the possibility of not being able to socialize well with other coursemates.
      I see this as a journey, not one person can take alone, for "no one is an island" as the famous quote says, plus we operate at our best when we work together. So you need others with you on this journey.
      While I was taking the course myself, I took it alone but it would have been better if I had someone to explain all my problems to concerning the course projects and lectures, you know to brain-storm and get things right with the help of another, I know I didn't build this entire project on my own(if I did, I wouldn't have gotten this far honestly), but with the help of my friend(who is not a CS50 student), I was able to learn a lot from him and implement some new ideas into my project and only then did it get really fun, LOL. So I hope to change that by the implementation of this Project and I hope it does change.
  
So all that being said, let me explain what each page on the web app does.
      
  ### firstpage
      The first page/route on the webpage is called "first-page", in the HTML file, it's called "firstpage.html". I named it that because it's the first page you'll see when you type in the project's URL.
      This page contains a summary of what CS50 MEET is and what it does for those who are just logging in for the first time. Underneath the summary, there's a button there that says "JOIN", clicking that button would redirect you to the second page/route called "login_register".
      
  ### login_register
      This page as the names state contains the login and the registration forms which will be required to log into your account or if you're just joining, to register you into the database. This page contains a bit of Javascript code which is used to make the cool effect of switching between the login and the registration form.
After a new user registers him/herself in the database, an instant redirect occurs which redirects you to a new page/route called "hobbies"
  
  ### hobbies
      This page/route was supposed to be called "personality" (because it contains a list of different traits and personalities of a person), but it was too long, I just wanted to shorten things out, so don't mistake things here, those are personality traits, not hobbies.
      So this page contains 30 personality traits questions with levels to which are true about you, ("Totally Agree", "Somewhat Agree", "Neutral", "Somewhat Disagree" and "Totally Disagree"). So you'd pick to answer each question according to the levels stated just now. After you answer every question, click the "next" button below the page and you'll be redirected instantly to a new page/route called "interests". NOTE: the questions on the page are tested and proven questions gotten from trusted sources.

  ### interests
      The information on this page is similar to the previous one(hobbies) as you'd be required to pick your interests, unlike the hobbies page you are only required to pick out of everything, but if you feel you are interested in everything too(which can be rare to find), you can certainly pick all, LOL.
      
  ### profile
      This is the profile page where you get to add your picture(which will be public to all users in the app), nothing much. After clicking the "create profile button", you'll be redirected to the next page/route called "match".
      
   ### match
      Now this page is considered to be straightforward as it only contains one button that clearly says to "Find Match" which is going to redirect you to the profile page where you can see all students you've been matched with. If you want to know how you get perfectly matched with other character-like students, read below.
      
   #### How does the match Algorithm work?
      The Algorithm cannot work without data(meaning there has to be data read into the algorithm for it to work), that data consists of the answers to the personality traits questions and your interests which you picked on the interest page. Because humans connect better and faster with those of similar traits and interests with us this Algorithm matches you with those that have >=70% of the traits and interests you have answered and picked in the previous pages. This means that you are most likely to make friends that have almost everything in common with you, isn't that amazing?
      
   ### CHALLENGES AND SETBACKS
      These are the challenges and setbacks I had while working on this project.
      1. Interface design:
            This was an almost major setback for me as I did not know any frontend tools or how to use and work with them, so I had to use pure CSS which was stressful and frustrating and at the same time impactful, as I got to learn some new CSS concepts that I didn't know existed, Lol. I leveraged videos from Youtube, Stack Overflow, Google, etc.
      2. Quering into the database:
            I had a lot of issues with this one, moving the project's server-side from sqlite3 to MySQL was one of them and it was frustrating because we didn't dive that deep into other databases aside from sqlite3, and how to connect and use them with your code, this I had to learn with the help of external sources like Youtube, Stack Overflow, Google, etc.
            Another one was getting, updating, inserting, and posting user inputs into and from the database which was stressful and tiring as I tried many times, but got a lot of errors, it was HELL trust me, LOL.
      3. Debugging:
            As developers, we all know how problematic debugging can be and how we always try to avoid them, at least me in this context. Debugging the code was not an easy task, I had to rewrite some parts of the project back from scratch, which was very annoying. And I must say, debugging is a very good practice as it allows you to find errors you never knew were there and it also helps you to think about how to better optimize your code in terms of design or running time, so always debug.
      4. The match algorithm(of course, LOL):
            This was a minor setback honestly as the algorithm needs user data to work and the algorithm was the last thing I worked on which means that every other part of the code was working fine already. So it was a little easy to implement.
      
    
### Thanks and appreciation
      First of all, I want to say a very big thank you to [David J. Malan](https://www.linkedin.com/in/malan/) for this wonderful opportunity and to be part of this journey, it was really exciting, richly impactful, and very challenging also, LOL. It has been an honor to learn from one of the best minds in the field of computer science. I also want to thank the instructors [doug loyd](https://www.linkedin.com/in/douglaslloyd/) and [brian yu](https://www.linkedin.com/in/brian-yu/) for their impactful and comprehensive run through and breakdown of the lectures and problem sets. Thank you once again.
      And lastly, I want to thank my friend [rehoboth micah-daniels](https://github.com/AlleyER16) for helping me with this project also.
      
      
So that's all about my project's description, I hope it was fun reading through and I hope it has inspired you to go on and build your project, whatever it might be. Thanks for reading through.

       
      
