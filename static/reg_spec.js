function applySpecFilters() {
  const shifrFilters = document.getElementById("shifrFilter").value;
  const naprFilters = document.getElementById("napravFilter").value;
  if (!shifrFilters && !naprFilters) {
    return;
  }
  getData(shifrFilters, naprFilters)
}


function dropSpecFilters() {
  getData(null, null)
}

function getData(shifrFilters, naprFilters) {
  $.ajax({
    type: "POST",
    url: "/admin/specializations",
    dataSrc: "data",
    data: { shifrFilters, naprFilters },
    success: function (data) {
      const table = document.getElementById("collapseTableBody")
      table.innerHTML = data;
      table.className = 'collapse show'
    },
    error: function (err) {
      console.log(err)
    },
  });
}

function uploadCsvSpecFile() {
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
    url: "/admin/csvSpec",
    success: function () {
      button.innerHTML = "Файл загружен!";
    },
    error: function (data) {
      button.innerHTML = "Файл не загружен! - " + data?.responseText;
    },
  });
}
