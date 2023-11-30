For those who prefer a video resource, installation and usage can be found on AnthonyWritesCode's youtube channel here: https://www.youtube.com/watch?v=CZZLCeRya74

Otherwise:

1. Create a virtualenv
```
pip install virtualenv

virtualenv aoc
```

2. Activate the env, for windows:

```
.\aoc\Scripts\activate
```

for mac:

```
source aoc\bin\activate
```

3. install requirements
```
pip install -r requirements.txt
```

4. add your session cookie
Create a .env file in the base folder and add the text
```
session=blablabla
```
replacing blablabla with the session cookie you get from advent of code (https://adventofcode.com/)
Do this by logging into advent of code using your preferred method, then right click the background, inspect, then:

a. on Firefox: Storage -> Cookies -> https://adventofcode.com -> copy the session value

b. on chrome: Application -> Storage -> Cookies -> https://adventofcode.com -> copy the session value

5. Create a folder for the current day
Copy the day00 folder and update the 00 to the appropriate 2 digit day for each problem.

6. Download input
Change directory into the new folder and run
```
aoc-download-input
```

7. Solve problem

8. Test your solution against the sample input
Update the INPUT_S and EXPECTED in part1.py to match the information provided in the puzzle, then run
```
pytest part1.py
```

8. Once the problem has been solved, submit your answer using
```
python partx.py input.txt | aoc-submit --part x
```
updating x as appropriate