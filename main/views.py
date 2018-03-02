from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# UTILS
def dictfetchall(cursor):
	desc = cursor.description
	return [
       dict(zip([col[0] for col in desc],row))
       for row in cursor.fetchall()
	]

# Raiz redirige a ADMIN
def home(request):
	return HttpResponseRedirect('/admin/main')

# Clases de REST
class TotalIngresosEgresosViewSet(APIView):

	def get(self, request, *args, **kw):
		cursor = connection.cursor()
		valorIni = kw['fec_ini']
		valorFin = kw['fec_fin']
		condominio = kw['condominio'].upper()

		if condominio == 'OLIMPO':
			query = '''
				SELECT  co.nombre as CONDOMINIO,
				        c.clabe as CUENTA,
				        min(m.fecha) as FECHAINI,
				        max(m.fecha) as FECHAFIN,
				        sum(m.deposito) as DEPOSITOS,
				        sum(m.retiro) as RETIRO,
				        sum(m.deposito) - sum(m.retiro) as SALDO
				FROM    olimpo_movimiento m, olimpo_cuenta_banco c, condominio co
				WHERE   m.cuenta_banco_id = c.id
				AND     c.condominio_id = co.id
				AND     m.fecha >= '%s'
				AND     m.fecha <= '%s'
				GROUP BY nombre, clabe
			''' % (valorIni, valorFin)
		elif condominio == 'SADICARNOT':
			query = '''
				SELECT  co.nombre as CONDOMINIO,
				        c.clabe as CUENTA,
				        min(m.fecha) as FECHAINI,
				        max(m.fecha) as FECHAFIN,
				        sum(m.deposito) as DEPOSITOS,
				        sum(m.retiro) as RETIRO,
				        sum(m.deposito) - sum(m.retiro) as SALDO
				FROM    sadi_movimiento m, sadi_cuenta_banco c, condominio co
				WHERE   m.cuenta_banco_id = c.id
				AND     c.condominio_id = co.id
				AND     m.fecha >= '%s'
				AND     m.fecha <= '%s'
				GROUP BY nombre, clabe
			''' % (valorIni, valorFin)
		else :
			query = ''' SELECT 'Sin datos' as '%s' FROM dual ''' % condominio	
		cursor.execute(query)
		totales_list = dictfetchall(cursor)
		response = Response(totales_list, status=status.HTTP_200_OK)
		return response

class CuotasDeptoMesViewSet(APIView):

    def get(self, request, *args, **kw):
        cursor = connection.cursor()
        valor = kw['mes_anio']
        condominio = kw['condominio'].upper()
        #print valor
        if condominio == 'SADICARNOT':
            query = '''
                    SELECT '%s' as MES,
                           nombre as CONDOMINIO,
                           depto as DEPTO,
                           propietario as PROPIETARIO,
                           sum(deposito) as DEPOSITO
                    FROM sadi_movimiento, sadi_cuenta_banco, sadi_condomino, condominio
                    WHERE sadi_movimiento.cuenta_banco_id = sadi_cuenta_banco.id
                          and date_format(fecha,'%%m-%%Y') = '%s'
                          and sadi_condomino.id = sadi_movimiento.condomino_id
                          and sadi_condomino.depto != '0000'
                          and condominio.nombre = 'SADICARNOT'
                          and deposito > 0
                    GROUP by 1,2,3,4
                    UNION
                    SELECT '%s' as MES,
                           nombre as CONDOMINIO,
                           depto as DEPTO,
                           propietario AS PROPIETARIO,
                           0 AS DEPOSITO
                    FROM sadi_condomino, condominio
                    WHERE sadi_condomino.condominio_id = condominio.id
                          and depto NOT IN
                             (SELECT depto
                              FROM sadi_movimiento,
                                   sadi_cuenta_banco,
                                   sadi_condomino
                              WHERE sadi_movimiento.cuenta_banco_id = sadi_cuenta_banco.id
                              AND sadi_condomino.id = sadi_movimiento.condomino_id
                              AND sadi_condomino.depto != '0000'
                              AND date_format(fecha,'%%m-%%Y') = '%s'
                              AND deposito > 0)
                     AND depto != '0000'  
                     AND condominio.nombre = '%s'     
                     ORDER BY depto
            ''' % (valor, valor, valor, valor, condominio)
        elif condominio == 'OLIMPO':
            query = '''
                SELECT '%s' as MES,
                       nombre as CONDOMINIO,
                       depto as DEPTO,
                       propietario as PROPIETARIO,
                       sum(deposito) as DEPOSITO
                FROM olimpo_movimiento, olimpo_cuenta_banco, olimpo_condomino, condominio
                WHERE olimpo_movimiento.cuenta_banco_id = olimpo_cuenta_banco.id
                      and date_format(fecha,'%%m-%%Y') = '%s'
                      and olimpo_condomino.id = olimpo_movimiento.condomino_id
                      and olimpo_condomino.depto != '000'
                      and condominio.nombre = 'SADICARNOT'
                      and deposito > 0
                GROUP by 1,2,3,4
                UNION
                SELECT '%s' as MES,
                       nombre as CONDOMINIO,
                       depto as DEPTO,
                       propietario AS PROPIETARIO,
                       0 AS DEPOSITO
                FROM olimpo_condomino, condominio
                WHERE olimpo_condomino.condominio_id = condominio.id
                      and depto NOT IN
                         (SELECT depto
                          FROM olimpo_movimiento,
                               olimpo_cuenta_banco,
                               olimpo_condomino
                          WHERE olimpo_movimiento.cuenta_banco_id = olimpo_cuenta_banco.id
                          AND olimpo_condomino.id = olimpo_movimiento.condomino_id
                          AND olimpo_condomino.depto != '000'
                          AND date_format(fecha,'%%m-%%Y') = '%s'
                          AND deposito > 0)
                 AND depto != '0000'  
		         AND condominio.nombre = '%s'     
                 ORDER BY depto
            ''' % (valor, valor, valor, valor, condominio)
        else:
            query = ''' SELECT 'Sin datos' as '%s' FROM dual ''' % condominio
        #
        cursor.execute(query)
        cuotas_list = dictfetchall(cursor)
        #
        response = Response(cuotas_list, status=status.HTTP_200_OK)
        return response

class CuotasViewSet(APIView):

    def get(self, request, *args, **kw):
        cursor = connection.cursor()
        valor = kw['depto_id']
        cursor.callproc("saldo_movimientos_depto", [valor])
        #
        desc = ['id', 'fecha', 'tipo', 'descripcion', 'condomino', 'cargo', 'abono', 'saldo']
        cuotas_list = []
        for row in cursor.stored_results():
            for r in row.fetchall():
                cuotas_list.append(dict(zip(desc,r)))
        #
        response = Response(cuotas_list, status=status.HTTP_200_OK)
        return response
