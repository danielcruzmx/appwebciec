from django.contrib import admin

# Register your models here.


from c_sadicarnot.models import Condomino, Estacionamiento, CuentaBanco, \
                            DetalleMovimiento, Documento, Movimiento, Asiento


class DetalleMovtoInlineB(admin.TabularInline):
	model = DetalleMovimiento
	fields = ['descripcion', 'monto', 'cuenta_contable', 'proveedor']
	#list_display = ('cuenta_contable',)
	#list_filter = (('cuenta_contable', admin.RelatedOnlyFieldListFilter),)

	def get_extra(self, request, obj=None, **kwargs):
		extra = 4
		#if(obj):
		#	return extra - DetalleMovimiento.objects.filter(id = request.id).count()
		return extra

	#def cuenta_ingreso(self, request, obj=None, **kwargs):
	#    return	CuentaContable.objects.filter(clave_mayor = '41')

class MovtoAdminB(admin.ModelAdmin):
	list_display = ('id','fecha','concepto','retiro','deposito','condomino','detalle','conciliacion')
	list_filter = ('fecha','condomino',)
	date_hierarchy = 'fecha'
	readonly_fields = ('detalle',)
	ordering = ('-fecha',)
	save_on_top = True 
	inlines = [DetalleMovtoInlineB]

	def concepto(self, request, obj=None, **kwargs):
		return '%s %s' % (request.tipo_movimiento,request.descripcion)

	def detalle(self, request, obj=None, **kwargs):
		cantidades =  DetalleMovimiento.objects.filter(movimiento_id = request.id).values_list('monto', flat = True)
		total = sum(cantidades)
		return total 

	def conciliacion(self, request, obj=None, **kwargs):
		cantidades =  DetalleMovimiento.objects.filter(movimiento_id = request.id).values_list('monto', flat = True)
		total = sum(cantidades)
		if(total != (request.retiro + request.deposito)):
			return 'NO'
		else:
			return 'SI'

class CuentaBancoAdminB(admin.ModelAdmin):
    list_display = ('banco','clabe','apoderado')

class CondominoAdminB(admin.ModelAdmin):
	list_display = ('depto','propietario','cargos','depositos','cuotas')
	search_fields = ('depto','propietario','poseedor')

class EstacionamientoAdminB(admin.ModelAdmin):
	list_display = ('ubicacion',)

class DocumentoAdminB(admin.ModelAdmin):
	list_display = ('tipo_documento','folio','fecha_expedicion','monto_total')

class AuxiliarAdminAB(admin.ModelAdmin):
	list_display = ('id','fecha','tipo_movimiento','debe','haber','descripcion', 'cuenta_contable','condomino')
	list_filter = ('fecha', 'condomino',)
	date_hierarchy = 'fecha'
	ordering = ('-fecha',)	


admin.site.register(Movimiento, MovtoAdminB)
admin.site.register(CuentaBanco, CuentaBancoAdminB)
admin.site.register(Condomino, CondominoAdminB)
admin.site.register(Estacionamiento, EstacionamientoAdminB)
admin.site.register(Documento, DocumentoAdminB)
admin.site.register(Asiento, AuxiliarAdminAB)
