function graphql_resolve(graphQ){
    console.log('in graphql_resolve')
    let arrOpen = graphQ.split('{ ').map((r, i) => {
        return r+'{\n'+('\t'.repeat(i+1))
    }).join('{ ')
    console.log(arrOpen)
    $('#query').text(arrOpen)
    $('#query').text(graphQ)
    return $.ajax({
        type : 'GET',
        url: $SCRIPT_ROOT + '/graphql',
        data: {
            query: graphQ
        },
        success: function(data){
            $('#response').text(JSON.stringify(data.data, null, 2))
            return data.data
        },//success
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log( "Request failed: " + textStatus + " "+ errorThrown );
        }//error
    });//$ajax
}

function cuandollega_http(d, l, p, days = 30){
    return $.ajax({
        type : 'GET',
        url: $SCRIPT_ROOT + '/cuandoLlego',
        data: {
            deltaDias: days,
            fecha: d,
            linea: l,
            parada: p
        },
        success: function(data){
            return data
        },//success
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log( "Request failed: " + textStatus + " "+ errorThrown );
        }//error
    });//$ajax
}

function cuandoLlega(l, p, cuadro, i = 0){
    console.log(cuadro[i])
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

$(function() {
    var graphQ = `{ cuadrosByLineaParada(idLinea:1, idParada:1104){ id idLinea idParada hora }}`
    $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
        let l = 1
        let p = 1104
        console.log(data.data)
        cuandoLlega(l, p, data.data.cuadrosByLineaParada)
    });
})