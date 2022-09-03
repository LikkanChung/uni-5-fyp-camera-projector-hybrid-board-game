# Project Proposal
## Introduction
Intrinsic motivation is a well researched area in human psychology. A person is intrinsically motivated to complete a task if they act without any
obvious enternal rewards, i.e. an acitvity is done for the inherent satisfactions. They may also engage in activities if they percieve it to be a
learning experience or have an opportunity to gain some potential. Intrinsic motivation differs from extrinsic motivation in the regard that there is a
separate outcome, or has some instumental value.

As a result of the pandemic, many people have been turning to online video calls to facilitate social engagement, through activities like playing
board games. Video calls have been a vital tool for this as it has allowed friends and family to socialise with eachother while physically separated,
such as during the lockdown periods. However, an increased number video calls throughout one’s working day has meant that the lines have
blurred between work life and social life, meaning that people have become more tired and have decreased motivation to engage in social
activities (Rudnicka, 2020).

Playing board games in a fully digital domain follows the same problems as with prolonged video calls. Bailenson (2021) suggests 4 arguments
which may cause the fatigue phenomenon: excessive close-up eye gaze, increased cognitive load, increased self-evaluation from starting at one’
s self, and constrained physical mobility. These factors may have a significant role in the motivation of a person to engage with a board game
socially. While digital board games have long existed, not all games can be translated exactly from a physical to a digital domain without some
modifications to gameplay, or enjoyability (Kriz, 2020).

Hybrid games (a mix of technological and non-technological domains) are a solution to this. Implementation of hybrid games take many forms,
utilising technology in different and versatile ways (Kankainen, 2019), with many implementations using augmented reality using smartphones.
This, however, still relies on people being in the same physcial space, and does not allow people to play the same game together while physicaly
separated.

I would like to propose a solution which combines the social, digital, and physical domains which hybrid board games allow, but at the same time
allow the physical domains to be distincly separate. Using a camera-projector system, a physical board game with physical game pieces can be
augmented with networked software to allow players in separate physcial locations to play the same instance of a game with eachother.

### Motivation
**Hypothesis:** A hybrid board game allows socially distant players to be more instrinsically motivated to play, when compared to a solely digital
game.

The current approach to hybrid games relies on groups playing in the same physical spaces, which excludes people such as those living alone,
ones who need to remain socially distant, or reside in different countries.

Players also seem to enjoy factors which come along with physical interactions with a board game, such as the direct face-to-face contact, or
exchanging physical pieces and the haptic feedback that comes from that. Games are acting as facilitators to allowing a person to relax,
motivated by reducing stress, or as a learning tool (Kriz, 2020). This may be a factor which influnces a player to be intrinsically motivated to play
a particular board game.

This solution means that these groups of people will be able to enjoy the benefits of a physical board game, while also providing a way for
players who have only played online games to become more motivated to participate.

## Previous Work
Studies into intrinsic motivation for online games have been carried out previously. An analysis into intrinsic motivation within Massive Multiplayer
Online Role Player Games (MMORPGs) shows that while video games are primarily created for the purpose of entertainment, there are elements
of learning within. However, there are elements of MMORPGs which require players to think, plan, act critically, and strategise. The analysis
suggests that MMORPG design may create an engaging environment for learning, which may foster intrinsic motivation as players are able to
make decisions which involve choice, control, collaboration, as well as experience elements of challenge and achievement (Dicket, 2007).

Another study shows that customisability of the player’s avatar in games increases the perceived enjoyment. Many players invest time, and
money, into creating and equipping their character (Birk, 2016). This is a fundemental limitation to a physical board game, as often the piece
which a player choses to represent themselves is chosen from a set of differently coloured pieces.

On the side of board games, many hybrid implementations exist, but many rely on the use of mobile devices and screens. Most techniques use
some augmented reality to embellish the physical game, or rely on mobile devices to play the game, and use the physical environment around it
to add context (e.g. Pokemon GO).

Hybrid Monopoly (Park, 2017) achieves similar goals, implementing bidirectional communication between a mobile device as a controller and a
physical game set, and embeds RFID tags with the game pieces. However, as with previous examples, this game is played with players in the
same physical space.

## Proposed Solution
The solution, as described above, will aim to augment a physical game board with a camera-projector system. The camera is able to find and
track game pieces, using computer vision techniques. This will allow the projector to display a image on the board or playable area. If a blank
board is played with, then it means an abstract system can be developed which allows for multiple games to be played.

A game engine can be developed to be able to play different games, but in the first instance it will be tic-tac-toe, and then a more complex game
such as snakes and ladders can be implemented. This allows the project to be extensible and versatile in the future, so that it can be adapted to
play multiple games. The aim is to reduce the impact for a consumer, adding potential to become marketable.

Players will be able to connect the camera-projector system to a network, so that it can communicate with a server. If multiple players connect to
the server, then it allows multiple players to play a single game together. The game engines can control which turn is made, and moved pieces
can be either projected onto another player’s board, or a ‘movement instruction’ can be projected guiding another player to move the piece to
synchronise the game states represented by the physical board. This ofcourse means that a game’s progress can be easily tracked, which
means that there is potential so play competitively with leaderboards, or to same game progress for another time - somewhich which is more
delicate to do with physical only games.

