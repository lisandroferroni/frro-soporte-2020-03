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
            return
            $('#response').text(JSON.stringify(data.data, null, 2))
            return data.data
        },//success
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            console.log( "Request failed: " + textStatus + " "+ errorThrown );
        }//error
    });//$ajax
}

$(function() { //Populate paradas
    var graphQ = `{ allLineas{ edges{ node{ id name } } } }`
    $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
        data.data.allLineas.edges.forEach(function(p){
            $('#sLineas').append(`<option value="${p.node.id}">${p.node.name}</option>`);
        })
    });
});


$(function() {
    var calle_id = ''
    $( "#calle" ).change(function() {
        var id_linea = $('#sLineas').val()
        var graphQ = `query{
            calle2ByIdlineaCalle1(idLinea: `+id_linea+`, idCalle1: `+$( this ).val()+`){
                calle2 {
                    id
                    nombre
                }
            }
        }`
        $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
            $('#calleInterseccion').empty()
            data.data.calle2ByIdlineaCalle1.forEach(c => $('#calleInterseccion').append(`<option value="${c.calle2.id}">${c.calle2.nombre}</option>`));
        });
    });

    function getInterseccion($) { //Buscando intersección luego de click en Calle
        var graphQ = `query{ interSearch(q: "`+calle_id+`"){ id calle2{ id nombre } } }`
        $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
            $('#calleI_search').toggle();
            $('#calleInterseccion').empty()
            data.data.interSearch.forEach(i => $('#calleInterseccion').append(`<option value="${i.calle2.id}">${i.calle2.nombre}</option>`));
        });
    };
    $('#calle_search').bind('click', function() {
        $( "input#calle" ).val($( this ).text())
        $( "input#calle_value" ).val($( this ).text())
        getInterseccion($)
        $( this ).toggle()
    })
    $('#sLineas').change(function() {
        var calle1 = $(this).val()
        var graphQ = `query{ calle1ByIdLinea(idLinea: `+calle1+`){ calle1{ id nombre } } }`
        $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
            $('#calle').empty()
            data.data.calle1ByIdLinea.forEach(c => $('#calle').append(`<option value="${c.calle1.id}">${c.calle1.nombre}</option>`));
        });
    })
    $('#calleInterseccion').change(function() {
        var linea = $('#sLineas').val()
        var calle1 = $('#calle').val()
        var graphQ = `query{ paradaByIdlineaC1C2(idLinea: `+linea+`, idCalle1: `+calle1+`, idCalle2: `+$( this ).val()+`){ idParada } }`
        $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
            if(data.data.paradaByIdlineaC1C2.length > 0)
                $('#paradaInput').val( data.data.paradaByIdlineaC1C2[0].idParada );
        });
    })
    $('button#lineas').bind('click', function() {
        var graphQ = `query{ lineas{ id name paradas{ edges{ node{ id idCallePpal idCalleCruce } } } } }`
        $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
            console.log(data.data)
        });
    });
    //Consultar
    $('button#consultar').bind('click', function() {
        if( $('#paradaInput').val() === '' )
            return
        let d = d_format(new Date())
        let l = $('#sLineas').val()
        let p = $('#paradaInput').val()
        $.when( cuandollega_http( d, l, p ) )
            .then(function( data, textStatus, jqXHR ) {
                if(!data.includes('0:'))
                    $('#arrive').html('Próximo servicio no encontrado.')
                else{
                    let arrHour = data.split(':')
                    if(arrHour.length > 1)
                        $('#arrive').html('Próximo servicio en: '+arrHour[1]+' minutos.')
                }
            });
    });
});