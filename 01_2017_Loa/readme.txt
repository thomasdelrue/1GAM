Readme
======

Thanks for trying out this game.

I'd had a lot of fun making it for my january entry
for One Game A Month, although it's pretty unfinished
to be any good.

It's player vs computer. You drag and drop your stones.
The computer takes a 7.5 seconds thinking about its next
move. The AI(1) is still extremely easy on my PC and easy to beat.

I hope it provides a bit more of a fun challenge on some better 
hardware. At least thank you for taking the time to have a look at it.

I hope to improve the game at some future date, as to make it challenging
for every type of level of play. Any remarks, feedback or suggestions
are welcome.


thdelrue


(1): AI consists of bitboards, MCTS with an evaluation function.
Though it still doesn't play enough simulations to explore the
search space sufficiently to play well on my PC.
There's also persistence, in the sense that winning moves are saved
at the end of each game, and loaded at the beginning of every game,
so that the MCTS should gradually perform better the more you play.

