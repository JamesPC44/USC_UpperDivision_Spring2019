# Help Make Mr. Blobsworth A Star

Help Mr. Blobsworth go from being just a small town blob to a world wide star.
His master plan for accomplishing this is to win the Olympic gold medal for
wriggling. Wriggling is a sport which involves contorting ones body to move
quickly through a narrow maze to reach a goal. Fortunately, Mr. Blobsworth,
being an amorphous blob, is a natural born wriggler. A particular wriggling course
can be represented as an $n$ by $n$ grid, of which Blobsworth's body takes up
$m$ squares. Blobsworth body can take on any shape, so long as his body remains
connected through adjacent grid cells. 

Mr. Blobsworth measures time in blips and knows has two moves: sliding and
stretching. Sliding takes one blip and translates Blobsworth up, down,
left or right. For example, if Blobsworth body looks like

____
_BB_
__B_
____

He can slide to

_BB_  or ____ or  ____ or ____
__B_     BB__     __BB    ____
____     _B__     ___B    _BB_
____     ____     ____    __B_

Stretching takes Blobsworth two blips and involves moving one square of his
body so that his whole body remains connected. This allows Blobsworth to
change his shape and move around tight corners. For example, if Blobsworth's
body looks like

____
_BB_
__B_
____

He can stretch to

____  or __B_ or  _B__ or ____
_BBB     _BB_     _BB_    BBB_
____     ____     ____    ____
____     ____     ____    ____

____  or __B_ or  ____ or ____
_BB_     __B_     __BB    __B_
_B__     __B_     __B_    __BB

____     ____     ____
____  or ____ or  ___
__B_     __B_     _B__
__B_     _BB_     _BB_
__B_     ____     ____

## Input Format
The first lines contains $n$ and the second line contains $m$. The next $n$ lines
each have $n$ characters corresponding to the grid of a particular wriggling course.
The character "\_" denotes an empty cell. The chacter "B" denotes a cell in
which Blobsworth's body starts. The character "\*" denotes a cell which
contains an obstacle.  The character "G" denotes the goal cell.

## Output format
The output should be a single line, which contains the minimum number of blips
in which Blobsworth can reach his goal.

## Input Constraints
$1 \le n \le 30$
$1 \le m \le 10$

## Sample Input
5
3
BB___
_B___
_****
_____
****G

## Sample Output
13

## Explanation

The following shows shortest sequence which brings Mr. Blobsworth to the
goal, along with corresponding time in blips.

blip = 0  
BB___  
_B___  
_****  
_____  
****G  

blip = 2  
BB___  
B____  
_****  
_____  
****G  

blip = 3  
_____  
BB___  
B****  
_____  
****G  

blip = 5  
_____  
B____  
B****  
B____  
****G  

blip = 7  
_____  
_____  
B****  
BB___  
****G  

blip = 9  
_____  
_____  
_****  
BBB__  
****G  

blip = 10  
_____  
_____  
_****  
_BBB_  
****G  

blip = 11  
_____  
_____  
_****  
__BBB  
****G  

blip = 13  
_____  
_____  
_****  
___BB  
****B  
