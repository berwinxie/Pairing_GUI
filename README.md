#PAIRING GUI and SHEET ORGANIZER

This repository is the initial workings of an interface to simplify the
pairing process for open ears. People who are seeking help are nicknamed
'warriors' to simplify the coding and mre is a lembers of our organization who 
are giving the help are 'friends.'


#THE PROCESS

The main idea is the list of people who are friends. These friends can then add
themselves to a queue marking themselves as available to help. At any point
they can also remove themselves from this queue, making themselves unavailable.

Now there is also a list of people who want to be helped, warriors. All warriors
are automatically added to the queue, setting them up to be helped by a friend.
Someone in the commmittee will see both the queues and pair someone in the 
warrior queue with someone in the friends queue. This removes both people from
the queues and adds them as a pair to the list of current pairings and all time
pairings. Once the warrior is finished being helped, the pair is removed from
current pairings, but remains in all as a history of all people helped.


#NOTES

Only friends who are trained may be added to the queue. The pairing happens
before the pair ever meets, so if someone gets cold feet then after a certain
amount of time they will be removed from the current pairings, but will remain
in all with a description of what happened. It would be nice if all pairings 
would change inactive pairs to red and have active as greeen. It is up to
committe to manually place in reason pair ended, at the moment. We could create
another interface that lets committee members end pairs and add reason.
