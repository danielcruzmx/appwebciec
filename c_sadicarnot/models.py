from django.db import models
from main.models import Banco, Condominio, Proveedore, TipoDocumento, \
                        Situacion, TipoMovimiento, CuentaContable

# Create your models here.

class Estacionamiento(models.Model):
    ubicacion = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return u'%s' % (self.ubicacion)

    class Meta:
        managed = True
        db_table = 'sadi_estacionamiento'

class CuentaBanco(models.Model):
    cuenta = models.CharField(max_length=20)
    clabe = models.CharField(max_length=18)
    apoderado = models.CharField(max_length=60)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_saldo = models.DateField(blank=True, null=True)
    situacion = models.IntegerField(blank=True, null=True)
    banco = models.ForeignKey(Banco, related_name='sadi_banco_cuenta')
    condominio = models.ForeignKey(Condominio, related_name='sadi_cuenta_condominio')
    tipo_cuenta = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s %s' % (self.condominio, self.clabe, self.apoderado[:10])

    class Meta:
        managed = True
        db_table = 'sadi_cuenta_banco'

class Condomino(models.Model):
    depto = models.CharField(max_length=15, blank=True, null=True)
    propietario = models.CharField(max_length=60, blank=True, null=True)
    poseedor = models.CharField(max_length=60, blank=True, null=True)
    ubicacion = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=25, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_escrituracion = models.DateField(blank=True, null=True)
    referencia = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    condominio = models.ForeignKey(Condominio, related_name='sadi_condomino_condominio_id')
    estacionamiento = models.ManyToManyField(Estacionamiento, related_name='sadi_condomino_estacionamiento_id')

    def __str__(self):
        return '%s %s' % (self.depto, self.poseedor)

    #http://127.0.0.1:8000/admin/c_olimpo/asiento/?condomino__id__exact=9

    def cargos(self):
        return '<a href="/admin/c_sadicarnot/asiento/?condomino__id__exact=%d">Cargos view</a>' % (self.id)

    #http://127.0.0.1:8000/admin/c_olimpo/movimiento/?condomino__id__exact=10

    def depositos(self):
        return '<a href="/admin/c_sadicarnot/movimiento/?condomino__id__exact=%d">Depositos view</a>' % (self.id)

    def cuotas(self):
        return '<a href="/explorer/5/download?format=csv&params=depto:\'%s\'">Cuotas *.csv</a>' % (self.depto)
        

    cargos.allow_tags = True
    depositos.allow_tags = True 
    cuotas.allow_tags = True

    class Meta:
        managed = True
        db_table = 'sadi_condomino'
        ordering = ['depto']

class Documento(models.Model):
    folio = models.IntegerField(blank=False, null=False)
    fecha_expedicion = models.DateField()
    monto_total = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    notas = models.CharField(max_length=45, blank=True, null=True)
    situacion = models.ForeignKey(Situacion, blank=True, null=True, related_name='sadi_recibo_situacion_id')
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True, related_name='sadi_recibo_tipodoc_id')

    def __str__(self):
        return '%d %s' % (self.folio, self.tipo_documento)

    class Meta:
        managed = True
        db_table = 'sadi_documento'

class Movimiento(models.Model):
    cuenta_banco = models.ForeignKey(CuentaBanco, related_name='sadi_movimiento_cuenta_id', default = 1)
    fecha = models.DateField(blank=True, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, blank=True, null=True, related_name='sadi_movimiento_tipo_movimiento_id')
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    condomino = models.ForeignKey(Condomino, related_name='sadi_movimiento_condomino_id')
    retiro = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    deposito = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    documento = models.ForeignKey(Documento, related_name='sadi_movimiento_documento_id', default=0)

    def __str__(self):
        return u'%d %s %d %s' % (self.id, self.fecha.strftime('%d/%m/%Y'), self.deposito, self.descripcion[:15])

    class Meta:
        managed = True
        db_table = 'sadi_movimiento'
        ordering = ['fecha']

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, verbose_name = ('Movto'), on_delete = models.CASCADE, related_name='sadi_mov_detalle')
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    monto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable Ingreso/Egreso'), on_delete = models.CASCADE, related_name='sadi_cta_detalle')
    proveedor = models.ForeignKey(Proveedore, verbose_name = ('Proveedor'), on_delete = models.CASCADE, related_name='sadi_prov_detalle')

    def __str__(self):
        return '%s %s %s' % (self.descripcion, self.monto, self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'sadi_detalle_movimiento'
        ordering = ['movimiento']

class Asiento(models.Model):
    fecha = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, blank=True, null=True, related_name='sadi_auxiliar_tipo_movimiento_id')
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    debe = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    haber = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    saldo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default=0)
    cuenta_contable =  models.ForeignKey(CuentaContable, verbose_name = ('Cuenta Contable'), on_delete = models.CASCADE, related_name='sadi_asiento_cuenta')
    condomino = models.ForeignKey(Condomino, related_name='sadi_auxiliar_condomino_id', default=67)
    a_favor = models.ForeignKey(Proveedore, related_name='sadi_auxiliar_proveedor_id', default=1)

    def __str__(self):
        return u'%d %s %d %d %s %s' % (self.id, self.fecha.strftime('%d/%m/%Y'), self.debe, self.haber, self.descripcion[:15], self.cuenta_contable)

    class Meta:
        managed = True
        db_table = 'sadi_asiento'
        ordering = ['fecha']    