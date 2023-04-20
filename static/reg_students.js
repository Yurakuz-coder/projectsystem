function applyStudentsFilters() {
  const fio = document.getElementById("fio").value;
  const grname = document.getElementById("grname").value;
  if (!fio && !grname) {
    return;
  }
  getDataStudents(fio, grname);
}

function dropStudentsFilters() {
  getDataStudents(null, null);
}

function getDataStudents(fio, grname) {
  $.ajax({
    type: "POST",
    url: "/admin/students",
    dataSrc: "data",
    data: { fio, grname },
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

function uploadCsvStudFile() {
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
    url: "/admin/csvStud",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}
