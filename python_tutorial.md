# Learn How to Code

Want to write code for Baxtabot but never learned how? 

## I've Never Coded Before

If you've never coded before, and aren't going to as part of your degree any time soon, would recommend going through [this full Python tutorial](https://www.youtube.com/watch?v=rfscVS0vtbw) video: 

## I'm studying Computer Science / Software Engineering / Data Science / Engineering

The following UNSW courses teach programming skills which are really helpful for Baxtabot:

* COMP1511 / COMP1911 Programming Fundamentals - teaches you how to code and problem solve, it doesn't teach Python but is really easy to learn Python once you've done this course
* ENGG1811 Computing for Engineers - Teaches programming in python
* COMP1531 Software Engineering Fundamentals - builds on COMP1511 and teaches Agile programming practices for software projects and Python. Baxtabot is pretty much made based off concepts from this course
* COMP3311 Database Systems - teaches databases and SQL. This course is really helpful if you want to work on the Baxtabot DB as it runs on teh same framework (PostgreSQL)
* COMP2521 Data Structures & Algorithms - teaches problem solving with algorithms. Helpful if you want to write a new function which requires some algorithmic processing!

## Python Fundamentals

The following videos are recordings of lectures from the first 4 weeks of COMP1531 and cover:

* [Introduction to Python](https://www.youtube.com/watch?v=Q0nj3edifbQ&feature=youtu.be)
* [Testing](https://www.youtube.com/watch?v=R5xAXHZGS84)
* [Dictionaries](https://www.youtube.com/watch?v=K1p0c857FpE)
* [Global variables](https://www.youtube.com/watch?v=BQ98I2IWT4E&feature=youtu.be)
* Importing and paths, [part 1](https://www.youtube.com/watch?v=z_GUxotui50), [part 2](https://www.youtube.com/watch?v=sVLnzM2tYpI)
* [Packages](https://www.youtube.com/watch?v=aTL1g6PLGzw)
* [Exceptions](https://www.youtube.com/watch?v=LJosvNVXhLQ)
* [Objects](https://www.youtube.com/watch?v=L5UhVGX6rDU&feature=youtu.be)
* [Pythonic coding](https://www.youtube.com/watch?v=8tj6W2_va8U)
* [Pylint](https://www.youtube.com/watch?v=zjFPa9jRP58&feature=youtu.be)
* HTTP and Flask, [part 1](https://www.youtube.com/watch?v=MQUv0PwqjG0&feature=youtu.be), [part 2](https://www.youtube.com/watch?v=JBeFZd0pIRM)

These videos are pretty long so you can skip some parts to where there's the coding.

## Git Fundamentals

You'll also need to know how to use Git. The following videos teach Git:

* [Introduction to Git](https://www.youtube.com/watch?v=A46dQSmse0g&feature=youtu.be)
* [Git Branches and Merge Requests](https://www.youtube.com/watch?v=f7NAUI2VrV0)

## Confirmatory Python Exercises

Here are a few challenges to test/revise your Python skills.

### 1. Fair Dinkum Duplicates

Each person that migrates to the country Dmojistan is tagged with an id number, then they must give their id number to the customs officer. However, some migrants say someone else’s number to cheat their way in. Write a program which takes an integer N, followed N lines of input, one integer per line. Your program should output FAIR DINKUM if there are no duplicates. If there are duplicates, your program should output DUPLICATE/S!!! Your program should work in the following fashion.

Sample Input 1

```
5
1
2
3
4
5
```

Sample Output 1

```
FAIR DINKUM
```

Sample Input 2

```
5
1
2
3
4
4
```

Sample Output 2

```
DUPLICATE/S!!!
```

### 2. The Baxter Election


In an imaginary college also called Philip Baxter in the UK, the president is elected every 5 years, the treasurer is appointed every 3 years, the Director of Computer Science is elected every 6 years and the Chief Librarian is replaced every 7 years. This year, X, all of the positions were changed over. This is highly unusual. Your task is to quantify how unusual this is. Write a program which takes a year X as input and the future year Y, and inputs all years between X and Y inclusive when all positions change. 

Sample Input 1

```
2016
2616
```

Sample Output 1

```
All positions change in year 2016
All positions change in year 2226
All positions change in year 2436 
```

### 3. 16 Bit S/W Only

One day you woke up, finding yourself back in 1992. It would seem that the gypsy wife of the wizened old monk whose voodoo shop you smash up every day after school has cast a spell on you. Early in the production process of the 80386, Intel discovered a fatal bug in the processor, which they of course fixed. The bug involved errors when performing 32-bit multiplication. But by the time they fixed the issue, a number of processors were already produced, and they decided that it would be a shame to throw them all out. It was decided that these processors would be sold at a reduced price with the tag 16 BIT S/W ONLY (16 bit software only). Conversely, the newer processors which don't have the bug instead have two sigmas (ΣΣ) stamped on. We will call them DOUBLE SIGMA processors.
Back in 1985, 32-bit software was something out of reach of most consumers. Even in 1989, the ancient 8086 was sold as new technology. Hence, there is a market for the defective processors. You, a programmer, decided to get a programming job in the 1992 world so you can survive until you find a way to return to the modern age. In a cluster of servers, some of them use the 16 BIT S/W ONLY processors, but you don't know which ones. Your first job is to determine the bad processors from the 32-bit multiplication results.
The 80386 has an instruction to multiply two 32-bit integers into a 64-bit result, conventionally stored in EDX:EAX register (i.e. temporary variable) pairs because there were no 64-bit registers.

The first line of input will be the integer N such that
1≤N≤1000. The next N lines of input will contain integers A, B, and P. For every line of input except the first, output 16 BIT S/W ONLY if the product is wrong, or POSSIBLE DOUBLE SIGMA if correct.

Sample Input 1

```
3
1 1 2
2147483647 2147483647 4611686014132420610
12345678 87654321 1082152022374638
```

Sample Output 1

```
16 BIT S/W ONLY
16 BIT S/W ONLY
POSSIBLE DOUBLE SIGMA
```

### 4. Scrabble Score

Scrabble is a game where players get points by spelling words. Words are scored by adding together the point values of each individual letter (we'll leave out the double and triple letter and word scores for now). Write a function scrabble_score which takes a word and prints the score for that word. You should use the following dictionary of mappings to complete this problem. Assume your input is only one word containing no spaces or punctuation, and it should be case insensitive 

```
score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, 
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3, 
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1, 
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, 
         "x": 8, "z": 10}
```

Sample Input & Output:

```
>> scrabble_score(‘harambe’)
14
>> scrabble_score(‘informaticsIsAwesome’)
32
```

## Advanced Concepts

Feeling confident? Try some more advanced topics.

* [Continuous Integration](https://www.youtube.com/watch?v=7cfJx088UX0&feature=youtu.be)
* [How to fake git history](https://www.youtube.com/watch?v=VcSIFTewQ6k)
* [Property based testing](https://www.youtube.com/watch?v=TcylCeABQlE)
* [Git Rebasing](https://www.youtube.com/watch?v=BCDCAEU0qSM&feature=youtu.be)
* [Deployment with heroku](https://www.youtube.com/watch?v=vP-VQErS7_o&feature=youtu.be)


