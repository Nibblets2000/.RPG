Welcome to .RPG, the programming language written like a Role Playing Game.

To ensure that you are able to write and run your code properly, please read the following for an optimal experience.

//RUNNING YOUR CODE
.RPG files can be launched in a terminal in the filepath of the ".RPG" folder. These lines look like this:

    python RPG.py name_of_file.RPG 

The above format will only function properly if your RPG.py, RPG.tx, and .RPG file are all in the same directory. Otherwise, the format to run the code
via the termial will look like this

    python FolderName/RPG.py FolderName/name_of_file.RPG --grammar FolderName/RPG.tx

"--grammar" is only needed if your RPG.tx file is in a different directory from your source folder; otherwise RPG.tx is used by default and does not need to be specified. As an example, run any of the example programs from the "ExamplePrograms" folder to give it a shot. Just as another example, if you wanted to run NewJourney.RPG, the terminal line would be

    python RPG.py ExamplePrograms/NewJourney.RPG 
