from credenciales import *
from config import *
from funciones import *
import sys
import os
import shutil
import subprocess as sp
sys.path.insert(0, 'libs')
# Migrado de chrome driver a : 
# https://pypi.org/project/webdriver-manager/
from webdriver_manager.chrome import ChromeDriverManager
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#import chromedriver_binary
from getpass import getpass

from time import sleep
from datetime import date
from datetime import datetime
import calendar
import dateutil.relativedelta

import lxml.etree
import lxml.html

# pip install selenium chromedriver-binary
# pacman -S python-dateutil python-lxml
import pdb
# import readline
# import rlcompleter # para autocomp. en modo interact

#usr = input("Ingresar nombre de usuario: ")
#pwd = getpass("Ingresar contraseña: ")

try:
	while True:
		os.system('clear')
		sele = input("\n1: AFIP - Factura C\n"+
					 "2: ARBA - DDJJ\n"+
					 "3: Ver facturas en DB\n"+
					 "4: Eliminar factura\n"+
					 "5: Guardar factura manualmente en DB\n"+
					 "6: Ingresos por mes\n"+
					 "7: Montos para DDJJ ARBA\n"+
					 "0: Salir (o ctrl+c)\n"+
					 "\n Selección:  ")
		#pdb.set_trace()

		if sele == "0":
			break
		if sele == "1":

			confirmar = input("¿Confirmar generación de comprobante? [s/n]: ")
			fecha_manual = input("¿Fechas manuales? [s/n]: ")
			if fecha_manual == 's':
				fd = input("Fecha desde: ")
				desde_dt = datetime.strptime(fd, '%d/%m/%Y')
			else:
				#desde = date.today().strftime("%d/%m/%y")
				#hasta = date.today().strftime("%d/%m/%y")
				#venc  = date.today().strftime("%d/%m/%y")

				# ajustado para mi:
				# desde/hasta -> 01 mes anterior a 30 o 31 mes anterior
				# ven: 20 del mes actual

				# 1er dia mes anterior

				# desde = date(datetime.now().year, datetime.now().month-1, 1).strftime("%d/%m/%Y")
				desde_dt = datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
				#ultimo dia mes anterior
				#hasta = date(datetime.now().year, datetime.now().month-1, calendar.monthrange(datetime.now().year, datetime.now().month-1)[1]).strftime("%d/%m/%Y")


			mes_hasta = desde_dt.month
			#(calendar.monthrange(datetime.now().year, mes_hasta)[1]).strftime("%d/%m/%Y")

			desde = date(desde_dt.year,desde_dt.month,1).strftime("%d/%m/%Y")
			desde_sqlite = date(desde_dt.year,desde_dt.month,1).strftime("%Y-%m-%d")

			hasta = date(desde_dt.year, desde_dt.month, calendar.monthrange(datetime.now().year, mes_hasta)[1]).strftime("%d/%m/%Y")
			hasta_sqlite = date(desde_dt.year, desde_dt.month, calendar.monthrange(datetime.now().year, mes_hasta)[1]).strftime("%Y-%m-%d")
			#hasta = date(datetime.now().year, datetime.now().month-1, calendar.monthrange(datetime.now().year, datetime.now().month-1)[1]).strftime("%d/%m/%Y")
			print(desde)
			print(hasta)
			# SI QUIERO TODOS LOS 28
			#venc  = date(datetime.now().year, datetime.now().month, 28).strftime("%d/%m/%Y")

			# 10 días desde ahora:
			venc = (datetime.now() + dateutil.relativedelta.relativedelta(days=10)).strftime("%d/%m/%Y")                        
			#venc = "05/02/2019"

			para = input( selecc + "\n Selección: " )


			# Descomentar si quiero preguntar por fechas al inicio:
			
			#pto_venta = input("Punto de venta:\n1: ############# \nSeleeccion: ")
			#tipo_comprobante = input("Tipo comprobante:\n2: Factura C\nSeleccion: ")
			#conceptos = input("Conceptos a incluir:\n1 Productos\n2 Servicios\n3 Productos y Servicios\nSeleccion: ")

			#desde = input("Facurado Desde: ")
			#hasta = input("Facturado Hasta: ")
			#venc = input("Vencimiento Factura: ")

			#cuit_receptor = input("CUIT receptor: ")
			#monto = input("Precio unitario: ")

			driver = webdriver.Chrome(ChromeDriverManager().install())
			# driver = webdriver.Chrome()
			driver.get(pagina_login)
			# driver.switch_to.window(driver.current_window_handle)
			pyName = driver.title
			pyHandle = driver.current_window_handle # es = driver.window_handles[0]	

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

			"""
			try:
				ir_version_orig = EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Ver versión original')]"))
				WebDriverWait(driver, timeout).until(ir_version_orig)
				# Tiene el portal resumido
				driver.get("https://portalcf.cloud.afip.gob.ar/portal/app/")
			except TimeoutException:
				pass
			"""
			"""
			pdb.set_trace()
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Monotributo')]"))
				WebDriverWait(driver, timeout).until(element_present)
				# Tiene el portal resumido
				ir_monotributo = driver.find_element(By.XPATH, "//h3[contains(., 'Monotributo')]")
				ir_monotributo.click()				
			except TimeoutException:
				pass			
			"""
			"""
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Ir al portal')]"))
				WebDriverWait(driver, timeout).until(element_present)
			except TimeoutException:
				print ("Timed out Ir al Portal")
			driver.find_element_by_xpath("//button[contains(., 'Ir al portal')]").click()
			"""
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//h3[contains(., 'Comprobantes en línea')]"))
				WebDriverWait(driver, timeout).until(element_present)
			except TimeoutException:
				print ("Timed out comprobantes en linea")

			comprobantes_linea = driver.find_element(By.XPATH, "//h3[contains(., 'Comprobantes en línea')]")
			comprobantes_linea.click()

			for handle in driver.window_handles:
				print(handle)
			for i in range(0, len(driver.window_handles)):
				print("ID win hand: "+str(i))


			sleep(2)
			for handle in driver.window_handles:
				print(handle)
				
			for i in range(0, len(driver.window_handles)):
				print("ID win hand: "+str(i))
			#pdb.set_trace()
				
			### CAMBIAR DE VENTANA ###

			#pyHandle = driver.window_handles[1] si 1 overflow del indice
			#driver.switch_to.window(pyHandle)

			#driver.get("https://monotributo.afip.gob.ar/app/Inicio.aspx")

			pyHandle = driver.window_handles[1]
			driver.switch_to.window(pyHandle)
			
			# dot . stands for text()
			"""
			try:
				element_present = EC.presence_of_element_located((By.ID, "myModalAdmRel"))
				# EC.presence_of_element_located((By.ID, "bBtn1"))
				# FALLA POR ERROR EN PÁGINA AFIP QUE TIENE DOS button con mismo ID !
				WebDriverWait(driver, timeout).until(element_present)
			except:
				pass
			finally:
				driver.find_elements_by_xpath("//div[@id='myModalAdmRel']/button[contains(.,'Aceptar')]")
			driver.find_element_by_xpath("//button[contains(.,'Aceptar')]").click()
			
			sleep(2)
			
   
   			# Ahora no lo estoy usando porque ya se está parando sobre el listado de empresas:
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//button[contains(.,'Emitir Factura')]"))
				# EC.presence_of_element_located((By.ID, "bBtn1"))
				# FALLA POR ERROR EN PÁGINA AFIP QUE TIENE DOS button con mismo ID !
				WebDriverWait(driver, timeout).until(element_present)
			except TimeoutException:
				print ("Timed out EMITIR FACTURA")
				driver.close()
				driver.quit()
			
			#driver.find_element_by_id('bBtn1').click()
			driver.find_element_by_xpath("//button[contains(.,'Emitir Factura')]").click()
			"""
			
			"""			  CON LA ACTUALIZACION DEL SITIO YA NO EXISTE ESTO
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//p[contains(., 'Comprobantes en línea')]"))
				WebDriverWait(driver, timeout).until(element_present)
			except TimeoutException:
				print ("Timed out Comprobantes en línea")

			acomprobantes = driver.find_element_by_xpath("//p[contains(., 'Comprobantes en línea')]")
			acomprobantes.click()
			"""
			

			#for handle in driver.window_handles:
			#	print(handle)



			
			#pyHandle = driver.window_handles[2] # era 2 antes 
			#driver.switch_to.window(pyHandle)
			try:
				element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'CABO ENRIQUE ALEJANDRO']"))
				WebDriverWait(driver, timeout).until(element_present)
			except TimeoutException:
				print ("Timed out empresa")
			 

			empresa = driver.find_element_by_xpath("//input[@value = 'CABO ENRIQUE ALEJANDRO']")
			empresa.click() # -> Viendo "Generar comprobante..."


			#### GENERO UNA O TODAS LAS FACTURAS ####
			if para != '0':
				destinos_nombres = para 
				# si seleccioné generar una sola factura
				# , si no itero por todo el diccionario
			"""
			for handle in driver.window_handles:
				print(handle)
			"""
			for para in destinos_nombres:

				# open new blank tab
				driver.execute_script("window.open();")

				# switch to the new window which is second in window_handles array
				index_winhand = max(i for i in range(0, len(driver.window_handles)))
				driver.switch_to.window(driver.window_handles[index_winhand])
				driver.get(pagina_generar_comprobantes)

				monto         = montos.get(para)
				descripcion   = detalles.get(para)
				cuit_receptor = cuits.get(para)
				condicion     = condiciones.get(para)
				destinatario  = cuits_nm.get(cuit_receptor)

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
				sleep(0.5)

				try:
					element_present = EC.presence_of_element_located((By.NAME, "universoComprobante"))
					WebDriverWait(driver, timeout).until(element_present)
				except TimeoutException:
					print ("Timed out universoComprobante")

				tipo = driver.find_element_by_name("universoComprobante")
				select_tipo = Select(tipo)
				#pdb.set_trace()
				sleep(0.5)
				select_tipo.select_by_visible_text(tipo_comprobante_txt)
				#select_tipo.select_by_value(tipo_comprobante)

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
				#venc_box.send_keys(Keys.TAB)
				#sleep(3)
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
				sleep(1)
				#razonsocialreceptor.send_keys(Keys.TAB)
				"""
				try:
					element_present = EC.presence_of_element_located((By.ID, "domicilioreceptorcombo"))
					WebDriverWait(driver, timeout).until(element_present)
				except TimeoutException:
					print ("Timed out domicilioreceptorcombo")

				domicilioreceptorcombo = driver.find_element_by_id("domicilioreceptorcombo")
				select_domicilioreceptorcombo = Select(domicilioreceptorcombo)
				select_domicilioreceptorcombo.select_by_index(0)
				"""
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
						alert = driver.switch_to.alert()
						alert.accept()
					else:
						print ("No alert exists")

					try:
						element_present = EC.presence_of_element_located((By.XPATH, "//input[@value = 'Imprimir..."))
						WebDriverWait(driver, timeout).until(element_present)
					except TimeoutException:
						print ("Timed out imprimir")

					imprimir = driver.find_element_by_xpath("//input[@value = 'Imprimir...']")
					imprimir.click()
					#~/Descargas/...........pdf
				# FIN GENERAR FACTURAS

				conn = create_connection(database)

				if GuardarEnDB:
						factura_campos = ('',
										cuit_receptor,
										destinatario,
										monto,
										descripcion,
										desde_sqlite,
										hasta_sqlite)			
						guardar_factura(conn,factura_campos)
				mostrar_facturas(conn)
				conn.close()
			print("Backup de la DB SQLite")
			shutil.copy('FacturasAFIP.db', 'FacturasAFIP.db.backup')

			input("Presione cualquier tecla para continuar")
			try:
				driver.close()
				driver.quit()
				sp.call(["pkill", "-9","chromedriver"])
				sys.exit()
			except: 
				pass
		##########################################
		############## SECCION ARBA ##############
		##########################################

		elif sele == "2":
			pdb.set_trace()

			facturado_mes_anterior = input("Ingrese total facturado en el mes anterior: ")

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

			#driver.switch_to.window(driver.window_handles[1])
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
			#select_mes.select_by_value(str(datetime.now().month-1))

			desde_dt = datetime.now() + dateutil.relativedelta.relativedelta(months=-1)
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
			driver.close()
			driver.quit()

		elif sele == "3":
			conn = create_connection(database)
			mostrar_facturas(conn)
			conn.close()
			
		elif sele == "4":
			conn = create_connection(database)
			mostrar_facturas(conn)
			nro_borrar = input("\n Eliminar factura con Nº de comprobante: ")
			if nro_borrar.isdigit():
				eliminar_registro(conn, nro_borrar)
				print("Factura eliminada")
			else:
				print(" Nº comprobante inválido")
			conn.close()

		elif sele == "5":
			m_nro = input("\n Nº comprobante: ")
			m_cuit = input(" CUIT destinatario: ")
			m_destinatario = input(" Nombre destinatario: ")
			m_monto = input(" Monto: ")
			m_descripcion = input(" Concepto: ")
			m_desde_sqlite = input(" Desde: ")
			m_hasta_sqlite = input(" Hasta: ")
								
			conn = create_connection(database)
			factura_campos = (m_nro,
							  m_cuit,
							  m_destinatario,
							  m_monto,
							  m_descripcion,
							  m_desde_sqlite,
							  m_hasta_sqlite)
			guardar_factura(conn,factura_campos)
			mostrar_facturas(conn)
			conn.close()
			
		elif sele == "6":
			conn = create_connection(database)
			mostrar_ingresos_mes(conn)
			conn.close()

		elif sele == "7":
			conn = create_connection(database)
			mostrar_montos_DDJJ(conn)
			conn.close()

		accion = input("\n ¿Continuar? [S/n]:")

		if accion == 'n':
			break

except KeyboardInterrupt:
	print('\n Saliendo...\n')
	try:
		driver.close()
		driver.quit()
		sp.call(["pkill", "-9","chromedriver"])
		sys.exit()
	except:
		pass


except:
	raise
	print('\n Saliendo...\n')
	#print('\nSaliendo por error. \Probablemente se haya tomado control manualmente del google chrome...\n')
	try:
		driver.close()
		driver.quit()
		sp.call(["pkill", "-9","chromedriver"])
		sys.exit()
	except:
		print("aca1")
		pass

