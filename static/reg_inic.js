function applyInicFilters() {
  const fioFilter = document.getElementById("fioFilter")?.value;
  const posFilter = document.getElementById("posFilter")?.value;
  if (!fioFilter && !posFilter) {
    return;
  }
  getDataInic(fioFilter, posFilter);
}

function dropInicFilters() {
  getDataInic(null, null, null);
}

function getDataInic(fioFilter, posFilter) {
  $.ajax({
    type: "POST",
    url: "/shefforg/iniciators",
    dataSrc: "data",
    data: { fioFilter, posFilter },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadCsvInicFile() {
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
    url: "/admin/csvInic",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}
