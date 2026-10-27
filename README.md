# Blue Light Filter

A Windows desktop app for warming and dimming your display. The interface uses a hydrangea-inspired pink and purple palette.

## Features

- Adjust colour temperature from 1900 K to 6500 K.
- Dim the display from 0% to 50%.
- Use the Reading, Evening, and Night presets.
- Toggle the filter on or off; changes apply as you adjust the controls.
- Restore the default display gamma ramp when the app closes.

## Requirements

- Windows
- Python 3.10 or later
- Tkinter (included with most standard Python for Windows installations)

No third-party packages are required. The app uses the Windows display gamma-ramp API through Python's built-in `ctypes`.

## Run

Open PowerShell or Command Prompt in the project folder and run:

```powershell
python app.py
```

## Notes

The filter changes the display gamma ramp. Support can vary by graphics hardware, drivers, and display configuration. If Windows rejects the setting, the app shows a status message. Closing the app restores the default gamma ramp.
