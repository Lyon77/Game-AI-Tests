The mycreatepathnetwork creates a nav mesh in the corresponding enviroment.

The algorithm creates triangles due to its convexity (if thats a word)

Then the code runs through the shapes to try to combine them to create larger polygons.

With the polygons, points are generated from the center and the midpoints of the edge of adjacent polygons

Lines are connected between them for the AI to move around

In this demonstration, the AI has random movement, but my A* folder add onto this code

Located in <strong>mycreatepathnetwork</strong>
