from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from getpass import getpass

from time import sleep
from datetime import date
from datetime import datetime
import calendar

import lxml.etree
import lxml.html
#import pdb


#usr = input("Ingresar nombre de usuario: ")
#pwd = getpass("Ingresar contraseña: ")

timeout = 10

usr = 'blabla'
pwd = 'blabla'

CUIT1 = "23452345234521": # CUIT 1 destino
CUIT2 = "45756785958978": # CUIT 2 destino

producto_servicio_CUIT1 = "bla bla bla mantenimiento de...": # -> hacia fulano
producto_servicio_CUIT2 = "bla bla bla por servicios de...": # -> hacia mengano
facturado_mes_anterior = "xxxxx" #ARBA DDJJ
	
sele = input("1: AFIP - Factura C\n2: DDJJ ARBA\n\n Selección:  ")
#pdb.set_trace()

if sele == "1":
	CUIT1 = "30546666707" 
	CUIT2 = "30677980032"


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
	para = input("Factura para: \n1: Raúl\n2: Fede\nSelección: ")

	#monto = input("Precio unitario: ")

	if para == "1":
		cuit_receptor = CUIT1 # comentar si estoy pidiendo ingresar el CUIT
		descripcion = producto_servicio_CUIT1
		monto = "xxxxxxxx"
	elif para == "2":
		descripcion = producto_servicio_CUIT2
		cuit_receptor = CUIT2 # comentar si estoy pidiendo ingresar el CUIT
		monto = "xxxxxxxx"

	driver = webdriver.Chrome()
	driver.get('https://auth.afip.gob.ar/contribuyente_/login.xhtml')
	driver.maximize_window()

	try:
		element_present = EC.presence_of_element_located((By.ID, "F1:username"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out username")

	usr_box = driver.find_element_by_id('F1:username')
	usr_box.send_keys(usr)

	try:
		element_present = EC.presence_of_element_located((By.ID, "F1:btnSiguiente"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out user->pass")

	siguiente = driver.find_element_by_id('F1:btnSiguiente')
	siguiente.click()

	try:
		element_present = EC.presence_of_element_located((By.ID, "F1:password"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out pass")

	pwd_box = driver.find_element_by_id('F1:password')
	pwd_box.send_keys(pwd)

	login_button = driver.find_element_by_id('F1:btnIngresar')
	login_button.click()

	try:
		element_present = EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Comprobantes en línea')]"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out Comprobantes en línea")

	acomprobantes = driver.find_element_by_xpath("//p[contains(., 'Comprobantes en línea')]")
	acomprobantes.click()

	try:
		element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'apellido nombre empresa...']"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out empresa")

	driver.switch_to_window(driver.window_handles[1])
	empresa = driver.find_element_by_xpath("//input[@value = 'Apellido nombre..']")
	empresa.click()

	try:
		element_present = EC.presence_of_element_located((By.ID, "btn_gen_cmp"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out empresa")

	generar_comprobante = driver.find_element_by_id("btn_gen_cmp")
	generar_comprobante.send_keys(Keys.ENTER)

	try:
		element_present = EC.presence_of_element_located((By.NAME, "puntoDeVenta"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out pto de venta")

	elemento_pto_venta = driver.find_element_by_name("puntoDeVenta")
	select_pto_venta = Select(elemento_pto_venta)
	select_pto_venta.select_by_value(pto_venta)

	try:
		element_present = EC.presence_of_element_located((By.NAME, "universoComprobante"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out universoComprobante")

	tipo = driver.find_element_by_name("universoComprobante")
	select_tipo = Select(tipo)
	select_tipo.select_by_value(tipo_comprobante)

	continuar1 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
	continuar1.click()

	try:
		element_present = EC.presence_of_element_located((By.ID, "idconcepto"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out idconcepto")

	conceptos_incluir = driver.find_element_by_id("idconcepto")
	select_conceptos_incluir = Select(conceptos_incluir)
	select_conceptos_incluir.select_by_value(conceptos)

	try:
		element_present = EC.presence_of_element_located((By.NAME, "periodoFacturadoDesde"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out periodoFacturadoDesde")

	desde_box = driver.find_element_by_name('periodoFacturadoDesde')
	desde_box.clear()
	desde_box.send_keys(desde)

	hasta_box = driver.find_element_by_name('periodoFacturadoHasta')
	hasta_box.clear()
	hasta_box.send_keys(hasta)

	venc_box = driver.find_element_by_name('vencimientoPago')
	venc_box.clear()
	venc_box.send_keys(venc)

	try:
		element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'Continuar >']"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out Continuar2")

	continuar2 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
	continuar2.click()

	try:
		element_present = EC.presence_of_element_located((By.ID, "idivareceptor"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out idivareceptor")


	idivareceptor = driver.find_element_by_id("idivareceptor")
	select_idivareceptor = Select(idivareceptor)
	select_idivareceptor.select_by_value(condicion)

	try:
		element_present = EC.presence_of_element_located((By.ID, "nrodocreceptor"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out nrodocreceptor")


	nrodocreceptor_box = driver.find_element_by_id('nrodocreceptor')

	nrodocreceptor_box.send_keys(cuit_receptor)

	sleep(1)
	nrodocreceptor_box.send_keys(Keys.TAB)

	try:
		element_present = EC.presence_of_element_located((By.ID, "razonsocialreceptor"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out razonsocialreceptor")


	razonsocialreceptor = driver.find_element_by_id("razonsocialreceptor")
	razonsocialreceptor.click()
	#sleep(2)
	#razonsocialreceptor.send_keys(Keys.TAB)
	try:
		element_present = EC.presence_of_element_located((By.ID, "domicilioreceptorcombo"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out domicilioreceptorcombo")

	domicilioreceptorcombo = driver.find_element_by_id("domicilioreceptorcombo")
	select_domicilioreceptorcombo = Select(domicilioreceptorcombo)
	select_domicilioreceptorcombo.select_by_index(0)

	try:
		element_present = EC.presence_of_element_located((By.ID, "formadepago1"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out formadepago1")


	formadepago1 = driver.find_element_by_id("formadepago1")
	formadepago1.click()

	try:
		element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'Continuar >']"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out continuar3")


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

	try:
		element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'Continuar >']"))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out continuar4")


	continuar4 = driver.find_element_by_xpath("//input[@value = 'Continuar >']")
	continuar4.click()

	#pdb.set_trace()

	if confirmar == 's':

		try:
			element_present = EC.presence_of_element_located((By.ID, "btngenerar"))
			WebDriverWait(driver, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out btngenerar")

		confirmar_btn = driver.find_element_by_id('btngenerar')
		confirmar_btn.click()

		sleep(1)
		
		#Aceptar el alert de confirmación
		if EC.alert_is_present: 
			alert = driver.switch_to_alert()
			alert.accept()
		else:
			print ("No alert exists")

		try:
			element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'Imprimir..."))
			WebDriverWait(driver, timeout).until(element_present)
		except TimeoutException:
			print ("Timed out imprimir")

		imprimir = driver.find_element_by_xpath("//input[@value = 'Imprimir...")
		imprimir.click()

		#~/Descargas/...........pdf
elif sele == "2":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://www.arba.gov.ar/DatosContacto/DatosContactoRedirect.asp?destino=http://www.arba.gov.ar/Gestionar/Gestionar_Default.asp')

    try:
        element_present = EC.presence_of_element_located((By.ID, "password"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out login")

    prefijo = driver.find_element_by_id('prefijo')
    prefijo.send_keys(usr1)

    dni = driver.find_element_by_id('dni')
    dni.send_keys(usr2)

    sufijo = driver.find_element_by_id('sufijo')
    sufijo.send_keys(usr3)

    password = driver.find_element_by_id('password')
    password.send_keys(pwd)

    ingresar = driver.find_element_by_xpath("//input[@value = 'Ingresar']")
    ingresar.submit()

    try:
        element_present = EC.presence_of_element_located((By.ID, "cmenu"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out main")

    driver.find_element_by_xpath("//a[@href='Gestionar_PresentacionDDJJ.asp']").click();

    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "//iframe[@class='frameAnchoTotal']"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out ddjj")

    sleep(3)
    driver.switch_to.frame(driver.find_element_by_class_name('frameAnchoTotal'))

    driver.find_element_by_xpath("//a[contains(@href,'DDJJ_WEB.asp')]").click();

    #driver.switch_to_window(driver.window_handles[1])
    sleep(3)
    driver.switch_to.window(driver.window_handles[1])


    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//a[contains(text(), ' DDJJ Web ')]"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out ddjj2")

    driver.find_element(By.XPATH, "//a[contains(text(), ' DDJJ Web ')]").click()

    driver.get('http://www4.arba.gov.ar/IBPresentaciones/preInicioDDJJ.do')

    try:
        element_present = EC.presence_of_element_located((By.ID, "mes"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out mes")

    mes = driver.find_element_by_id("mes")
    select_mes = Select(mes)
    select_mes.select_by_value(str(datetime.now().month-1))

    driver.find_element_by_name("siguiente").click()

    sleep(2)
    driver.find_element_by_id("btnActividades").click()

    #Aceptar el alert de confirmación
    if EC.alert_is_present: 
        alert = driver.switch_to.alert
        alert.accept()
    else:
        print ("No alert exists")

    driver.find_element_by_class_name('iconoEditar').click()

    sleep(2)


    try:
        element_present = EC.presence_of_element_located((By.ID, "imImponible"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out imImponible")


    imImponible = driver.find_element_by_id('imImponible')
    imImponible.clear()
    imImponible.send_keys(facturado_mes_anterior)


    montoMinimo = driver.find_element_by_id('montoMinimo')
    montoMinimo.clear()
    montoMinimo.send_keys("0")

    driver.find_element_by_id("siguiente").click()


    #Aceptar el alert de confirmación
    if EC.alert_is_present: 
        alert = driver.switch_to.alert
        alert.accept()
    else:
        print ("No alert exists")

    driver.find_element_by_id("button1").click()


    driver.find_element_by_id('btnDeducciones').click()
    driver.find_element_by_id('deduccionesCancelarBtn').click()


    driver.find_element_by_id("benviar").click()
    driver.find_element_by_id("enviar").click()



    #sufijo = driver.find_element_by_id('sufijo')
    #sufijo.send_keys(usr3)

    #driver.get('http://www4.arba.gov.ar:80/IBPresentaciones/listActividadesVerifIncons.do')


    #actions.click(btn)
    #actions.perform()

    #driver.window_handles
    #driver.page_source
    #webdriver.find_element(By.XPATH, "//a[@href='" + the_full_href + "']")
    #((By.XPATH, "//p[contains(., 'Comprobantes en línea')]"))
    #driver.find_element_by_link_text('<abbr title="Declaraciones juradas">DDJJ</abbr> Web').click()


