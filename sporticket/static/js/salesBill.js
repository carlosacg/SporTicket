function prueba(){
    console.log("hola : ");
    //var x = document.getElementById("main_table").rows[1].cells.namedItem("Oeste_id").innerHTML;
    //console.log("this is : "+x);
    //console.log("</td><td id='"+obj_avaliables_tickets['name']+"_id' style='display:none'>");
}
function createJson(){
    var jsonFinal={};
    var total = parseInt(document.getElementById("total_bill").innerHTML);
    var metodo_pago = document.getElementById("select_metodo_pago")
    var selectedOption = metodo_pago.options[metodo_pago.selectedIndex];
    jsonFinal.total = total;
    jsonFinal.metodo_pago = selectedOption.text;
    jsonFinal.tickets = [];
    var table=document.getElementById("bill_table");
    var table_len=(table.rows.length)-1;
    for (var i = 1; i < table_len; i++) {
        var ticketsIn = {};
        var id_location = document.getElementById('id_location_'+i).innerHTML;
        var event_name = document.getElementById('evento_'+i).innerHTML;
        var cant = document.getElementById('cantidad_boletos_'+i).innerHTML;
        ticketsIn = {'id_location':id_location, 'event_name':event_name, 'cant':cant};
        jsonFinal['tickets'].push(ticketsIn);
    }
    //console.log(jsonFinal);
    //console.log(JSON.stringify(jsonFinal))
    return JSON.stringify(jsonFinal);
    //return jsonFinal;
}
function getIdLocation(numRow,location){
    var idLocation = document.getElementById("main_table").rows[numRow].cells.namedItem(location+"_id").innerHTML;
    return idLocation;
}
function comprobarCantidadBoletos(tribuna,cantidad){
    var prueb = parseInt(document.getElementById(tribuna+'_cant').innerHTML);
    if(prueb>=cantidad){
        //console.log("La cantidad ingresada puede pasar");
        return true;
    } else {
        alert("La cantidad ingresada supera la disponibilidad");
        return false;
    }
}

function limpiarInputs(){
    document.getElementById('select_tribuna').selectedIndex="0";
    document.getElementById('cantidad').min=0;
    document.getElementById('cantidad').value="";
}
function comprobar(){
    if (document.getElementById('cantidad').value=="") {alert("No a escogido la cantidad de boletos")} else {
        if (document.getElementById('select_tribuna').selectedIndex==0) {alert("No a seleccionado la tribuna")} else{
            var nombre_evento=document.getElementById('nombre_evento').innerHTML;
            var table=document.getElementById("bill_table");
            var table_len=(table.rows.length)-1;
            if (table_len==1) {
                addRowMain();
            } else {
                var selectTribuna = document.getElementById('select_tribuna');
                var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
                var cantidadBoletos = document.getElementById('cantidad').value;
                var cantidadFinal =0;
                for (var i = 1; i < table_len; i++) {
                    var ubicacionRow = document.getElementById("ubicacion_"+i).innerHTML;
                    var eventoRow = document.getElementById("evento_"+i).innerHTML;
                    //console.log("evento.ROW : "+eventoRow);
                    //console.log("evento.name : "+nombre_evento);
                    //console.log("selectedOption : "+selectedOption.text);
                    //console.log("ubicacion.ROW : "+ubicacionRow);
                    if ((selectedOption.text == ubicacionRow)&&(nombre_evento==eventoRow)) {
                        console.log("Paso");
                        var cantidadRow = document.getElementById("cantidad_boletos_"+i).innerHTML;
                        cantidadFinal = parseInt(cantidadRow)+parseInt(cantidadBoletos);
                        console.log(cantidadFinal);
                        if (comprobarCantidadBoletos(ubicacionRow,cantidadFinal)) {
                            document.getElementById("cantidad_boletos_"+i).innerHTML=cantidadFinal;	
                             calcularSubotales();
                             calcularTotal();
                             calcularSubotalesF();
                             calcularTotalF();
                             limpiarInputs();
                             break;
                        }			 		
                    } else{
                        if (i==(table_len-1)) {addRowMain();}		
                    }
                }
            }
        }
    }		
}
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

function addTicket(fila){
    var cantView=parseInt(document.getElementById('cantidad_boletos_'+fila).innerHTML);
    var cant=cantView+1;
    document.getElementById("cantidad_boletos_"+fila).innerHTML=cant;
    document.getElementById("cantidad_boletos_f_"+fila).innerHTML=cant;
    calcularSubotales();
     calcularTotal();
    calcularSubotalesF();
    calcularTotalF();
}

