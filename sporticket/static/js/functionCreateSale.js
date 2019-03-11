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

function calcularTotalF(){
	var table=document.getElementById("bill_table1");
		var table_len=(table.rows.length)-1;
		var total=0;
	for (var i = 1; i < table_len; i++) {
		var subtotal = parseInt(document.getElementById("subtotal_f_"+i).innerHTML);
		total += subtotal;
	}
	document.getElementById("total_bill1").innerHTML=total;
}

function calcularSubotales(){
	var table=document.getElementById("bill_table");
		var table_len=(table.rows.length)-1;
	for (var i = 1; i < table_len; i++) {
		var cant = document.getElementById("cantidad_boletos_"+i).innerHTML;
		var cost = document.getElementById("costo_"+i).innerHTML;
		document.getElementById("subtotal_"+i).innerHTML=(cant*cost);
	}
}

function calcularSubotalesF(){
	var table=document.getElementById("bill_table1");
		var table_len=(table.rows.length)-1;
	for (var i = 1; i < table_len; i++) {
		var cant = document.getElementById("cantidad_boletos_f_"+i).innerHTML;
		var cost = document.getElementById("costo_f_"+i).innerHTML;
		document.getElementById("subtotal_f_"+i).innerHTML=(cant*cost);
	}
}

function getCosto(selectTribuna){
	var costoTribuna = document.getElementById(selectTribuna+"_cost");
	//console.log("costo tribuna : "+costoTribuna.firstChild.nodeValue);
	return costoTribuna.innerHTML;
}

function addRow(){
	var selectTribuna = document.getElementById('select_tribuna');
	var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
	var cantidadBoletos = document.getElementById('cantidad').value;
	//console.log("Cantidad de boletos :"+cantidadBoletos);
	//console.log(selectedOption.value + ': ' + selectedOption.text);
	var table=document.getElementById("bill_table");
		var table_len=(table.rows.length)-1;
		//console.log("tamaño de la tabla : "+table_len);
		 var row = table.insertRow(table_len).outerHTML="<tr id='row_"+table_len+"'> <td id='cantidad_boletos_"+table_len+"'>"+cantidadBoletos+"</td> <td id='ubicacion_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_"+table_len+"'></td></tr>";
		 calcularSubotales();
		 calcularTotal();
}

function addRowF(){
	var selectTribuna = document.getElementById('select_tribuna');
	var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
	var cantidadBoletos = document.getElementById('cantidad').value;
	//console.log("Cantidad de boletos :"+cantidadBoletos);
	//console.log(selectedOption.value + ': ' + selectedOption.text);
	var table=document.getElementById("bill_table1");
		var table_len=(table.rows.length)-1;
		//console.log("tamaño de la tabla : "+table_len);
		 var row = table.insertRow(table_len).outerHTML="<tr id='row_f_"+table_len+"'> <td id='cantidad_boletos_f_"+table_len+"'>"+cantidadBoletos+"</td> <td id='ubicacion_f_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_f_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_f_"+table_len+"'></td></tr>";
		 calcularSubotalesF();
		 calcularTotalF();
}

function addRowMain(){
	addRow();
	addRowF();
}