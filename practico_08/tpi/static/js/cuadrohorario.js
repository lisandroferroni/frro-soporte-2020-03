function cuandoLlega(l, p, cuadro, i = 0){
    console.log(cuadro[i])
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
          '<td class="border px-4 py-2">'+l+'</td>'+
          '<td class="border px-4 py-2">'+p+'</td>'+
          '<td class="border px-4 py-2">'+d+'</td>'+
          '<td class="border px-4 py-2">'+d_format(new Date(date.getTime() + (first*1000)))+'</td>'+
          '<td class="border px-4 py-2">'+((first/60).toFixed())+' minutos</td>'+
        '</tr>');
        console.log('date: ',d,' próximo: ',data)
        if(i < 24)
            cuandoLlega(l, p, cuadro, i+1)
    });
}

function cuandoLlega_gql(idL, idP){
    //Populate cuadro horarios
    console.log(idL, idP)
    var graphQ = `{ cuadrosByLineaParada(idLinea:`+idL+`, idParada:`+idP+`){ id idLinea idParada hora }}`
    $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
        console.log(data.data)
        if(data.data.length === 0)
            $('#tbody:last-child').append('<tr class="text-center">'+
                '<td class="border px-4 py-2" colspan="5">No hay cuadro de horarios para la parada seleccionada.</td>'+
            '</tr>');
        cuandoLlega(idL, idP, data.data.cuadrosByLineaParada)
    });
}

$('button#consultar').bind('click', function() {
    let l = $('#sLineas').val()
    let p = $('#paradaInput').val()
    cuandoLlega_gql(l, p)
})