function minusTicket(fila){
    var cantView=parseInt(document.getElementById('cantidad_boletos_'+fila).innerHTML);
    if(cantView > 1){
        var cant=cantView-1;
        document.getElementById("cantidad_boletos_"+fila).innerHTML=cant;
        document.getElementById("cantidad_boletos_f_"+fila).innerHTML=cant;
        calcularSubotales();
        calcularTotal();	
        calcularSubotalesF();
        calcularTotalF();
    } else {
        deleteRow(fila);
    }
}

function deleteRow(row){
    var rest = parseInt(document.getElementById('subtotal_'+row).innerHTML);
    document.getElementById('total_bill').innerHTML = parseInt(document.getElementById('total_bill').innerHTML)-rest;
    document.getElementById('total_bill1').innerHTML = parseInt(document.getElementById('total_bill').innerHTML);
    document.getElementById("bill_table").deleteRow(row);
    document.getElementById("bill_table1").deleteRow(row);
}

function addRow(){
    var nombre_evento=document.getElementById('nombre_evento').innerHTML;
    var selectTribuna = document.getElementById('select_tribuna');
    var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
    var cantidadBoletos = document.getElementById('cantidad').value;
    //console.log("aqui estoy probando")
    //console.log("Cantidad de boletos :"+cantidadBoletos);
    //consol//e.log(selectedOption.value + ': ' + selectedOption.text);
    //console.log("AQUI POSIBLE ERROR : "+selectedOption.text+" -- "+cantidadBoletos);
    if (comprobarCantidadBoletos(selectedOption.text,cantidadBoletos)){
        var table=document.getElementById("bill_table");
         var table_len=(table.rows.length)-1;
          var row = table.insertRow(table_len).outerHTML="<tr id='row_"+table_len+"'> <td id ='id_event_"+table_len+"' style='display:none'></td><td id='evento_"+table_len+"'>"+nombre_evento+"</td><td id='cantidad_boletos_"+table_len+"'>"+cantidadBoletos+"</td> <td id='ubicacion_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_"+table_len+"'></td><td><a data-toggle='tooltip' title='Aumentar boletos'><button id='"+table_len+"' onclick='addTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-plus'></i></button></a> <a data-toggle='tooltip' title='Disminuir boletos'><button id='"+table_len+"' onclick='minusTicket(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-minus'></i></button></a> <a data-toggle='tooltip' title='Eliminar fila'><button id='"+table_len+"' onclick='deleteRow(this.id)' class='w3-button w3-padding-small w3-dark-grey w3-circle'><i class='fa fa-remove'></i></button></a></td> <td id='id_location_"+table_len+"' style='display:none'>"+getIdLocation(selectTribuna.selectedIndex,selectedOption.text)+"</td></tr>";
          calcularSubotales();
          calcularTotal();
          var table_len1=(table.rows.length)-1;
          return true;
    } else {
        return false;
    }
    
}
function addRowF(){
    var nombre_evento=document.getElementById('nombre_evento').innerHTML;
    var selectTribuna = document.getElementById('select_tribuna');
    var selectedOption = selectTribuna.options[selectTribuna.selectedIndex];
    var cantidadBoletos = document.getElementById('cantidad').value;
    //console.log("Cantidad de boletos :"+cantidadBoletos);
    //console.log(selectedOption.value + ': ' + selectedOption.text);
    var table=document.getElementById("bill_table1");
     var table_len=(table.rows.length)-1;
     //console.log("tamaño de la tabla : "+table_len);
     var row = table.insertRow(table_len).outerHTML="<tr id='row_f_"+table_len+"'> <td 'evento_"+table_len+"'>"+nombre_evento+"</td><td id='cantidad_boletos_f_"+table_len+"'>"+cantidadBoletos+"</td> <td id='ubicacion_f_"+table_len+"'>"+selectedOption.text+"</td><td id='costo_f_"+table_len+"'>"+getCosto(selectedOption.text)+"</td><td id='subtotal_f_"+table_len+"'></td></tr>";
     calcularSubotalesF();
     calcularTotalF();	
         
}
function addRowMain(){
    if(addRow()){
        addRowF();
    }		
    limpiarInputs();
}


$("#get-events").submit(function(e){
    e.preventDefault();
    if(document.getElementById('select_buscar').selectedIndex==0){
        alert("No a seleccionado un tipo de evento");
    } else {
        $.ajax({
        url:$(this).attr('action'),
        type:$(this).attr('method'),
        data:$(this).serialize(),
        success: function(json){
            console.log(json);
            var table=document.getElementById("search_table");
            var table_len=(table.rows.length);
            if (table_len!=1){
                for (var i = 1; i <table_len; i++) {
                    document.getElementById("search_table").deleteRow(1);
                }					
            }
            table_len=1;
            //console.log("TAMAÑO DE JSON :"+json.length)
            var len = table_len;
            for (var i = 0;  i<json.length; i++) {
                var obj_event = json[i];
                var row = table.insertRow(len).outerHTML="<tr id='row_st_"+len+"'> <td id='event_s_"+len+"'>"+obj_event['name']+"</td> <td id='capacidad_s_"+len+"'>"+obj_event['capacity']+"</td><td id='fecha_s_"+len+"'>"+obj_event['initial_date']+"</td><td id='selec_"+len+"'><buttom class='w3-button w3-padding w3-dark-grey w3-circle' type='submit' onclick='selectNewEvent("+len+")'><i class='fa fa-check'> Seleccionar</i></buttom></td></tr>";
                len += 1;
            }			
        }
        });
    }		
});

