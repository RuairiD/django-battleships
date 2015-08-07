![Could not fetch build status.](https://travis-ci.org/RuairiD/django-battleships.svg?branch=master)

# django-battleships
A multiplayer game of Battleships using the Django framework.

### What do I need first?
Nothing much, just Python 3+ and (ideally) virtualenv.

### How do I start it?
Clone the repo, `cd` to the repo directory then run (again, ideally inside a virtualenv):

```sh
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

### How do I play?
Assuming you're using the default templates and not rolling your own, go to `localhost:8000` and also direct your friends/foes to the correct IP address. Have everyone signup and login using the links from the homepage. Once that's done, someone head to `/games/create_game`, enter everyone else's usernames and then you can start pretending to blow each other up. When it's your turn (order goes from left to right), select your target player and the co-ordinates, then click `Shoot!`. Rinse and repeat until one player stands victorious in a sea of shipwrecks and shrapnel.

### I don't know how to play Battleships.
Really? [Check it out.](http://www.cs.nmsu.edu/~bdu/TA/487/brules.html)

### Isn't it called _Battleship_? Not _Battleships_?
So they say, but there's more then one battleship in the game. Makes no sense. I'm calling it _Battleships_.

### Shouldn't Battleships only have two players?
Yeah, it should but I wanted to write a flexible application that could handle an arbitrary number of players with some grace. You could have a 32 player battle royale if you felt like it. I recommend sticking with classic two player though. In any case, [players are of course required to make their own sound effects during gameplay.](https://www.youtube.com/watch?v=dVYa-VbIeDY)
