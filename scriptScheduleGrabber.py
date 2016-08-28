

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flask import Flask, request, send_from_directory
app = Flask(__name__)


def getMagic( ID):   
  driver = webdriver.PhantomJS()
  driver.set_window_size(1120, 550)
  driver.get('https://mitec.itesm.mx/portal/page/portal/Alumnos/Publica?p_iPortal=1')
  driver.find_element_by_name('ssousername').send_keys("HIDDEN_ID")
  driver.find_element_by_name('password').send_keys("HIDDEN_PASSWORD")
  driver.find_element_by_name('password').send_keys(Keys.RETURN)
  WebDriverWait(driver, 10).until(
    EC.title_is("Portal Alumnos")
  )
  
  driver.get('https://alsvdbw01.itesm.mx/servesc/plsql/swglocalumnos_itesm.inicio')
  driver.find_element_by_name('matricula').send_keys(ID)
  driver.find_element_by_id('btnConsultar').click()
  
  driver.implicitly_wait(3) # seconds
 
  driver.find_element_by_link_text(ID).send_keys("\n")
  WebDriverWait(driver, 10).until(
    EC.title_is("Horario Alumno, Tec de Monterrey")
  )

  driver.save_screenshot('static/screenie-' + ID + '.png')
  
  
  # print driver.current_url
  source = driver.page_source
  driver.quit()
  return 'screenie-' + ID + '.png'

#@app.route("/")
@app.route('/get_schedule')
def hello():
    ID = request.args.get('id')
    path = getMagic(ID)
    print path
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'HackMTY', 'static'), path) 


if __name__ == "__main__":
    app.run()