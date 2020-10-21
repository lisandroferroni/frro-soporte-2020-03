var configG = {
    type: 'pie',
    data: {
        datasets: [{
            data: [ 50, 50],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
            ],
            label: 'Dataset 1'
        }],
        labels: [
            'Masculino',
            'Femenino'
        ]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por Género'
        }
    }
};
var ctx = document.getElementById('genero').getContext('2d');
var generoChart = new Chart(ctx, configG)

var configT = {
    type: 'pie',
    data: {
        datasets: [{
            data: [ 0, 0, 0, 0 ],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            label: 'Dataset 1'
        }],
        labels: [
            'Medio boleto',
            'Pase',
            'Normal',
            'Jubilado'
        ]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por Tipo'
        }
    }
};
var ctx = document.getElementById('tipo').getContext('2d');
var tipoChart = new Chart(ctx, configT)


var configD = {
    type: 'pie',
    data: {
        datasets: [{
            data: [ 0, 0 ],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            label: 'Dataset 1'
        }],
        labels: [
            'Día',
            'Noche'
        ]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por Momento del día'
        }
    }
};
var ctx = document.getElementById('diaNoche').getContext('2d');
var diaChart = new Chart(ctx, configD)

var MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
var configM = {
    type: 'line',
    data: {
        labels: [], //Months
        datasets: [{
            label: 'My First dataset',
            backgroundColor: "rgb(255, 99, 132)",
            borderColor: "rgb(255, 99, 132)",
            data: [ //Value of Months
            ],
            fill: false,
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por meses'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Mes'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Boletos'
                }
            }]
        }
    }
};
var ctx = document.getElementById('mes').getContext('2d');
var mesesChart = new Chart(ctx, configM)


var configDia = {
    type: 'pie',
    data: {
        datasets: [{
            data: [0,0],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            label: 'My dataset' // for legend
        }],
        labels: [
            'Masculino',
            'Femenino'
        ]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por género durante el día'
        }
    }
};
var ctx = document.getElementById('diaG').getContext('2d');
var diaFChart = new Chart(ctx, configDia)

var configNoche = {
    type: 'pie',
    data: {
        datasets: [{
            data: [0,0],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            label: 'My dataset' // for legend
        }],
        labels: [
            'Masculino',
            'Femenino'
        ]
    },
    options: {
        maintainAspectRatio: false,
        responsive: true,
        title: {
            display: true,
            text: 'Boletos marcados por género durante la noche'
        }
    }
};
var ctx = document.getElementById('nocheG').getContext('2d');
var nocheGChart = new Chart(ctx, configNoche)

function getBoletos(d){
    var graphQ = `query{
        boletosByDeltadias(deltaDias:`+d+`){
            id
            genero
            tipo
            createdDate
        }
    }`
    $.when( graphql_resolve(graphQ) ).then(function( data, textStatus, jqXHR ) {
        console.log(data.data)
        //Género
        configG.data.datasets[0].data = []
        configG.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => x.genero === '0').length )
        configG.data.datasets[0].data.push( data.data.boletosByDeltadias.length - configG.data.datasets[0].data[0] )
        generoChart.update();
        //Tipo
        configT.data.datasets[0].data = []
        configT.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => x.tipo === 'Medio').length )
        configT.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => x.tipo === 'Pase').length )
        configT.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => x.tipo === 'Normal').length )
        configT.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => x.tipo === 'Jubilado').length )
        tipoChart.update()
        //Día
        configD.data.datasets[0].data = []
        configD.data.datasets[0].data.push( data.data.boletosByDeltadias.filter(x => { //Día
            let h = parseInt(x.createdDate.split('T')[1].split(':')[0])
            return h > 7 && h < 20
        } ).length )
        configD.data.datasets[0].data.push( data.data.boletosByDeltadias.length - configD.data.datasets[0].data[0] )
        diaChart.update()
        //Meses
        configM.data.labels = []
        configM.data.datasets[0].data = []
        data.data.boletosByDeltadias.forEach((x, i) => {
            let m = parseInt(x.createdDate.split('T')[0].split('-')[1])
            let mIndex = configM.data.labels.indexOf( MONTHS[m-1] )
            if( mIndex === -1 ){ //Case month its not considered
                configM.data.labels.push( MONTHS[m-1] ) //Push month name
                configM.data.datasets[0].data.push(0) //Push counter
                mIndex = 0
            }
            configM.data.datasets[0].data[mIndex]++
        })
        configM.data.labels = configM.data.labels.reverse()
        configM.data.datasets[0].data = configM.data.datasets[0].data.reverse()
        mesesChart.update()
        //Género en el día
        configDia.data.datasets[0].data[0] = data.data.boletosByDeltadias.filter(x => { //Masculino
            let h = parseInt(x.createdDate.split('T')[1].split(':')[0])
            return h > 7 && h < 20 && x.genero === '0'
        } ).length
        configDia.data.datasets[0].data[1] = data.data.boletosByDeltadias.filter(x => { //Femenino
            let h = parseInt(x.createdDate.split('T')[1].split(':')[0])
            return h > 7 && h < 20 && x.genero === '1'
        } ).length
        diaFChart.update()
        //Género a la noche
        configNoche.data.datasets[0].data[0] = data.data.boletosByDeltadias.filter(x => { //Masculino
            let h = parseInt(x.createdDate.split('T')[1].split(':')[0])
            return (h >= 20 || h <= 7) && x.genero === '0'
        } ).length
        configNoche.data.datasets[0].data[1] = data.data.boletosByDeltadias.filter(x => { //
            let h = parseInt(x.createdDate.split('T')[1].split(':')[0])
            return (h >= 20 || h <= 7) && x.genero === '1'
        } ).length
        nocheGChart.update()

    });
}

$( "#diasInput" ).change(function() {
    var dias = $('#diasInput').val()
    getBoletos(dias)
});

$(function() {
    getBoletos(30)
})