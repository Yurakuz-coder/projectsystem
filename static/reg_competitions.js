function applySpec() {
  const spec = document.getElementById("spec").value;
  console.log(spec);
  if (!spec) {
    return;
  }
  getDataComp(spec);
}

function getDataComp(spec) {
  $.ajax({
    type: "POST",
    url: "/admin/competitions",
    dataSrc: "data",
    data: { spec },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadCsvCompFile() {
  const formData = new FormData();
  const button = document.getElementById("button-upload-csv");
  const file = document.getElementById("input-upload-csv").files[0];
  if (!file) return;
  formData.append("file", file);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/admin/csvComp",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}


function getCompetitions(spec, op) {
  $.ajax({
    type: "GET",
    url: "/admin/getCompetition",
    data: { spec },
    success: function (data) {
      const select = document.getElementById(op + "Comp");
      const button = document.getElementById(op + "CompButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Компетенции не найдены", 0));
        select.disabled = true;
        button.disabled = true
        return;
      }
      select.disabled = false;
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item.competensionsShifr}`,
            item.IDcompetensions
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
