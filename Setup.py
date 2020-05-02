import cx_Freeze

executables = [cx_Freeze.Executable("FuelRun.py")]

cx_Freeze.setup(
    name = "FuelRun",
    options = {"build_exe": {"packages": ["pygame"], "include_files":["Resources/Images/Cloud.png", "Resources/BULKYPIX.ttf", "Resources/Images/BluePlane.png", "Resources/Images/GreenPlane.png", "Resources/Images/MonoPlane.png", "Resources/Images/PinkPlane.png", "Resources/Images/RedPlane.png", "Resources/Images/RetroPlane.png", "Resources/Images/TechPlane.png", "Resources/Images/PurplePlane.png", "Resources/Sound/WrongAnswer.wav", "Resources/Sound/RightAnswer.wav", "Resources/Sound/ButtonPress.wav", "Resources/Sound/GameOver.wav", "Resources/Sound/Overworld.mp3", "Resources/Sound/Bit Quest.mp3"]}},
    executables = executables
    )
