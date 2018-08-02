from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from getpass import getpass

from time import sleep
from datetime import date
from datetime import datetime
import calendar

import lxml.etree
import lxml.html
import pdb


#usr = input("Ingresar nombre de usuario: ")
#pwd = getpass("Ingresar contraseña: ")

usr = 'blabla'
pwd = 'blabla'

CUIT1 = "23452345234521": # CUIT 1 destino
CUIT2 = "45756785958978": # CUIT 2 destino

producto_servicio_CUIT1 = "bla bla bla mantenimiento de...": # -> hacia fulano
producto_servicio_CUIT2 = "bla bla bla por servicios de...": # -> hacia mengano
unidades_medida = " unidades"

confirmar = input("¿Confirmar generación de comprobante? [s/n]: ")
	
#pto_venta = input("Punto de venta:\n1: ############# \nSeleeccion: ")
#tipo_comprobante = input("Tipo comprobante:\n2: Factura C\nSeleccion: ")
#conceptos = input("Conceptos a incluir:\n1 Productos\n2 Servicios\n3 Productos y Servicios\nSeleccion: ")

pto_venta = "1"
tipo_comprobante = "2"
conceptos = "2"

# Descomentar si quiero preguntar por fechas al inicio:

#desde = input("Facurado Desde: ")
#hasta = input("Facturado Hasta: ")
#venc = input("Vencimiento Factura: ")

#desde = date.today().strftime("%d/%m/%y")
#hasta = date.today().strftime("%d/%m/%y")
#venc  = date.today().strftime("%d/%m/%y")

# ajustado para mi: 
# desde/hasta -> 01 mes anterior a 30 o 31 mes anterior
# ven: 20 del mes actual

# 1er dia mes anterior
desde = date(datetime.now().year, datetime.now().month-1, 1).strftime("%d/%m/%Y")

#ultimo dia mes anterior
hasta = date(datetime.now().year, datetime.now().month-1, calendar.monthrange(datetime.now().year, datetime.now().month-1)[1]).strftime("%d/%m/%Y")
venc  = date(datetime.now().year, datetime.now().month, 20).strftime("%d/%m/%Y")


#condicion = input("Condición frente al IVA:\n4: Sujeto Exento\nSelección: ")
condicion = "4"
#cuit_receptor = input("Receptor: \n1: CUIT receptor 1\n2: CUIT receptor 2\nSelección: ")
para = input("Factura para: \n1: Fulano\n2: Mengano\nSelección: ")

if para == "1":
	cuit_receptor = CUIT1 # comentar si estoy pidiendo ingresar el CUIT
	descripcion = producto_servicio_CUIT1
	monto = "..........."
elif para == "2":
	descripcion = producto_servicio_CUIT2	
	cuit_receptor = CUIT2 # comentar si estoy pidiendo ingresar el CUIT
	monto = "..........."

#monto = input("Precio unitario: ")
driver = webdriver.Chrome()
driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')

usr_box = driver.find_element_by_id('F1:username')
usr_box.send_keys(usr)

sleep(2)

siguiente = driver.find_element_by_id('F1:btnSiguiente')
siguiente.click()

sleep(2)

pwd_box = driver.find_element_by_id('F1:password')
pwd_box.send_keys(pwd)

login_button = driver.find_element_by_id('F1:btnIngresar')
login_button.click()
sleep(2)
acomprobantes = driver.find_element_by_xpath("//p[contains(., 'Comprobantes en línea')]")
acomprobantes.click()
sleep(2)
driver.switch_to_window(driver.window_handles[1])
empresa = driver.find_element_by_xpath("//input[@value = 'APELLIDO NOMBRES']")
empresa.click()

sleep(2)

generar_comprobante = driver.find_element_by_id("btn_gen_cmp")
generar_comprobante.send_keys(Keys.ENTER)
sleep(2)
elemento_pto_venta = driver.find_element_by_name("puntoDeVenta")
select_pto_venta = Select(elemento_pto_venta)
select_pto_venta.select_by_value(pto_venta)

sleep(1)

tipo = driver.find_element_by_name("universoComprobante")
select_tipo = Select(tipo)
select_tipo.select_by_value(tipo_comprobante)

continuar1 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
continuar1.click()

sleep(2)

conceptos_incluir = driver.find_element_by_id("idconcepto")
select_conceptos_incluir = Select(conceptos_incluir)
select_conceptos_incluir.select_by_value(conceptos)

sleep(1)

desde_box = driver.find_element_by_name('periodoFacturadoDesde')
desde_box.clear()
desde_box.send_keys(desde)

hasta_box = driver.find_element_by_name('periodoFacturadoHasta')
hasta_box.clear()
hasta_box.send_keys(hasta)

venc_box = driver.find_element_by_name('vencimientoPago')
venc_box.clear()
venc_box.send_keys(venc)

sleep(1)

continuar2 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
continuar2.click()

sleep(2)


idivareceptor = driver.find_element_by_id("idivareceptor")
select_idivareceptor = Select(idivareceptor)
select_idivareceptor.select_by_value(condicion)

sleep(1)

nrodocreceptor_box = driver.find_element_by_id('nrodocreceptor')

nrodocreceptor_box.send_keys(cuit_receptor)

sleep(1)
nrodocreceptor_box.send_keys(Keys.TAB)
sleep(1)

razonsocialreceptor = driver.find_element_by_id("razonsocialreceptor")
razonsocialreceptor.click()
#sleep(2)
#razonsocialreceptor.send_keys(Keys.TAB)


domicilioreceptorcombo = driver.find_element_by_id("domicilioreceptorcombo")
select_domicilioreceptorcombo = Select(domicilioreceptorcombo)
select_domicilioreceptorcombo.select_by_index(0)

sleep(2)

formadepago1 = driver.find_element_by_id("formadepago1")
formadepago1.click()

continuar3 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
continuar3.click()

descripcion_box = driver.find_element_by_id('detalle_descripcion1')

descripcion_box.send_keys(descripcion)
descripcion_box.send_keys()

detalle_medida1 = driver.find_element_by_id("detalle_medida1")
select_detalle_medida1 = Select(detalle_medida1)
select_detalle_medida1.select_by_visible_text(unidades_medida)
#select_detalle_medida1.select_by_value("7")

detalle_precio1_box = driver.find_element_by_id('detalle_precio1')
detalle_precio1_box.send_keys(monto)

sleep(1)

continuar4 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
continuar4.click()

sleep(1)
pdb.set_trace()
if confirmar == 's':
	confirmar_btn = driver.find_element_by_id('btngenerar')
	confirmar_btn.click()
	sleep(1)
	imprimir = driver.find_element_by_xpath("//input[@value = 'Imprimir...")
	imprimir.click()
	#~/Descargas/...........pdf