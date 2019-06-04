#!/usr/bin/env python

timeout = 20
GuardarEnDB = True

pagina_login = 'https://auth.afip.gob.ar/contribuyente_/login.xhtml'
pagina_generar_comprobantes = 'https://serviciosjava2.afip.gob.ar/rcel/jsp/menu_ppal.jsp'
pagina_princpal_arba = 'http://www.arba.gov.ar/DatosContacto/DatosContactoRedirect.asp?destino=http://www.arba.gov.ar/Gestionar/Gestionar_Default.asp'

unidades_medida = " unidades"
pto_venta = '1'
#tipo_comprobante = '2'
tipo_comprobante_txt = 'Factura C'
conceptos = '2' #SERVICIOS

destinos_nombres = {'1' : 'Para juan',
                    '2' : 'Para pepito',
                    '3' : 'Para fulano'}

# CUIT's de los receptores:
destinos = {'1' : 'cuit1',
            '2' : 'cuit2',
            '3' : 'cuit3'}

condiciones = {'1' : '4',
               '2' : '4',
               '3' : '1'} 
#1 = iva resp inscr
#4 = Sujeto Exento

cuits_nm = {'cuit1' : 'empresa 1',
            'cuit2' : 'cliente 1',
            'cuit2' : 'cleinte 2'}

cuits = {'1': 'cuit1',
         '2': 'cuit2',
         '3': 'cuit3'}

montos = {'1' : '10000',
          '2' : '20000', 
          '3' : '30000'}

detalles = {'1' : 'Por servicios informáticos...', 
             '2' : 'Mantenimiento DB y...', 
             '3' : 'Servicios De Informática ...'}

selecc = '\n0: +++ Generar todas las Facturas +++ \n'

for destino in destinos_nombres:
    selecc += destino+": " + destinos_nombres.get(destino)+"\n"
