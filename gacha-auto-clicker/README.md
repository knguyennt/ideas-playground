# Gacha Daily Automation

Tired of the daily grind in gacha games? This automation will do the work for you. Inspired by the game **Epic 7**, this tool is designed to handle your daily tasks, saving you time and effort.

## Initial Idea

- Utilize a library to capture pixels or images that require clicks or conditions to trigger a button press.
- Map out button click conditions to handle different tasks.
- Implement a cycle through various tasks, since daily activities in gacha games can be numerous.

## Thoughts after prototype
- pyautogui works as expected, it can detect image on scrren and trigger click event. Making it perfect for auto clicker gacha games
- The image size is still a problem, when you take picture in full screen and scale it can't detect correctly
- This is a linear development not much room for extend, thinking of using pyqt for UI.
