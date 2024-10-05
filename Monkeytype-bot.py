from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pyautogui
import keyboard  # Import for keyboard event detection

# Set up the Selenium WebDriver
driver_path = r"chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Update with your ChromeDriver path
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

def login():
    driver.get('https://monkeytype.com/')
    time.sleep(5)  # Wait for the page to load

    try:
        # Accept cookies (if the button is visible)
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
        accept_button.click()
    except:
        print("Cookies accept button not found. Moving on...")

def writee(delay):
    try:
        # Locate the words and start typing
        while True:
            active_word = driver.find_element(By.CSS_SELECTOR, ".word.active")
            letters = [letter.text for letter in active_word.find_elements(By.TAG_NAME, "letter")]
            word = ''.join(letters)  # Create the word from letters
            pyautogui.write(word + ' ', interval=delay)
    except Exception as e:
        print(f"Typing error: {e}")

def playy(delay):
    time.sleep(3)
    pyautogui.alert("Please select the mode and the time you want and THEN press OK!")
    time.sleep(1)

    # Adjust the window position to ensure visibility
    driver.set_window_position(0, 0)
    time.sleep(4)

    # Start writing
    writee(delay)

def main():
    login()
    data = {"wpm": [], "accu": [], "consis": [], "delay": []}

    while True:
        # Scroll to bring typing area into focus
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Get delay from user
        delay = float(pyautogui.prompt(text='Enter the delay (seconds)\n0 is instantaneous', default='0.1'))
        playy(delay)

        # Fetch results
        try:
            wpm = driver.find_element(By.CSS_SELECTOR, ".group.wpm .bottom").text
            acc = driver.find_element(By.CSS_SELECTOR, ".group.acc .bottom").text
            consistency = driver.find_element(By.CSS_SELECTOR, ".group.consistency .bottom").text

            # Store the results
            data["wpm"].append(wpm)
            data["accu"].append(acc)
            data["consis"].append(consistency)
            data["delay"].append(delay)

            # Display the collected data
            for key in data:
                print(f"{key}: {data[key]}")
            print("--------------------------------------")
        except Exception as e:
            print(f"Error fetching results: {e}")

        # Ask if the user wants to try again
        ans = pyautogui.confirm(text='Wanna Type again?', title='Try Again?', buttons=['YES', 'NO'])
        if ans != 'YES':
            break

    driver.quit()

if __name__ == "__main__":
    main()
