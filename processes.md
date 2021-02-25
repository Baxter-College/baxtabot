# Baxtabot Team Development Processes

This is a rough outline of how features/defects are coded up. Please follow this process so we can make sure Bbot stays working around the clock!

## 1. Requirements Analysis

* If it's a defect, the requirement is pretty straightforward
* If it's a new feature, come up with some user stories that describes what you want out of the feature `As a <type of user> I want <some thing> so that <some reason>`
* Usually we'll do this together in a meeting
* If it's not done already, create a new issue, link it to the Project Taskboard and assign yourself

## 2. Design

* Come up with a design of how you're going to solve the problem in a word doc, including
    * What modifications/additions you're going to make to the codebase
    * How you will unit test your code
    * The success and fail/error conditions for your functionality
* Send the doc to Nick for review

## 3. Coding and Testing

* Checkout a new branch called yourname/featurename
* Write a stub function for the code (if creating a new function)
* Write a failing unit test(s) inside the respective test file
* Write the code so that the unit test passes
* Force push your changes to `dev` (make sure no one else is also working on it!) and acceptance test your new feature (play around with it on `dev` and see if anything breaks)

## 4. Deployment

* Once you're happy with everything, make a pull request and assign Nick as a reviewer
* Link the pull request to your issue
* Make sure that any merge conflicts with `master` are resolved
* After the code review you can merge in your new feature into `master`
* Presto!
