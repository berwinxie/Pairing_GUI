#PAIRING GUI and SHEET ORGANIZER

This repository is the initial workings of an interface to simplify the
pairing process for Open Ears. People who are seeking help are nicknamed
'warriors' to simplify the coding and members of our organization who 
are giving the help are 'friends.'


##THE PROCESS

Let's start with the friends. If a friend has gone through training and
has been verified, they can then add themselves to a 
queue from the /add page. Once they add themselves to the queue we will
know they are available to help a certain amount of people
(however many they put down). At any point, they may remove themselves 
from this queue. This will let us know that they are not capable of being
paired with anymore warriors at the moment for whatever reason. Be it school
work is piling up, they are beginning to feel mentally drained, etc.

Now, there is also a list of people who want to be helped, warriors. All warriors
on this list are automatically added to the queue, setting them up to 
be helped by a friend.
Someone in the commmittee will see both the queues and pair someone in the 
warrior queue with someone in the friends queue. This removes both people from
the queues and adds them as a pair to the list of current pairings and all time
pairings along with the date that they were paired. 
Once the warrior is finished being helped, the pair is removed from
current pairings, but remains in all as a history of all people helped.
(This code still needs to be done.)


##NOTES

Only friends who are trained may be added to the queue. The pairing happens
before the pair ever meets, so if someone gets cold feet then after a certain
amount of time they will be removed from the current pairings, but will remain
in all pairings with a description of what happened. 
It would be nice if all pairings 
would change inactive pairs to red and have active as greeen. 
(This is something to consider onces google sheets integration is complete.)
It is up to committe to manually place in reason pair ended, 
at the moment. We could create
another interface that lets committee members end pairs and add reason.

I really hope that I make this and then it breaks horrendously in the future.
That'd be no bueno.

