$(function() {

    //Consultar
    $('button#consultar').bind('click', function() {
        if( $('#paradaInput').val() === '' )
            return
        let d = d_format(new Date())
        let l = $('#sLineas').val()
        let p = $('#paradaInput').val()
        $('#arrive').html();
        $.when( cuandollega_http( d, l, p ) )
            .then(function( data, textStatus, jqXHR ) {
                let parts = data.substring(1).slice(0, -1).split(', ')
                let first = parseInt(parts[0])
                let second = parseInt(parts[1])
                if(Number.isNaN(first) ||  Number.isNaN(second))
                    $('#arrive').html('Próximo servicio no encontrado.')
                else{
                    if( first < 0){
                        $('#arrive').html('El anterior servicio pasó hace: '+((first/60).toFixed())+' minutos. ')
                        $('#arrive').html($('#arrive').html()+'Próximo servicio en: '+((second/60).toFixed())+' minutos.')
                     } else {
                     $('#arrive').html($('#arrive').html()+'Próximo servicio en: '+((first/60).toFixed())+' minutos.')
                     }
                }
            });
    });
});