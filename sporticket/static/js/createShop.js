var ubications=[];
    var quantitys=[];
	var event_id;
	var pago;
	var fila=0;
	var total=0;
	function calcularTotal(){
		var table=document.getElementById("bill_table");
 		var table_len=(table.rows.length)-1;
 		var total=0;
		for (var i = 1; i < table_len; i++) {
			var subtotal = parseInt(document.getElementById("subtotal_"+i).innerHTML);
			total += subtotal;
		}
		document.getElementById("total_bill").innerHTML=total;
	}

	function calcularSubotales(){
		var table=document.getElementById("bill_table");
 		var table_len=(table.rows.length)-1;
		for (var i = 1; i < table_len; i++) {
			var cant = document.getElementById("cant_boletos_"+i).value;
			var cost = parseInt(document.getElementById("costo_"+i).innerHTML);
			document.getElementById("subtotal_"+i).innerHTML=(cant*cost);
		}
	}

	function getCosto(selectTribuna){
		var costoTribuna = document.getElementById(selectTribuna+"_cost");
		return costoTribuna.innerHTML;
	}
	function addRow(){
		var selectTribuna = document.getElementById('select_tribuna');
		var selectPago = document.getElementById('select_pago');
		var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
		var cantidadBoletos = document.getElementById('cantidad').value;
		var selectedPago = selectPago.options[selectPago.selectedIndex];
		pago= selectedPago.text
		event_id =  document.getElementById('event_id').value;
		var table=document.getElementById("bill_table");
 		var table_len=(table.rows.length)-1;
		if(parseInt(cantidadBoletos).toString() == 'NaN'){
		}else{

			for(var i=1; i<=table_len; i++){
				if(!(document.getElementById("ubicacion_"+i)==null)){// Si la tabla no esta vacia
					if(document.getElementById("ubicacion_"+i).innerHTML == selectedOption.text){ //Si la ubicacion insertada es igual a la de una fila
						cantidadOld = parseInt(document.getElementById("cant_boletos_"+i).value);
						cantidadNew= cantidadOld+parseInt(cantidadBoletos);
						document.getElementById("cantidad_boletos_"+i).innerHTML="<input style='display:none' id='cant_boletos_"+i+"' value="+cantidadNew+">"+cantidadNew;
						quantitys[i-1]=cantidadNew;
						break;
					}
				}else{// Si la tabla esta vacia inserto el registros
					table.insertRow(table_len).outerHTML="<tr id='row_"+table_len+"'> <td id='cantidad_boletos_"+table_len+"'> <input style='display:none' id='cant_boletos_"+table_len+"' value='"+cantidadBoletos+"'>"+cantidadBoletos+"</td> <td id='ubicacion_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_"+table_len+"'></td> <td><a data-toggle='tooltip' title='Aumentar boletos'><button id='"+table_len+"' onclick='addTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-plus'></i></button></a></td>  <td><a data-toggle='tooltip' title='Disminuir boletos'><button id='"+table_len+"' onclick='minusTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-minus'></i></button></a></td> </tr>";
					quantitys.push(cantidadBoletos)
					ubications.push(selectedOption.text)
					break;
				}
				if(i==table_len){ //Si recorri toda la tabla y no hay ubicacion igual, inserto el registro
					table.insertRow(table_len).outerHTML="<tr id='row_"+table_len+"'> <td id='cantidad_boletos_"+table_len+"'> <input style='display:none' id='cant_boletos_"+table_len+"' value='"+cantidadBoletos+"'>"+cantidadBoletos+"</td> <td id='ubicacion_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_"+table_len+"'></td> <td><a data-toggle='tooltip' title='Aumentar boletos'><button id='"+table_len+"' onclick='addTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-plus'></i></button></a></td>  <td><a data-toggle='tooltip' title='Disminuir boletos'><button id='"+table_len+"' onclick='minusTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-minus'></i></button></a></td> </tr>";
					quantitys.push(cantidadBoletos)
					ubications.push(selectedOption.text)
				}
			}
			calcularSubotales();
			calcularTotal();
		}

	}

	function addTicket(fila){
		var cantidad=document.getElementById('cant_boletos_'+fila).value;
		var cantView=document.getElementById("cantidad_boletos_"+fila).innerHTML;
		cantView=parseInt(cantidad)+1
		document.getElementById("cantidad_boletos_"+fila).innerHTML="<input style='display:none' id='cant_boletos_"+fila+"' value="+cantView+">"+cantView;
		quantitys[fila-1]=parseInt(cantidad)+1;
		calcularSubotales();
 		calcularTotal();
	}

	function minusTicket(fila){
		var cantidad=document.getElementById('cant_boletos_'+fila).value;
		if(cantidad > 1){
			var cantView=document.getElementById("cantidad_boletos_"+fila).innerHTML;
			cantView=parseInt(cantidad)-1
			document.getElementById("cantidad_boletos_"+fila).innerHTML="<input style='display:none' id='cant_boletos_"+fila+"' value="+cantView+">"+cantView;
			quantitys[fila-1]=parseInt(cantidad)-1;
			calcularSubotales();
			calcularTotal();	
		}
	}

	function addRowMain(){
		addRow();
	}

    function getCookie(c_name){
    if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }

    function finishShop(){
        var jsonQuantitys = JSON.stringify(quantitys);
        var jsonUbications = JSON.stringify(ubications);
		total=parseInt(document.getElementById("total_bill").innerHTML);
        console.log(quantitys)
        console.log(jsonUbications)
        $.ajax({
            url:'/sales_ajax/',
            dataType: 'json',
            data: {
				'jsonUbications':jsonUbications,
				'jsonQuantitys':jsonQuantitys,
				'event_id':event_id,
				'pago':pago,
				'total':total
            },
            beforeSend: function () {
                console.log('Procesando')        
            },
            success: succesRequest
        });
    }

	function reload(){
		location.reload()
	}

	function finishShopMain(){
		finishShop();
		//reload();
	}

	function succesRequest(result){
		if(result.status =='success'){
			$(document).ready(function(){
				$("#success").toggle(100);
				$("#success").fadeOut(3500);
			});
			setTimeout("reload()", 2500);
		}else{
			const interval = 2000;
			window.setTimeout(finishShop,interval)
		}

	}