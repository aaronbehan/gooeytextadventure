A GUI based text adventure.

I made this program in order to learn the ins and outs of GUI's. I used Python's Tkinter module as Python was my strongest language. My secondary goal was to create an application which required no tutorial or manual and could teach a user how to play itself. I aimed to achieve this through a combination of pain-free trial and error and an uncomplicated, uncluttered, user-friendly interface.

The code spans 7 files but can be explained by its one universal behaviour. After the user inputs text, the string data is fed into the process_input function and analysed by various If statements to check if it is a recognised command. This leads the program to generate feedback which is ultimately displayed in the main GUI text box.

This will only work on Windows at the moment as Linux systems have some issues with the GUI.

If you experience difficulties running this on VSCode then I advise 'pip install pyautogui'.
