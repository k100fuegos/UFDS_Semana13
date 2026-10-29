from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from ..models import Cliente, DetalleVenta, Producto, TipoPago, Venta


@login_required
def lista_ventas(request):
    ventas = (
        Venta.objects.select_related('cliente', 'usuario', 'tipo_pago')
        .all()
        .order_by('-fecha', '-id')
    )
    paginador = Paginator(ventas, 10)

    pagina = request.GET.get('page')
    ventas_paginadas = paginador.get_page(pagina)

    return render(
        request, "venta/lista.html", context={'ventas': ventas_paginadas}
    )


@login_required
def registrar_venta(request):
    clientes = Cliente.objects.all().order_by('nombre')
    tipos_pago = TipoPago.objects.all().order_by('nombre')
    productos = Producto.objects.filter(stock__gt=0).order_by('nombre')

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        tipo_pago_id = request.POST.get("tipo_pago")
        producto_ids = request.POST.getlist("producto_id[]")
        cantidades = request.POST.getlist("cantidad[]")

        if not cliente_id or not tipo_pago_id:
            messages.error(
                request, "Debe seleccionar un cliente y un tipo de pago."
            )
            return render(
                request,
                "venta/registrar.html",
                {
                    'clientes': clientes,
                    'tipos_pago': tipos_pago,
                    'productos': productos,
                },
            )

        if not producto_ids or len(producto_ids) == 0:
            messages.error(
                request, "Debe agregar al menos un producto a la venta."
            )
            return render(
                request,
                "venta/registrar.html",
                {
                    'clientes': clientes,
                    'tipos_pago': tipos_pago,
                    'productos': productos,
                },
            )

        cliente = get_object_or_404(Cliente, id=cliente_id)
        tipo_pago = get_object_or_404(TipoPago, id=tipo_pago_id)

        items_venta = []
        total_venta = Decimal("0.00")

        # Validar productos y stock disponible
        for p_id, cant_str in zip(producto_ids, cantidades):
            try:
                cant = int(cant_str)
            except (ValueError, TypeError):
                cant = 0

            if cant <= 0:
                continue

            try:
                prod = Producto.objects.get(id=p_id)
            except Producto.DoesNotExist:
                messages.error(
                    request, f"Producto con ID {p_id} no encontrado."
                )
                return render(
                    request,
                    "venta/registrar.html",
                    {
                        'clientes': clientes,
                        'tipos_pago': tipos_pago,
                        'productos': productos,
                    },
                )

            if prod.stock < cant:
                messages.error(
                    request,
                    f"Stock insuficiente para '{prod.nombre}'. Disponible: {prod.stock}, solicitado: {cant}.",
                )
                return render(
                    request,
                    "venta/registrar.html",
                    {
                        'clientes': clientes,
                        'tipos_pago': tipos_pago,
                        'productos': productos,
                    },
                )

            subtotal = prod.precio_venta * cant
            total_venta += subtotal
            items_venta.append({
                'producto': prod,
                'cantidad': cant,
                'precio_unitario': prod.precio_venta,
                'subtotal': subtotal,
            })

        if not items_venta:
            messages.error(
                request,
                "Debe seleccionar cantidades válidas mayores a cero para los productos.",
            )
            return render(
                request,
                "venta/registrar.html",
                {
                    'clientes': clientes,
                    'tipos_pago': tipos_pago,
                    'productos': productos,
                },
            )

        # Registro atómico de la venta, detalles y actualización de inventario
        with transaction.atomic():
            nueva_venta = Venta.objects.create(
                cliente=cliente,
                usuario=request.user,
                tipo_pago=tipo_pago,
                total=total_venta,
            )

            for item in items_venta:
                DetalleVenta.objects.create(
                    venta=nueva_venta,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio_unitario'],
                    subtotal=item['subtotal'],
                )
                item['producto'].stock -= item['cantidad']
                item['producto'].save()

        messages.success(
            request, f"Venta #{nueva_venta.id} registrada con éxito."
        )
        return redirect("detalle_venta", id=nueva_venta.id)

    return render(
        request,
        "venta/registrar.html",
        {
            'clientes': clientes,
            'tipos_pago': tipos_pago,
            'productos': productos,
        },
    )


@login_required
def detalle_venta(request, id):
    venta = get_object_or_404(
        Venta.objects.select_related('cliente', 'usuario', 'tipo_pago'), id=id
    )
    detalles = venta.detalles.select_related('producto').all()

    return render(
        request,
        "venta/detalle.html",
        {
            'venta': venta,
            'detalles': detalles,
        },
    )

