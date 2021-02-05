from bs4 import element
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
import base64

# https://stackoverflow.com/questions/52327098/how-to-wait-iframe-page-load-in-selenium

# tangenter osv
import time
import csv

cheat_cheet = dict()
SOV = 5
T_KORT = 0.7
T_V_KORT = 0.07
QUIZZ_LADD_TIMEOUT = 30


def kryptera(key, strang):
    krypt_chars = []
    for i in range(len(strang)):
        key_c = key[i % len(key)]
        krypt_c = chr(ord(strang[i]) + ord(key_c) % 256)
        krypt_chars.append(krypt_c)
    krypt_strang = "".join(krypt_chars)
    return krypt_strang


def dekrypt(key, strang):
    krypt_chars = []
    for i in range(len(strang)):
        key_c = key[i % len(key)]
        krypt_c = chr(ord(strang[i]) - ord(key_c) % 256)
        krypt_chars.append(krypt_c)
    krypt_strang = "".join(krypt_chars)
    return krypt_strang


KTH_ID = "rmarte"
KTH_PWRD = "lmao jag kommer inte skriva mitt lösen här"
PATH = "C:\Program Files\Selenium\chromedriver.exe"
COOKIE_ID = ""
CANVAS_LANK = "https://kth.instructure.com/courses/21375/assignments/147180/submissions/94958"
# CANVAS_LANK = "https://kth.instructure.com/courses/21375/assignments/147162/submissions/94959"


# with open("svar.csv", "w", newline="") as csvfile:
#     answer_csv = csv.writer(csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL)
#     for key, val in cheat_cheet:
#         answer_csv.writerow([key] + [val])


def hämta_personuppgifter():
    global KTH_ID
    global KTH_PWRD
    global PATH
    global CANVAS_LANK
    KTH_ID = input("vad är ditt kth-id? ") or "rmarte"
    KTH_PWRD = input("vad är ditt kth-lösenord? ") or "ne!"
    PATH = input("skriv in din path till chromedriver: ") or "C:\Program Files\Selenium\chromedriver.exe"
    CANVAS_LANK = input("skriv in länk till quizzet: ") or "https://kth.instructure.com/courses/21375/assignments/147180/submissions/94959"
    # print(KTH_ID, KTH_PWRD, PATH)


def logga_in(driver):
    print("loggar in...")
    namn_fält = driver.find_element_by_id("username")
    namn_fält.send_keys(KTH_ID)
    # print("namnfältet e", namn_fält)
    lösen_fält = driver.find_element_by_id("password")
    lösen_fält.send_keys(KTH_PWRD)
    lösen_fält.send_keys(Keys.RETURN)
    return


def gammal_dum_kod(driver, frågor):
    for fråga in frågor:
        print("-----------------------------###---------------------------")
        # print(fråga.text)
        # knappar = fråga.find_elements_by_css_selector('div[aria-label="yes"]')

        # knappar = fråga.find_elements_by_tag_name("input")
        # print(knappar[0].text)
        # knappar[0].parent.parent.click()
        # time.sleep(0.5)

        min_knapp = fråga.find_element_by_class_name("fNHEA_bOnW")
        print(min_knapp.text)
        min_knapp.click()
        time.sleep(T_V_KORT)

    time.sleep(T_KORT)
    wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-submit-button"]')))
    färdig_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-submit-button"]')
    färdig_knapp.click()
    time.sleep(T_KORT)
    wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-confirmation-modal-confirm"]')))

    rly_färd_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-confirmation-modal-confirm"]')
    rly_färd_knapp.click()

    wait.sleep(3)
    return


def starta_nu(driver):
    # === take now === #
    print("klickar på take now...")
    while len(driver.find_elements_by_class_name("fOyUs_bGBk")) < 4:
        continue
    elem = driver.find_elements_by_class_name("fOyUs_bGBk")
    elem[3].click()

    # wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fQfxa_bGBk")))
    # wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fQfxa_bGBk")))

    # === starta quizzer === #
    print("klickar på kör...")
    time.sleep(T_KORT)
    elem2 = driver.find_elements_by_class_name("fQfxa_bGBk")
    # elem = driver.find_element_by_id("alertHolder")
    # print("elem is", elem2)
    elem2[0].click()

    # frågor = driver.find_elements_by_class_name("bnWTo_bGBk")
    # print("hela listan", frågor[0])
    # for fråga in frågor:
    #     print("tjo", fråga)

    # driver.find_element_by_class_name
    # frågor = driver.find_elements_by_css_selector("div[role=main]")
    return