The solution does not implement any sort of video call feature. The aim is to augment the gameplay experience, an alternative to current systems
such as http://boardgamearena.com, Tabetop Simulator, or Monopoly Plus. Players will need to use their own video-call software of choice, in
order to be able to commincate with their opponents during the game. It is also envisioned that this may be used as part of a larger social
gathering, where a group may engage with different activites, and not solely board games.

### Challenges
Low light conditions pose an interesting challenge for both the projector and camera. Low light may mean that for a low-cost projection system,
the image may be feint or hard to see for players. For a camera, low light may cause difficulties in colour or edge detection - making it difficult to
pereieve movement of pieces or distiguising between different pieces.

Perception of differently shaped pieces could also be challenging. In games such as chess, pieces may only be distinguishable if a camera has a
side-on view, which then may add in the parallax effect into the equation. Other games, on the other hand, may suffice with an overhead camera,
such as in checkers. Both can be played on the same board, but have different limitations and mechanics.

Hardware may also cause challenges. As this project is aimed as an alternative to a physical board game, or an online game (which is often
free), the hardware should be low cost. This puts limitations on what can be used as lower cost hardware generally tends to be lower quality,
which may create limitations in the definition of the camera or projectors, for example. Hardware projects naturally come with their own
challenges as well, as physical projects inherently have more risk associated with them.

### Methods
Game pieces may include the board itself, player tokens, and dice. Models have been developed in the past to be able to identify dice values.
Multiple techniques are known to be able to count the number of dice, from either using a CNN or a series of filters to count the numbers of pips
on the dice faces. This should be moderately straightforward to implement. However, I would need to do some more research into vision
techniques here. A webserver should also be moderately straightforward to implement, along with a game engine. I have done similar work in
Team Project in 2nd year, thought it may be time consuming.

The challenging work is creating the integrations between the different elements. The cameras, projectors, and client controller would need to be
intereconnected. A Raspberry Pi would seem to be an ideal way to implement this, so presumably some Python script would be best suited to
implement the controlling behaviour. An initial search suggests that libraries like OpenCV may be suitable for this.

The current hypothesis hopes to prove that this solution will help to mitigate the effects of video-call fatigue. To prove this, an experiment would
need to be run, measuring fatigue. As it is a recent phenomenon, little work has been conducted on the causes of the fatigue, and therefore it
may be difficult to measure and quantify. This is the most significant issue at present. (*Note: This may mean that the hypothesis needs some reworking.*)

## Milestones
In order to build the proposed solution (with initial target deadlines):
1. Develop a game engine and web server which is able to play a simple game (tic-tac-toe, for example) between two web clients. (end S1W5)
2. Implement a projector system which is able to duplicate the game state onto a physical board. (end S1W6)
3. Implement a camera system which is able to verify a physical game state is synced with the game server. (end S1W8)
    1. Implement the client being able to make movement suggestions to match the game server’s state.
4. Adapt the camera system to be able to identify a player has made the move, and update the server’s state. (end S1W12)
    1. This will then allow the other player to synchronise the game on their board.
5. Implement a more complex game, such as snakes and ladders (end S2 W3)
    1. This will include enumerating dice rolls.
6. Conduct tests to validate the hypothesis. (Throughout rest of S2)

## References
Ryan, R.M. and Deci, E.L., 2000. Intrinsic and extrinsic motivations: Classic definitions and new directions. Contemporary educational psychology,
25(1), pp.54-67.

Rudnicka, A., Newbold, J.W., Cook, D., Cecchinato, M.E., Gould, S. and Cox, A.L., 2020, August. Eworklife: Developing effective strategies for
remote working during the COVID-19 pandemic. In Eworklife: developing effective strategies for remote working during the COVID-19 pandemic.
The New Future of Work Online Symposium.

Bailenson, J.N., 2021. Nonverbal overload: A theoretical argument for the causes of Zoom fatigue. Technology, Mind, and Behavior, 2(1).
Kriz, W.C., 2020. Gaming in the Time of COVID-19.

Kankainen, V. and Paavilainen, J., 2019. Hybrid Board Game Design Guidelines. In DiGRA Conference.

Dickey, M.D., 2007. Game design and learning: A conjectural analysis of how massively multiple online role-playing games (MMORPGs) foster
intrinsic motivation. Educational Technology Research and Development, 55(3), pp.253-273.

Birk, M.V., Atkins, C., Bowey, J.T. and Mandryk, R.L., 2016, May. Fostering intrinsic motivation through avatar identification in digital games. In Pr
oceedings of the 2016 CHI conference on human factors in computing systems (pp. 2982-2995).

Park, J.W., 2017. Hybrid monopoly: a multimedia board game that supports bidirectional communication between a Mobile device and a physical
game set. Multimedia Tools and Applications, 76(16), pp.17385-17401.