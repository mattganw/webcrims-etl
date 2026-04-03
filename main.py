import pyautogui
import pyperclip

# https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc={lstDates[0]}&td={lstDates[-1]}

def submit_form():
    url = "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar?optionCountyCourt=NY051033J%3AU&dc=04/02/2026&td=04/09/2026"
    pyautogui.press('win')
    pyautogui.sleep(2)
    pyautogui.write('chrome')
    pyautogui.press('enter')
    pyautogui.sleep(2)
    pyautogui.write(url)
    pyautogui.press('enter')
    pyautogui.sleep(3)
    pyautogui.press("tab", presses=21)
    pyautogui.press("down", presses=2)

    # Select court parts ( 25 limit )
    pyautogui.keyDown("ctrl")
    for _ in range(24):
        pyautogui.press('down')
        pyautogui.press('space')
    pyautogui.keyUp("ctrl")
    
    pyautogui.press('tab', presses=2)
    pyautogui.press('enter')
    pyautogui.sleep(15) # Wait for results to load


def extract_html():
     # open DevTools
    pyautogui.press('f12')
    pyautogui.sleep(2)

    # focus console (Ctrl + `)
    pyautogui.hotkey('ctrl', '`')
    pyautogui.sleep(1)

    # type JS to get full HTML
    pyautogui.write("copy(document.querySelector('table').outerHTML)")
    pyautogui.press('enter')

    pyautogui.sleep(1)

    # close DevTools (optional)
    pyautogui.press('f12')
    pyautogui.sleep(1)

    html = pyperclip.paste()
    return html

if __name__ == "__main__":
    submit_form()
    data = extract_html()
    print(data)