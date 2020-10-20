function cuandoLlega(l, p, cuadro, lName, i = 0){
    if(i === 0)
        $('#tbody').html('')
    if(typeof cuadro[i] === 'undefined')
        return
    let cuadroParts = cuadro[i].hora.split(':')
    let date = new Date(2020,09,24, cuadroParts[0], cuadroParts[1],cuadroParts[2])
    let d = d_format(date)
    $.when( cuandollega_http( d, l, p ) )
        .then(function( data, textStatus, jqXHR ) {
        let parts = data.substring(1).slice(0, -1).split(', ')
        let first = parseInt(parts[0])
        let second = parseInt(parts[1])
        $('#tbody:last-child').append('<tr>'+
          '<td class="border px-4 py-2">'+lName+'</td>'+
          '<td class="border px-4 py-2">'+p+'</td>'+
          '<td class="border px-4 py-2">'+d.slice(0, -8).slice(11)+'</td>'+
          '<td class="border px-4 py-2">'+d_format(new Date(date.getTime() + (first*1000))).slice(0, -8).slice(11)+'</td>'+
          '<td class="border px-4 py-2">'+((first/60).toFixed())+' minutos</td>'+
        '</tr>');
        if(i < 24)
            cuandoLlega(l, p, cuadro, lName, i+1)
    });
}

function cuandoLlega_gql(idL, idP, lName){
    //Populate cuadro horarios
    var graphQ = `{ cuadrosByLineaParada(idLinea:`+idL+`, idParada:`+idP+`){ id idLinea idParada hora }}`
    $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
        if(data.data.length === 0)
            $('#tbody:last-child').append('<tr class="text-center">'+
                '<td class="border px-4 py-2" colspan="5">No hay cuadro de horarios para la parada seleccionada.</td>'+
            '</tr>');
        cuandoLlega(idL, idP, data.data.cuadrosByLineaParada, lName)
    });
}

$('button#consultar').bind('click', function() {
    let l = $('#sLineas').val()
    let lName = $('#sLineas option:selected').text()
    let p = $('#paradaInput').val()
    cuandoLlega_gql(l, p, lName)
})