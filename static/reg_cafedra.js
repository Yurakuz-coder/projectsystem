function applyCafedraFilters() {
  const cafedraFIO = document.getElementById("cafedraFIO").value;
  const cafedraPos = document.getElementById("cafedraPos").value;
  if (!cafedraFIO && !cafedraPos) {
    return;
  }
  getData(cafedraFIO, cafedraPos);
}

function dropCafedraFilters() {
  getData(null, null);
}

function getData(cafedraFIO, cafedraPos) {
  $.ajax({
    type: "POST",
    url: "/admin/cafedra",
    dataSrc: "data",
    data: { cafedraFIO, cafedraPos },
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

function uploadCsvCafedraFile() {
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
    url: "/admin/csvCafedra",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}