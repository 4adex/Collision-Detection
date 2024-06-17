# Project Presentation for Makers 2024 - Collision Simulation

### by Adesh Gupta

Dear Makers 2024 Committee,

I am delighted to introduce my project for Makers 2024, which focuses on implementing a sophisticated collision detection algorithm and creating an interactive screen to visualize its applications.

Simulation live at: https://aadex.itch.io/collision-simulation

## Problem Statement
The primary goal of this project was to develop a collision detection algorithm specifically tailored for detecting collisions between convex polygons in a 2D environment. To achieve this, I employed the Gilbert-Johnson-Keerthi Distance Algorithm (GJK), a powerful method for identifying collisions between two polygons. Additionally, I incorporated Bounding Volume Hierarchy for optimizations, ensuring efficient performance and frame rate maintenance.

## Presented Implementations  
Two distinct implementations were presented, each differing in their response when a collision is detected. Both implementations feature a player-controlled polygon that responds to UP, DOWN, LEFT, and RIGHT arrow keys in play mode. The modes include:

* **Play Mode**: Allows users to control the player polygon to interact with environmental polygons.
* **Draw Mode**: Enables users to draw polygons in the surrounding environment.

In the first implementation, the player polygon changes color upon colliding with any surrounding polygon. In the second implementation, the collision response is more advanced, restricting the motion of the player polygon upon colliding with surrounding blocks.

## Code Implementation 
The GJK part of code I coded out myself, the pseudo code from sources was very helpful but implementing it in my way was a process which required a lot of debugging and iterating. The optimization part I have used an open source work on AABB trees by kiphart but in order to display it and use it in accordance with my code required me to learn a lot of its working and I also have to modify it in order to display it visually.

## Project Process
**Research**: In-depth research was conducted to understand the intricacies of collision detection algorithms.  

**Initial Code**: The foundation of the project was laid with the writing of the initial code.  

**Debugging**: A thorough debugging process was undertaken to ensure the accuracy and reliability of the implemented algorithms.  

**Code Refinement**: The code underwent refinement to enhance clarity and maintainability.

**Deployment**: The project was deployed on itch.io using Pygbag, allowing for seamless access and interaction.

## Tech Stack Used
**Programming Language**: Python  
**Library/Framework**: Pygame  
**Optimization**: AABB trees by kiphart GitHub  
**Deployment**: Pygbag and itch.io

## Project Access
The second implementation is currently live on itch.io and can be accessed here. Please note that you are initially in draw mode, so click on play mode to enable controls.
Also it takes a while to load in the browser so please wait for it.

Thank you for considering my project. I am excited about the opportunity to discuss it further and showcase the various aspects of this collision simulation endeavor.

## Support Libraries
Please install pygame and numpy in the analyzing system before looking into code. Thanks!

## Further improvements and scopes 
The program can be extended to detecting collision with concave shapes by implementing triangulation if a polygon is concave in nature. The EPA algorithm can be implemented to improve response to collision.

## Refrences
K. A. Hart and J. J. Rimoli, Generation of statistically representative microstructures with direct grain geomety control, Computer Methods in Applied Mechanics and Engineering, 370 (2020), 113242.
https://github.com/kip-hart/AABBTree