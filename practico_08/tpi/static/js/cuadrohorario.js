
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

function cuandoLlega(l, p, i = 0){
    let date = new Date(2020,09,24, i, 00,00)
    let d = d_format(date)
    $.when( cuandollega_http( d, l, p ) )
        .then(function( data, textStatus, jqXHR ) {
        let parts = data.substring(1).slice(0, -1).split(', ')
        let first = parseInt(parts[0])
        let second = parseInt(parts[1])
        $('#tbody:last-child').append('<tr>'+
          '<td class="border px-4 py-2">'+p+'</td>'+
          '<td class="border px-4 py-2">'+d+'</td>'+
          '<td class="border px-4 py-2">'+d_format(new Date(date.getTime() + (first*1000)))+'</td>'+
          '<td class="border px-4 py-2">'+((first/60).toFixed())+' minutos</td>'+
        '</tr>');
        console.log('date: ',d,' próximo: ',data)
        if(i < 24)
            cuandoLlega(l, p, i+1)
    });
}

$(function() {

    let l = 1
    let p = 1104
    cuandoLlega(l, p)


    /*for(i=0; i<24; i++){
        let date = new Date(2020,09,24, i, 00,00)
        let d = d_format(date)

        await $.when( cuandollega_http( d, l, p ) )
        .then(function( data, textStatus, jqXHR ) {
        date.setSeconds(date.getSeconds() + data);
        let milliseconds= data * 1000;
        $('#tbody:last-child').append('<tr>'+
          '<td class="border px-4 py-2">'+p+'</td>'+
          '<td class="border px-4 py-2">'+d+'</td>'+
          '<td class="border px-4 py-2">'+new Date(date.getTime() + milliseconds)+'</td>'+
          '<td class="border px-4 py-2">'+data+'</td>'+
        '</tr>');
            console.log('date: ',d,' próximo: ',data)
        });
    }*/
})