def fixa_svar(driver):
    global cheat_cheet
    time.sleep(T_KORT)
    while len(driver.find_elements_by_class_name("cQHeE_ebwZ")) < 2:
        continue
    fråge_matris = driver.find_elements_by_class_name("cQHeE_ebwZ")
    # print(fråge_matris)
    fråge_idx = 1
    for svar_låda in fråge_matris:
        print("-----------------------------#", fråge_idx, "#---------------------------")
        fråge_idx += 1

        svar_rader = svar_låda.find_elements_by_tag_name("p")
        text_rader = [x.text for x in svar_rader]
        svar_ikån = svar_låda.find_elements_by_css_selector('svg[name="IconCheck"]')

        frågeställning = text_rader[0]
        rätt_svar = ""

        # for i in text_rader:
        #     print(i)
        hej = "hej".splitlines(1)
        # === välj rätt svar === #
        if len(svar_ikån) > 0:  # vi valde redan rätt svar
            rätt_svar = svar_ikån[0].find_element_by_xpath("./../../..").text
            # print("rätt svar:", rätt_svar, "0")
            # print("EEE", rätt_svar)
            rätt_svar = rätt_svar.splitlines()
            rätt_svar = rätt_svar[1]

        else:  # vi valde fel
            # for rad in text_rader:
            #     print(rad)
            #     if rad == "":
            #         print("Ö")
            #     if rad == " ":
            #         print("Å")
            #     print("längd:", len(rad))

            text_rader = list(filter(lambda x: (len(x) > 1), text_rader))

            rätt_svar = max(text_rader, key=text_rader.count)

        # === printar === #
        print("fråga:", frågeställning)
        print("svar: ", rätt_svar)
        cheat_cheet[frågeställning] = rätt_svar

    w = csv.writer(open("output.csv", "w"))
    for key, val in cheat_cheet.items():
        w.writerow([key, val])
    return


def gör_frågor(driver, frågor):
    fråge_idx = 1
    print("hej")
    for fråga in frågor:
        print("-----------------------------#", fråge_idx, "#---------------------------")
        fråge_idx += 1
        # print(fråga.text)
        # knappar = fråga.find_elements_by_css_selector('div[aria-label="yes"]')

        # knappar = fråga.find_elements_by_tag_name("input")
        # print(knappar[0].text)
        # knappar[0].parent.parent.click()
        # time.sleep(0.5)

        # hitta alla <p>
        p_tags = fråga.find_elements_by_tag_name("p")
        # print("rätt svar på frågan:", cheat_cheet[p_tags[0].text])
        count = 0
        for i in p_tags:
            count += 1
            if cheat_cheet[p_tags[0].text] == i.text:
                time.sleep(T_V_KORT)
                print("-> ", end="")
                i.click()
            print(i.text, "/n")

        # min_knapp = fråga.find_element_by_class_name("fNHEA_bOnW")
        # print(min_knapp.text)
        # min_knapp.click()

        time.sleep(T_V_KORT)

    # time.sleep(999)
    färdig_frågor(driver)
    return


def slumpa_frågor(driver, frågor):
    fråge_idx = 1
    print("hej")
    for fråga in frågor:
        print("-----------------------------#", fråge_idx, "#---------------------------")
        fråge_idx += 1
        # print(fråga.text)
        # knappar = fråga.find_elements_by_css_selector('div[aria-label="yes"]')

        # knappar = fråga.find_elements_by_tag_name("input")
        # print(knappar[0].text)
        # knappar[0].parent.parent.click()
        # time.sleep(0.5)

        # hitta alla <p>
        p_tags = fråga.find_elements_by_tag_name("p")
        # print("rätt svar på frågan:", cheat_cheet[p_tags[0].text])
        p_tags[1].click()
        for i in p_tags:
            if i == p_tags[1]:
                print("?-> ", end="")
            print(i.text)

        # min_knapp = fråga.find_element_by_class_name("fNHEA_bOnW")
        # print(min_knapp.text)
        # min_knapp.click()
        time.sleep(T_V_KORT)

    färdig_frågor(driver)

    return


