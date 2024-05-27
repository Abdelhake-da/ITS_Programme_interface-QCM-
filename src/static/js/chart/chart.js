
function bar_chart(element_id, labels, data_set) {
    //  data set example
    // [{
    //         label: 'My First Dataset',
    //         data: [65, 59, 80, 81, 56, 55, 40],
    //         backgroundColor: [
    //                 'rgba(255, 99, 132, 0.2)',
    //         'rgba(255, 159, 64, 0.2)',
    //         'rgba(255, 205, 86, 0.2)',
    //         'rgba(75, 192, 192, 0.2)',
    //         'rgba(54, 162, 235, 0.2)',
    //         'rgba(153, 102, 255, 0.2)',
    //         'rgba(201, 203, 207, 0.2)'
    //     ],
    //     borderColor: [
    //             'rgb(255, 99, 132)',
    //             'rgb(255, 159, 64)',
    //             'rgb(255, 205, 86)',
    //             'rgb(75, 192, 192)',
    //             'rgb(54, 162, 235)',
    //             'rgb(153, 102, 255)',
    //             'rgb(201, 203, 207)'
    //         ],
    //     borderWidth: 1
    // }]
    var element = document.getElementById(element_id).getContext('2d')
    const data = {
        labels: labels,
        datasets: data_set
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        },
    };
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    var pieChart = new Chart(element, config)
}

function bubble_chart(element_id, data_set) {
    const data = {
        datasets: data_set
    };
    const config = {
        type: 'bubble',
        data: data,
        options: {}
    };
    var element = document.getElementById(element_id).getContext('2d')
    console.log('hello')
    var bubbleChart = new Chart(element, config)
}

function pie_chart(element_id, labels, data_set) {
    //  data set example
    //    [ {
    //         label: 'My First Dataset',
    //             data: [300, 50, 100],
    //                 backgroundColor: [
    //                     'rgb(255, 99, 132)',
    //                     'rgb(54, 162, 235)',
    //                     'rgb(255, 205, 86)'
    //                 ],
    //                     hoverOffset: 4
    //     }]
    var element = document.getElementById(element_id).getContext('2d')
    const data = {
        labels:labels,
        datasets:data_set
    };
    
    const config = {
        type: 'pie',
        data: data,
        options: {
            maintainAspectRatio: false,
            responsive: true,
        }
    };
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    var pieChart = new Chart(element, config)
}

function doughnut_chart(element_id, labels, data_set) {
    //  data set example
    //    [ {
    //         label: 'My First Dataset',
    //             data: [300, 50, 100],
    //                 backgroundColor: [
    //                     'rgb(255, 99, 132)',
    //                     'rgb(54, 162, 235)',
    //                     'rgb(255, 205, 86)'
    //                 ],
    //                     hoverOffset: 4
    //     }]
    var element = document.getElementById(element_id).getContext('2d')
    const data = {
        labels: labels,
        datasets: data_set
    };

    const config = {
        type: 'doughnut',
        data: data,
        options: {
            maintainAspectRatio: false,
            responsive: true,
        }
    };
    //Create pie or douhnut chart
    // You can switch between pie and douhnut using the method below.
    var pieChart = new Chart(element, config)
}


function line_chart(element_id, labels, data_set) {
    // [{
    //     label: 'My First Dataset',
    //     data: [65, 59, 80, 81, 56, 55, 40],
    //     fill: false,
    //     borderColor: 'rgb(75, 192, 192)',
    //     tension: 0.1
    // }]
    const data = {
        labels: labels,
        datasets: change_fill(data_set)
    };
    const config = {
        type: 'line',
        data: data,
    };
    var element = document.getElementById(element_id).getContext('2d')
    var lineChart = new Chart(element, config)
}
function mixed_chart(element_id, label, data_set) {
    // [{
    //     type: 'bar',
    //     label: 'Bar Dataset',
    //     data: [10, 20, 30, 40],
    //     borderColor: 'rgb(255, 99, 132)',
    //     backgroundColor: 'rgba(255, 99, 132, 0.2)'
    // }, {
    //         type: 'line',
    //         label: 'Line Dataset',
    //         data: [50, 50, 50, 50],
    //         fill: false,
    //         borderColor: 'rgb(54, 162, 235)'
    //     }]
    const data = {
        labels:label,
        datasets: data_set
    };
    const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };
    var element = document.getElementById(element_id).getContext('2d')
    var mixedChart = new Chart(element, config)
}
function polar_area_chart(element_id, label, data_set) {
    // [{
    //     label: 'My First Dataset',
    //     data: [11, 16, 7, 3, 14],
    //     backgroundColor: [
    //         'rgb(255, 99, 132)',
    //         'rgb(75, 192, 192)',
    //         'rgb(255, 205, 86)',
    //         'rgb(201, 203, 207)',
    //         'rgb(54, 162, 235)'
    //     ]
    // }]
    const data = {
        labels: label,
        datasets: data_set
    };
    const config = {
        type: 'polarArea',
        data: data,
        options: {}
    };
    
    var element = document.getElementById(element_id).getContext('2d')
    var polarAreaChart = new Chart(element, config)
    
}
function change_fill(data) {
    for (i in data){
        data[i].fill = Boolean(data[i].fill)
    }
    return data
    
}
function radar_chart(element_id, label, data_set) {
    // [{
    //     label: 'My First Dataset',
    //     data: [65, 59, 90, 81, 56, 55, 40],
    //     fill: true,
    //     backgroundColor: 'rgba(255, 99, 132, 0.2)',
    //     borderColor: 'rgb(255, 99, 132)',
    //     pointBackgroundColor: 'rgb(255, 99, 132)',
    //     pointBorderColor: '#fff',
    //     pointHoverBackgroundColor: '#fff',
    //     pointHoverBorderColor: 'rgb(255, 99, 132)'
    // }, {
    //         label: 'My Second Dataset',
    //         data: [28, 48, 40, 19, 96, 27, 100],
    //         fill: true,
    //         backgroundColor: 'rgba(54, 162, 235, 0.2)',
    //         borderColor: 'rgb(54, 162, 235)',
    //         pointBackgroundColor: 'rgb(54, 162, 235)',
    //         pointBorderColor: '#fff',
    //         pointHoverBackgroundColor: '#fff',
    //         pointHoverBorderColor: 'rgb(54, 162, 235)'
    //     }]
    const data = {
        labels: label,
        datasets: change_fill(data_set)
    };
    const config = {
        type: 'radar',
        data: data,
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            }
        },
    };

    var element = document.getElementById(element_id).getContext('2d')
    var radarChart = new Chart(element, config)

}

function scatter_chart(element_id, data_set) {
    //     [{
    //     label: 'Scatter Dataset',
    //         data: [{
    //             x: -10,
    //             y: 0
    //         }, {
    //             x: 0,
    //             y: 10
    //         }, {
    //             x: 10,
    //             y: 5
    //         }, {
    //             x: 0.5,
    //             y: 5.5
    //         }],
    //             backgroundColor: 'rgb(255, 99, 132)'
    // }],
    const data = {
        
        datasets: data_set
    };
    const config = {
        type: 'scatter',
        data: data,
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    };

    var element = document.getElementById(element_id).getContext('2d')
    var scatterChart = new Chart(element, config)

}