$("#get-new-event").submit(function(e){
    e.preventDefault();
    document.getElementById('id03').style.display='none';
    $.ajax({
        url:$(this).attr('action'),
        type:$(this).attr('method'),
        data:$(this).serialize(),
        success: function(json){
            //console.log("recien horneado : ");
            //console.log(json);
            document.getElementById("nombre_evento").innerHTML=json.event['name']
            //console.log(json.event['name']);
            //console.log(json.avalibleTicket);
            //console.log(json.avalibleTicket.length);
            var table=document.getElementById("main_table");
            var table_len=(table.rows.length);
            if (table_len!=1){
                for (var i = 1; i <table_len; i++) {
                    document.getElementById("main_table").deleteRow(1);
                }					
            }
            table_len=1;
            var len = table_len;
            for (var i = 0;  i<json.avalibleTicket.length; i++) {
                var obj_avaliables_tickets = json.avalibleTicket[i];
                //console.log("SUPER PROBA : "+obj_avaliables_tickets['name']+"_cant = "+obj_avaliables_tickets['count']);
                //console.log("SUPER PROBA : "+obj_avaliables_tickets['name']+"_id ="+obj_avaliables_tickets['id']);
                console.log("</td><td id='"+obj_avaliables_tickets['name']+"_id' style='display:none'>");
                var row = table.insertRow(len).outerHTML="<tr id='row_ticktet_"+len+"'> <td id='"+obj_avaliables_tickets['name']+"_cant'>"+obj_avaliables_tickets['count']+"</td> <td id='"+obj_avaliables_tickets['name']+"_ubication'>"+obj_avaliables_tickets['name']+"</td><td id='"+obj_avaliables_tickets['name']+"_cost'>"+obj_avaliables_tickets['cost']+"</td><td id='"+obj_avaliables_tickets['name']+"_id' style='display:none'>"+obj_avaliables_tickets['id']+"</td></tr>";
                len += 1;
            }
            var select_tribuna = document.getElementById("select_tribuna");
            var tamaño = select_tribuna.length;
            for (var i = 1; i < tamaño; i++) {
                select_tribuna.remove(1);					
            }
            for (var i = 0; i <json.avalibleTicket.length; i++) {
                var obj_avaliables_tickets = json.avalibleTicket[i];
                var optionNew=document.createElement("option");
                optionNew.text=obj_avaliables_tickets['name'];
                select_tribuna.add(optionNew);
            }
            
        }
    });
});

$("#post_venta").submit(function(e){
    e.preventDefault();			
    document.getElementById("post_venta_envio").value = createJson();
    document.getElementById('select_metodo_pago').selectedIndex="0";
    console.log("ANTES DEL AJAX")
    console.log(document.getElementById("post_venta_envio").value);
    var prueba = $('#post_venta_envio').val()
    console.log("CON JQUERY : "+prueba)
    console.log(typeof prueba)
    $.ajax({
        url:$(this).attr('action'),
        type:$(this).attr('method'),
        data:{
            csrfmiddlewaretoken: '{{ csrf_token }}',
            post_venta_envio: $('#post_venta_envio').val()
        },
        success: succesRequest
    });

});

function redirect(){
    location.href="/sales/saleEvent.html";
}

function succesRequest(result){
    if(result.status =='success'){
        document.getElementById('id02').style.display='none'
        $(document).ready(function(){
            $("#success").toggle(100);
            $("#success").fadeOut(3500);
        });
        setTimeout("redirect()", 2500);
    }
}

function showBill(){
     var table=document.getElementById("bill_table");
    var table_len=(table.rows.length);
    if (table_len == 2){
        alert("No a añadido ningun boleto");
    } else {
        document.getElementById('id02').style.display='block';
    }
}

function selectNewEvent(rowNum){		
    document.getElementById("get_event_selec").value = document.getElementById("event_s_"+rowNum).innerHTML;
    console.log("Mostrar en tabla : "+document.getElementById("event_s_"+rowNum).innerHTML);
    console.log("Mostrar seleccionado : "+document.getElementById("get_event_selec").value);
}