def färdig_frågor(driver):
    time.sleep(T_KORT)
    wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-submit-button"]')))
    färdig_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-submit-button"]')
    färdig_knapp.click()
    time.sleep(T_KORT)
    wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-confirmation-modal-confirm"]')))

    rly_färd_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-confirmation-modal-confirm"]')
    rly_färd_knapp.click()
    return


def klicka_runt(driver):

    # === take now === #
    starta_nu(driver)

    # === laddar frågor === #
    print("laddar frågor...")
    wait(driver, QUIZZ_LADD_TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role=form]")))
    frågor = driver.find_elements_by_css_selector("div[role=form]")

    time.sleep(T_KORT)
    return frågor


def main():
    hämta_personuppgifter()
    # def logga_in(namn, lösen, driver):
    #     namn_fält = driver.fin

    driver = webdriver.Chrome(PATH)

    sida_länk = CANVAS_LANK

    driver.get(sida_länk)
    print(driver.title)

    # === logga in === #
    logga_in(driver)

    # === iframe === #
    print("växlar till iframe...")
    wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("preview_frame"))
    # driver.switch_to.frame(driver.find_element_by_id("preview_frame"))

    # wait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fOyUs_bGBk")))

    # === slumpklicka fram svar === #
    frågor = klicka_runt(driver)
    slumpa_frågor(driver, frågor)

    # === hämta svaren från när vi hoppa runt innan === #
    print("hämtar svar...")
    fixa_svar(driver)

    # === gör frågor på riktigt === #
    frågor = klicka_runt(driver)
    print("gör frågor på riktigt...")
    gör_frågor(driver, frågor)

    time.sleep(50)

    # for fråga in frågor:
    #     print("-----------------------------###---------------------------")
    #     # print(fråga.text)
    #     # knappar = fråga.find_elements_by_css_selector('div[aria-label="yes"]')

    #     # knappar = fråga.find_elements_by_tag_name("input")
    #     # print(knappar[0].text)
    #     # knappar[0].parent.parent.click()
    #     # time.sleep(0.5)

    #     min_knapp = fråga.find_element_by_class_name("fNHEA_bOnW")
    #     print(min_knapp.text)
    #     min_knapp.click()
    #     time.sleep(0.05)

    # time.sleep(T_KORT)
    # wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-submit-button"]')))
    # färdig_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-submit-button"]')
    # färdig_knapp.click()
    # time.sleep(T_KORT)
    # wait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-automation="sdk-confirmation-modal-confirm"]')))

    # rly_färd_knapp = driver.find_element_by_css_selector('button[data-automation="sdk-confirmation-modal-confirm"]')
    # rly_färd_knapp.click()

    # wait.sleep(3)

    # radio_knapp = driver.find_element_by_class_name("fNHEA_ycrn")
    # radio_knapp.click()
    # print(frågor)

    # wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("iframe_name_or_id"))

    # try:
    #     main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "flash_message_holder")))
    #     print("main text är", main)

    # except:
    #     print("hitta inte :(")
    #     driver.quit()

    # knapplista = driver.find_elements_by_class_name("dEAKG_fziJ")
    # print(knapplista)
    # for knapp in knapplista:
    #     print(knapp)
    # start_btn_cls = "fOyUs_bGBk fOyUs_fKyb fOyUs_cuDs fOyUs_cBHs fOyUs_eWbJ fOyUs_fmDy fOyUs_eeJl fOyUs_cBtr fOyUs_fuTR fOyUs_cnfU fQfxa_bGBk"
    # class2 = "fOyUs_bGBk"

    # knappar = driver.find_element_by_class_name

    # startknapp = driver.find_element_by_class_name(class2)
    # startknapp = driver.find_element
    # print(startknapp)
    # startknapp.click()

    # search = driver.find_element_by_name("s")
    # search.send_keys("test")
    # search.send_keys(Keys.RETURN)

    # fQfxa_biBD

    # print(driver.page_source) # hela källkoden för sidan

    # time.sleep(5)

    # driver.close()


main()
