# STAGE 0_HackBio-Internship-Coding-for-Life-Sciences
This repo contains a Python script to organise and display Team Glycine 001 members' details.

## Task
Use any data structure of your choice to organise the following information:
- Your names
- Your Slack username
- Your email
- Your hobby
- Your countries
-Your discipline
- Your preferred programming language

Don’t use functions, loops, conditionals or any complex concepts
Your code should include a final print statement that prints the organised output logically and understandably.

## Code Features
- This project was done using a **nested dictionary**. Outer keys (a, b, c, d, e) uniquely identified each team member. Inner keys (name, slack username, email, hobby, country, discipline, preferred programming language) were used to store members details
- The output was formatted using f-strings to insert values from the dictionary into the output and escape characters for line breaks and blank lines between member details to ensure readability.
- The final output combines a header with the formatted details string.
