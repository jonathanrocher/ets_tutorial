# First real version of the pycasa ETS pyface application!
Building on the hello world application, this stage creates a real application 
that allows to navigate the local drive, and open an image file in the central 
pane. The following steps are taken here: 
- create a realistic task with a split editor area pane for the central pane 
  and a file browser dock pane that exposes the home folder using the custom 
  version of TraitsUI's `FileEditor`. 
- Adds a ImageFile model, view and an editor so that an image can be open in 
  the central pane.
- Add a listener on the file browser double-click event to trigger opening the 
  image file. 
