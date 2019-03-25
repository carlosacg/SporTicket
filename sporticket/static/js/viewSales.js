$("#get_sales_for_date").submit(function(e){
	e.preventDefault();
	if (document.getElementById("dateO").value == "") {
		alert("Seleccione primero la fecha")
	} else {
		$.ajax({
			url:$(this).attr('action'),
			type:$(this).attr('method'),
			data:$(this).serialize(),
			success: function(json){
				console.log(json);
				if (json.length != 0) {
					fillTable(json);
				} else{
					cleanTable();
					alert("La fecha seleccionada no contiene ventas");
				}
				//
			}
		});
	}				
});

$("#get-bill").submit(function(e){
	e.preventDefault();
	$.ajax({
		url:$(this).attr('action'),
		type:$(this).attr('method'),
		data:$(this).serialize(),
		success: function(json){
			cleanBillTable();
			console.log(json);
			detailsBills = json['detailsBills'];
			fillTableBill(detailsBills, json['total']);
			document.getElementById("numFactura").innerHTML="Factura #"+json['id']
			document.getElementById("fecha").innerHTML=""+json['date']
			document.getElementById("nombre").innerHTML="VENDEDOR: "+json['name']
			document.getElementById("id02").style.display='block';
		}
	});			
});

function fillTableBill(detailsBills, total){
	var table=document.getElementById("bill_table1");		
	for (var i = 0; i < detailsBills.length; i++){
		var table_len=(table.rows.length)-1;
		var row = table.insertRow(table_len).outerHTML="<tr id='row_"+table_len+"'><td>"+detailsBills[i]['eventName']+"</td><td>"+detailsBills[i]['cant']+"</td><td>"+detailsBills[i]['locationName']+"</td><td>"+detailsBills[i]['costo']+"</td><td>"+detailsBills[i]['subtotal']+"</td></tr>"
	}
	document.getElementById('total_bill1').innerHTML = total;
}

function cleanBillTable(){
	var table=document.getElementById("bill_table1");
	var table_len=(table.rows.length);
	if (table_len != 2) {
		table_len = table_len-1;
		for (var i = 1; i < table_len; i++){
			document.getElementById("bill_table1").deleteRow(1);
		}
	}
}

function cleanTable(){
	var table=document.getElementById("sale_table");
	var table_len=(table.rows.length);
	if (table_len != 1) {
		for (var i = 1; i < table_len; i++){
			document.getElementById("sale_table").deleteRow(1);
		}
	}		
}
function fillTable(json) {
	cleanTable()
	var table=document.getElementById("sale_table");
	for (var i = 0; i < json.length; i++) {
		var table_len=(table.rows.length);
		var row = table.insertRow(table_len).outerHTML="<tr id='row_'"+table_len+"> <td id='factura_"+table_len+"'>"+json[i]['id']+"</td><td id='metodo_pago_"+table_len+"'>"+json[i]['metodo_pago']+"</td><td id='total_"+table_len+"'>"+json[i]['total']+"</td><td><a class='w3-button w3-padding w3-dark-grey w3-round w3-small orange-color' data-toggle='tooltip' title='Ver Factura'><button id='"+table_len+"' class='w3-button w3-padding w3-dark-grey w3-round w3-small' type='submit' onclick='showBill(this.id)'>Ver Factura</button></a></td></tr>"
	}
	document.getElementById("sale_table").style.display='block';	
}

function showBill(row){
	document.getElementById("get_bill").value = document.getElementById("factura_"+row).innerHTML;
}