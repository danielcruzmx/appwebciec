from django.db import models

# Create your models here.

class TipoMovimiento(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return '%s' % (self.descripcion)

    class Meta:
        managed = True
        db_table = 'tipo_movimiento'

class TipoDocumento(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return '%s' % (self.descripcion)

    class Meta:
        managed = True
        db_table = 'tipo_documento'

class Situacion(models.Model):
    situacion = models.CharField(max_length=25)

    def __str__(self):
        return '%s' % (self.situacion)

    class Meta:
        managed = True
        db_table = 'situacion'

class CuentaContable(models.Model):
    num_cuenta = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    clave_mayor = models.CharField(max_length=4)
    
    def __str__(self):
        return '%s %s' % (self.num_cuenta, self.descripcion)

    class Meta:
        managed = True
        db_table = 'cuenta_contable'
        ordering = ['num_cuenta']        

class Banco(models.Model):
    clave = models.CharField(max_length=3)
    descripcion = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.clave, self.descripcion)

    class Meta:
        managed = True
        db_table = 'banco'

class Condominio(models.Model):
    nombre = models.CharField(max_length=45)
    calle = models.CharField(max_length=45, blank=True, null=True)
    colonia = models.CharField(max_length=45, blank=True, null=True)
    delegacion = models.CharField(max_length=45, blank=True, null=True)
    ciudad = models.CharField(max_length=45, blank=True, null=True)
    estado = models.CharField(max_length=45, blank=True, null=True)
    cp = models.CharField(max_length=5, blank=True, null=True)
    regimen = models.CharField(max_length=45, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    fecha_constitucion = models.DateField(blank=True, null=True)

    #def ingresos_egresos(self):
    #    return '<a href="/admin/c_olimpo/asiento/?condomino__id__exact=%d">Cargos</a>' % (self.id)

    def __str__(self):
        return '%s' % (self.nombre)        

    class Meta:
        managed = True
        db_table = 'condominio'                        

class Proveedore(models.Model):
    proveedor =  models.CharField(max_length=60)
    domicilio =  models.CharField(max_length=100, blank=True, null=True)
    telefono =  models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True, null=True)
    clabe = models.CharField(max_length=18, null=True , default='0')
  
    def __str__(self):
        return '%s'  % (self.proveedor)

    class Meta:
        managed = True
        db_table = 'proveedore'

class Periodo(models.Model):
    condominio = models.ForeignKey(Condominio)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.condominio)

    class Meta:
        managed = True
        db_table = 'periodo'

#############################################################


