# MobileRobots
Repo for mobile robots course


## Project Status

### Implemented Movements
- Move(distance) - backwards or forwards x cm
- Rotate(angle) - left or right in degrees
- turn(radius, angle) - perform a turn with the specified radius and for the arc-length correspoding to the angle
- follow(object) - follows object, if it is in front of the robot. Otherwise, asks ChatGPT for further instructions
- push() - pushes object in front of robot, must be really close

### ChatGPT Integration Status
- Asks for prompt when main() is ran, and tries to execute the response from gpt3.5, sometimes it responds with stuff other than lists

### Computer Vision Status
- Detected Objects, score and rectangle position are displayed
- App creates BT server which waits for connection to send the results

### To do
- Implement ask where I am behaviour. Should be simple
- Manual mode, instead of automaticly asking gpt3.5-turbo. Allow user to copy past ChatGPT4 responses

