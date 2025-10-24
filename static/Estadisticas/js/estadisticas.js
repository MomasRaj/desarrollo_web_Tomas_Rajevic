Highcharts.chart("container", {
  chart: {
    type: "line",
  },
  title: {
    text: "Numero de avisos de adopción Enviados en el Tiempo",
  },
  xAxis: {
    type: "datetime",
    dateTimeLabelFormats: {
      month: "%b %e, %Y",
    },
    title: {
      text: "Fecha",
    },
  },
  yAxis: {
    title: {
      text: "Numero de Confesiones",
    },
  },
  legend: {
    align: "left",
    verticalAlign: "top",
    borderWidth: 0,
  },

  tooltip: {
    shared: true,
    crosshairs: true,
  },

  series: [
    {
      name: "Avisos de adopción",
      data: [],
      lineWidth: 1,
      marker: {
        enabled: true,
        radius: 4,
      },
      color: "#FC2865",
    },
  ],
});

fetch("http://127.0.0.1:5000/get-stats-data")
  .then((response) => response.json())
  .then((data) => {
    let parsedData = data.map((item) => {
      const [year, month, day] = item.date
        .split("-")
        .map((part) => parseInt(part, 10));
      return [
        Date.UTC(year, month - 1, day), 
        item.count,
      ];
    });


    const chart = Highcharts.charts.find(
      (chart) => chart && chart.renderTo.id === "container"
    );


    chart.update({
      series: [
        {
          data: parsedData,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));

fetch("http://127.0.0.1:5000/get-stats-type")
  .then((response) => response.json())
  .then((data) => {
    const pieData = data.map((item) => {
      return {
        name: item.type,
        y: Number(item.count),
      };
    });

    Highcharts.chart("pie-container", {
      chart: {
        type: "pie",
      },
      title: {
        text: "Avisos de adopción por tipo de mascota",
      },
      tooltip: {
        pointFormat: "{series.name}: <b>{point.y}</b>",
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: "pointer",
          dataLabels: {
            enabled: true,
            format: "<b>{point.name}</b>: {point.y}",
          },
        },
      },
      series: [
        {
          name: "Avisos",
          colorByPoint: true,
          data: pieData,
        },
      ],
    });
  })
  .catch((error) => console.error("Error:", error));

fetch("http://127.0.0.1:5000/get-stats-monthly-type")
  .then((response) => response.json())
  .then((data) => {
    const categories = data.map((item) => item.month);
    const perros = data.map((item) => Number(item.perro));
    const gatos = data.map((item) => Number(item.gato));

    Highcharts.chart("bar-container", {
      chart: {
        type: "column",
      },
      title: {
        text: "Avisos de adopción por mes y tipo",
      },
      xAxis: {
        categories: categories,
        title: {
          text: "Mes",
        },
        crosshair: true,
      },
      yAxis: {
        min: 0,
        title: {
          text: "Cantidad",
        },
      },
      tooltip: {
        shared: true,
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat:
          '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
          '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: "</table>",
        useHTML: true,
      },
      plotOptions: {
        column: {
          pointPadding: 0.2,
          borderWidth: 0,
        },
      },
      series: [
        {
          name: "Perro",
          data: perros,
          color: "#1f77b4",
        },
        {
          name: "Gato",
          data: gatos,
          color: "#ff7f0e",
        },
      ],
    });
  })