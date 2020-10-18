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
            console.log(data)
            return data
        },//success
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log( "Request failed: " + textStatus + " "+ errorThrown );
        }//error
    });//$ajax
}

function d_format(d){
    return [d.getFullYear(),
           (d.getMonth()+1).toString().padStart(2, '0'),
           d.getDate().toString().padStart(2, '0')].join('-')+' '+
          [d.getHours().toString().padStart(2, '0'),
           d.getMinutes().toString().padStart(2, '0'),
           d.getSeconds().toString().padStart(2, '0')].join(':')+'.0000';
}