# controller-manager
a Maya controller manager

### Usage
1. Place the `conLibrary/` under the Maya `script/` folder
2. Run below code to generate the UI
  ```python
  from conLibrary import libraryUI
  reload(libraryUI)

  ui = libraryUI.showUI()
  ```

![controller-manager-save](https://user-images.githubusercontent.com/23650308/172152977-ef9a6a5f-8b41-473c-871e-4180a6acf4ab.gif)
![controller-manager-load](https://user-images.githubusercontent.com/23650308/172152992-e6d0de4c-8a0d-4bc8-b881-ff9b0e00d7ef.gif)
